# Use unittest2 for older versions of Python
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# Use thirdt party ordereddict for older versions of Python
try:
    from collections import OrderedDict
except ImportError:
    import OrderedDict

# Use standard unittest.mock if possible. (mock doesn't support Python 3.4)
try:
    from unittest import mock
except ImportError:
    import mock

try:
    from aliyunsdkcore import client
except ImportError:
    import client
