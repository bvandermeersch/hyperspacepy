import unittest
from hyperspace import Hyperspace

class HyperspaceTest(unittest.TestCase):
    def test_get_version(self):
        hyperspace = Hyperspace()
        self.assertEqual(hyperspace.get_version(), '0.2.0')

if __name__ == '__main__':
    unittest.main()
