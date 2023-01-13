import unittest
from delineo import master


class MasterTester(unittest.TestCase):
    def test_master(self):
        print("Testing master.py")
        print("Testing functions:")
        master.runTest()


if __name__ == '__main__':
    unittest.main()
