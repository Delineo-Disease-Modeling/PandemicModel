import unittest
import simulation as master
from inspect import getmembers, isfunction


class MasterTester(unittest.TestCase):
    def test_master(self):
        print("Testing master.py")
        print(getmembers(master, isfunction))
        print(dir(master))


if __name__ == '__main__':
    unittest.main()
