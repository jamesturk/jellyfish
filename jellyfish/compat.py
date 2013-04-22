import sys
import itertools

IS_PY3 = sys.version_info[0] == 3

if IS_PY3:
    _range = range
    _unicode = str
    _zip_longest = itertools.zip_longest
else:
    _range = xrange
    _unicode = unicode
    _zip_longest = itertools.izip_longest
