import unittest
from simulation.master import MasterController as sim


class MasterTester(unittest.TestCase):
    def test_master(self):
        mc = sim()  # Instantiate a MasterController
        mc.Anytown(print_infection_breakdown=False,
                   num_days=2, intervention_list={}, visitMatrix=r'sim\src\simulation\data\Anytown_Jan06_fullweek_dict.pkl')


if __name__ == '__main__':
    unittest.main()
