try:
    from ._cjellyfish import *   # noqa
    library = "C"

except ImportError:
    from ._jellyfish import *   # noqa
    library = "Python"
