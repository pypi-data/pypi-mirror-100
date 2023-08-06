# Copyright (c) Ye Liu. All rights reserved.

from collections import OrderedDict
from itertools import permutations

import torch

import nncore
from .buffer import Buffer
from .comm import gather, is_main_process, synchronize
from .hooks import HOOKS, Hook
from .utils import get_checkpoint, load_checkpoint

_DEFAULT_STAGES = dict(
    epochs=5,
    optimizer=dict(type='SGD', lr=1e-2, momentum=0.9, weight_decay=1e-4),
    lr_schedule=dict(type='iter', policy='cosine'),
    warmup=dict(type='iter', policy='linear', steps=500, ratio=0.001),
    validation=dict(interval=1))

_DEFAULT_HOOKS = [
    'TimerHook', 'LrUpdaterHook', 'OptimizerHook', 'CheckpointHook',
    'EvalHook', 'EventWriterHook'
]


@nncore.bind_getter('mode', 'model_cfg', 'hooks', 'max_stages', 'max_epochs',
                    'max_iters', 'start_iter', 'stage', 'epoch', 'iter')
class Engine(object):
    """
    An engine that can take over the whole training, validation and testing
    process, with all the baby-sitting works (stage control, optimizer
    configuration, lr scheduling, checkpoint management, metrics & tensorboard
    writing, etc.) done automatically.

    Args:
        model (:obj:`nn.Module`): The model to be trained or tested. The
            :obj:`forward` method of the model should return a dict containing
            ``_num_samples`` indicating the number of samples in the current
            batch.
        data_loaders (dict): The data loaders for training, validating and
            testing. It should be in the format of
            ``dict(train=train_loader, val=val_loader, test=test_loader)``.
        stages (dict, list[dict], optional): The stage config or list of stage
            configs to be scheduled. Default: ``_DEFAULT_STAGES``.
        hooks (list[:obj:`Hook`] or list[dict] or list[str], optional): The
            list of hooks to be registered. Each hook could be represented as a
            :obj:`Hook`, a dict or a str. Default: ``_DEFAULT_HOOKS``.
        batch_processor (callable, optional): A customized callable method
            that processes a data batch. It should be in the format of
            ``batch_processor(model, data, mode, **kwargs) -> dict`` where mode
            could be ``train``, ``val`` or ``test``. If ``None``, the default
            batch processors will be used. Default: ``None``.
        buffer_size (int, optional): Maximum size of the buffer. Default:
            ``100000``.
        logger (:obj:`logging.Logger` or str or None, optional): The logger or
            name of the logger to be used. Default: ``None``.
        work_dir (str, optional): Path to the working directory. If ``None``,
            the default working directory will be used Default: ``None``.
    """

    def __init__(self,
                 model,
                 data_loaders,
                 stages=_DEFAULT_STAGES,
                 hooks=_DEFAULT_HOOKS,
                 batch_processor=None,
                 buffer_size=100000,
                 logger=None,
                 work_dir=None,
                 **kwargs):
        self.model = model
        self.batch_processor = batch_processor

        for a, b in permutations(('val', 'test')):
            if a in data_loaders and b not in data_loaders:
                data_loaders[b] = data_loaders[a]
        self.data_loaders = data_loaders

        if isinstance(stages, dict):
            stages.update(kwargs)
        self.stages = stages if isinstance(stages, (list, tuple)) else [stages]

        self._hooks = OrderedDict()
        if hooks is not None:
            self.register_hook(hooks)

        time_str = nncore.get_timestamp()
        self.work_dir = work_dir or nncore.join('work_dirs', time_str)

        log_file = nncore.join(self.work_dir, time_str + '.log')
        self.logger = nncore.get_logger(logger, log_file=log_file)

        self.buffer = Buffer(max_size=buffer_size, logger=logger)
        self.reset_states()

    @property
    def cur_stage(self):
        return self.stages[self._stage]

    @property
    def epoch_in_stage(self):
        cumsum = 0
        for stage in self.stages:
            if self._epoch + 1 <= cumsum + stage['epochs']:
                return self._epoch - cumsum
            cumsum += stage['epochs']
        return self.stages[-1]['epochs']

    @property
    def iter_in_stage(self):
        cumsum = 0
        for i in range(self._stage):
            cumsum += len(
                self.data_loaders['train']) * self.stages[i]['epochs']
        return self._iter - cumsum

    @property
    def iter_in_epoch(self):
        return self._iter - len(self.data_loaders['train']) * self._epoch

    def _call_hook(self, name):
        for hook in self._hooks.values():
            getattr(hook, name)(self)

    def reset_states(self):
        self.buffer.clear()
        self._max_stages = len(self.stages)
        self._max_epochs = sum(stage['epochs'] for stage in self.stages)
        self._max_iters = (len(self.data_loaders['train']) if 'train'
                           in self.data_loaders else 0) * self._max_epochs
        self._start_iter = self._stage = self._epoch = self._iter = 0

    def register_hook(self, hook, before=None, overwrite=True, **kwargs):
        """
        Register a hook into the engine.

        Args:
            hook (list or :obj:`Hook` or dict or str): The hook or list of
                hooks to be registered. Each hook could be represented as a
                :obj:`Hook`, a dict or a str.
            before (str, optional): Name of the hook to be inserted before. If
                ``None``, the new hook will be added to the end of hook list.
                Default: ``None``.
            overwrite (bool, optional): Whether to overwrite the old hook with
                the same name if exists. Default: ``True``.
        """
        if isinstance(hook, (list, tuple)):
            for h in hook:
                self.register_hook(
                    h, before=before, overwrite=overwrite, **kwargs)
            return
        elif isinstance(hook, dict):
            hook = nncore.build_object(hook, HOOKS, **kwargs)
        elif isinstance(hook, str):
            hook = HOOKS.get(hook)(**kwargs)
        elif not isinstance(hook, Hook):
            raise TypeError("hook must be a Hook or dict, but got '{}'".format(
                type(hook)))

        if hook.name in self._hooks:
            if overwrite:
                self._hooks.pop(hook.name)
            else:
                raise KeyError("hook '{}' exists".format(hook.name))

        self._hooks[hook.name] = hook

        if before is not None:
            if before not in self._hooks:
                raise ValueError("hook '{}' not found".format(before))

            keys = list(self._hooks.keys())
            idx = keys.index(before)
            for key in keys[idx:-1]:
                self._hooks.move_to_end(key)

    def build_optimizer(self, optimizer):
        """
        Build an optimizer for the engine.

        Args:
            optimizer (any): A :obj:`optim.Optimizer` or a dict used for
                constructing the optimizer.
        """
        if isinstance(optimizer, dict):
            self.optimizer = nncore.build_object(
                optimizer, torch.optim, params=self.model.parameters())
        elif isinstance(optimizer, torch.optim.Optimizer):
            self.optimizer = optimizer
        else:
            raise TypeError("invalid optimizer: '{}'".format(optimizer))

    def load_checkpoint(self, checkpoint, strict=False):
        """
        Load checkpoint from a file or an URL.

        Args:
            checkpoint (dict or str): A dict, a filename, an URL or a
                ``torchvision://<model_name>`` string indicating the
                checkpoint.
            strict (bool, optional): Whether to allow different params for the
                model and checkpoint. If ``True``, raise an error when the
                params do not match exactly. Default: ``False``.
        """
        load_checkpoint(
            self.model,
            checkpoint,
            map_location=next(self.model.parameters()).device,
            strict=strict,
            logger=self.logger)

        if isinstance(checkpoint, str):
            self.logger.info('Loaded checkpoint from {}'.format(checkpoint))
        else:
            self.logger.info('Loaded checkpoint')

    def resume(self, checkpoint, strict=False):
        """
        Resume from a checkpoint file.

        Args:
            checkpoint (dict or str): A `dict`, filename, URL or
                ``torchvision://<model_name>`` string indicating the
                checkpoint.
            strict (bool, optional): Whether to allow different params for the
                model and checkpoint. If ``True``, raise an error when the
                params do not match exactly. Default: ``False``.
        """
        if isinstance(checkpoint, str):
            checkpoint = get_checkpoint(
                checkpoint, map_location=next(self.model.parameters()).device)

        if self.stages != checkpoint['meta']['stages']:
            self.logger.warn(
                'Stages in the engine and checkpoint are mismatch')

        load_checkpoint(
            self.model, checkpoint, strict=strict, logger=self.logger)

        self._epoch = checkpoint['meta']['epoch']
        self._iter = self._start_iter = checkpoint['meta']['iter']

        cumsum, count = 0, 0
        for stage in self.stages:
            if self._epoch + 1 <= cumsum + stage['epochs']:
                break
            count += 1
        self._stage = count

        if 'optimizer' in checkpoint:
            self.build_optimizer(self.cur_stage['optimizer'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
        else:
            raise KeyError('optimizer not found in the checkpoint')

        self.logger.info('Resumed stage {}, epoch {}, iter {}'.format(
            self._stage + 1, self._epoch, self._iter))

    def train_iter(self, data):
        self._call_hook('before_train_iter')

        if callable(self.batch_processor):
            output = self.batch_processor(
                self.model, data, mode=self._mode, **self._model_cfg)
        else:
            output = self.model(data, mode=self._mode, **self._model_cfg)

        self.losses = {k: v for k, v in output.items() if 'loss' in k}
        if 'loss' not in output:
            self.losses['loss'] = output['loss'] = sum(
                value for value in self.losses.values())

        for key, value in output.items():
            self.buffer.update(
                key,
                value.detach().cpu()
                if isinstance(value, torch.Tensor) else value)

        self._call_hook('after_train_iter')
        self._iter += 1

    def val_iter(self, data):
        self._call_hook('before_val_iter')

        if callable(self.batch_processor):
            output = self.batch_processor(
                self.model, data, mode=self._mode, **self._model_cfg)
        else:
            with torch.no_grad():
                output = self.model(data, mode=self._mode, **self._model_cfg)

        if any('loss' in key for key in output) and 'loss' not in output:
            output['loss'] = sum(v for k, v in output.items() if 'loss' in k)

        for key, value in output.items():
            self.buffer.update(
                key,
                value.detach().cpu()
                if isinstance(value, torch.Tensor) else value)

        self._call_hook('after_val_iter')

    def test_iter(self, data):
        if callable(self.batch_processor):
            output = self.batch_processor(
                self.model, data, mode=self._mode, **self._model_cfg)
        else:
            with torch.no_grad():
                output = self.model(data, mode=self._mode, **self._model_cfg)

        for key, value in output.items():
            self.buffer.update(
                key,
                value.detach().cpu()
                if isinstance(value, torch.Tensor) else value)

    def train_epoch(self):
        self._mode = 'train'
        self.model.train()
        self.data_loader = self.data_loaders[self._mode]
        self._call_hook('before_train_epoch')

        for data in self.data_loader:
            self.train_iter(data)

        self._call_hook('after_train_epoch')
        self._epoch += 1

    def val_epoch(self):
        self.logger.info('Validating...')
        self._mode = 'val'
        self.model.eval()
        self.data_loader = self.data_loaders[self._mode]
        self._call_hook('before_val_epoch')

        prog_bar = nncore.ProgressBar(len(self.data_loader))
        for data in self.data_loader:
            self.val_iter(data)
            prog_bar.update()

        self._call_hook('after_val_epoch')

    def test_epoch(self):
        self.logger.info('Evaluating...')
        self._mode = 'test'
        self.model.eval()
        self.data_loader = self.data_loaders[self._mode]

        prog_bar = nncore.ProgressBar(len(self.data_loader))
        for data in self.data_loader:
            self.test_iter(data)
            prog_bar.update()

    def run_stage(self):
        if isinstance(self.cur_stage['optimizer'], dict):
            optim = self.cur_stage['optimizer'].copy()
            optim_type = optim.pop('type')
            optim_args = ['{}: {}'.format(k, v) for k, v in optim.items()]
            optim = '{}({})'.format(optim_type, ', '.join(optim_args))
        else:
            optim = '{}()'.format(
                self.cur_stage['optimizer'].__class__.__name__)

        self.logger.info('Stage: {}, epochs: {}, optimizer: {}'.format(
            self._stage + 1, self.cur_stage['epochs'], optim))

        if self.epoch_in_stage == 0:
            self.build_optimizer(self.cur_stage['optimizer'])

        self._call_hook('before_stage')

        while self.epoch_in_stage < self.cur_stage['epochs']:
            self.train_epoch()
            if 'val' in self.data_loaders or 'test' in self.data_loaders:
                cfg = self.cur_stage.get('validation')
                if cfg is not None:
                    itr, off = cfg.get('interval', 0), cfg.get('offset', 0)
                    epoch = self.epoch_in_stage
                    if itr > 0 and epoch > off and epoch % itr == 0:
                        self.val_epoch()

        self._call_hook('after_stage')
        self._stage += 1

    def evaluate(self):
        blob = self.buffer.pop('out')
        blob = gather(blob)

        if is_main_process():
            blob = nncore.concat_list(blob)
            output = self.data_loader.dataset.evaluate(
                blob, logger=self.logger)
        else:
            output = dict()

        synchronize()
        return output

    def launch(self, eval_mode=False, **kwargs):
        """
        Launch engine.

        Args:
            eval_mode (bool, optional): Whether to only run evaluation.
                Default: ``False``.
        """
        self._model_cfg = kwargs

        if eval_mode:
            self.test_epoch()
            output = self.evaluate()
            self.logger.info(
                'Evaluation results: ' +
                ', '.join(['{}: {}'.format(k, v) for k, v in output.items()]))
            return output

        self.logger.info('Launch engine, host: {}, work_dir: {}'.format(
            nncore.get_host_info(), self.work_dir))
        self._call_hook('before_launch')

        while self._stage < self._max_stages:
            self.run_stage()

        self._call_hook('after_launch')
