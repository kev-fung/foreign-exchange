"""If database was given we may set up db connection/struct tests here instead"""

import unittest
from fx_api import models


class TestModels(unittest.TestCase):
    def test_xrs(self):
        assert(isinstance(models.xrs, list))
        assert("country" in models.xrs[0])
        assert("rate" in models.xrs[0])
        assert("xrcode" in models.xrs[0])


if __name__ == "__main__":
    unittest.main()


