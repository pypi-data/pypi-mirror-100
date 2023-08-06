# Copyright (c) Ye Liu. All rights reserved.

from .misc import bind_getter


@bind_getter('name', 'items')
class Registry(object):
    """
    A registry to map strings to objects.

    Records in the :obj:`self.items` maintain the registry of objects. For each
    record, the key is the object name and the value is the object itself. The
    method :obj:`self.register` can be used as a decorator or a normal
    function.

    Args:
        name (str): Name of the registry.

    Example:
        >>> backbones = Registry('backbone')
        >>> @backbones.register()
        >>> class ResNet(object):
        ...     pass

        >>> backbones = Registry('backbone')
        >>> class ResNet(object):
        ...     pass
        >>> backbones.register(ResNet)
    """

    def __init__(self, name):
        self._name = name
        self._items = dict()

    def __len__(self):
        return len(self._items)

    def __contains__(self, key):
        return key in self._items

    def __getattr__(self, key):
        if key in self._items:
            return self._items[key]
        else:
            raise AttributeError(
                "registry object has no attribute '{}'".format(key))

    def __repr__(self):
        return "{}(name='{}', items={})".format(self.__class__.__name__,
                                                self._name,
                                                list(self._items.keys()))

    def _register(self, obj, name=None):
        if name is None:
            name = obj.__name__
        if name in self._items:
            raise KeyError('{} is already registered in {}'.format(
                name, self._name))
        self._items[name] = obj
        return obj

    def register(self, obj=None, name=None):
        if isinstance(obj, (list, tuple)):
            assert name is None
            for o in obj:
                self._register(o, name=name)
            return

        if obj is not None:
            self._register(obj, name=name)
            return

        def _wrapper(obj):
            self._register(obj, name=name)
            return obj

        return _wrapper

    def get(self, key, default=None):
        return self._items.get(key, default)

    def pop(self, key):
        return self._items.pop(key)


def build_object(cfg, parent, default=None, **kwargs):
    """
    Initialize an object from a dict.

    The dict must contain a key ``type``, which is a indicating the object
    type. Remaining fields are treated as the arguments for constructing the
    object.

    Args:
        cfg (any): The object or object configs.
        parent (any): The module or a list of modules which may contain the
            expected object.
        default (any, optional): The default value when the object is not
            found. Default: ``None``.

    Returns:
        any: The constructed object.
    """
    if not hasattr(cfg, 'copy'):
        return cfg

    if isinstance(parent, (list, tuple)):
        for p in parent:
            obj = build_object(cfg, p, **kwargs)
            if obj != default:
                return obj
        return default

    _cfg = cfg.copy()
    _cfg.update(kwargs)
    obj_type = _cfg.pop('type')

    if hasattr(parent, 'get'):
        obj_cls = parent.get(obj_type)
    else:
        obj_cls = getattr(parent, obj_type, None)

    return obj_cls(**_cfg) if obj_cls is not None else default
