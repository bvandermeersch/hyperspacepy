import unittest
from hyperspacepy import Hyperspace

class HyperspaceTest(unittest.TestCase):
    def test_get_version(self):
        hyperspace = Hyperspace()
        self.assertEqual(hyperspace.get_version(), '1.0.4')

if __name__ == '__main__':
    unittest.main()
