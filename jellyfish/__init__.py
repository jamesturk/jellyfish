try:
    from .cjellyfish import *   # noqa
    from ._jellyfish import wagner_fischer_distance
except ImportError:
    from ._jellyfish import *   # noqa
