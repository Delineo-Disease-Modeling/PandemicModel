import unittest
import simulation as master

class MasterTester(unittest.TestCase):
    def test_master(self):
        print("Testing master.py")
        master.runTest()


if __name__ == '__main__':
    unittest.main()
