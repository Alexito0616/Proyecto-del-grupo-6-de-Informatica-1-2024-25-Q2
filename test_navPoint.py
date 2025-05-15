import unittest
from navPoint import NavPoint


class TestNavPoint(unittest.TestCase):
   def test_creation(self):
       np = NavPoint(6062, "IZA.A", 38.877280483, 1.3690495)
       self.assertEqual(np.number, 6062)
       self.assertEqual(np.name, "IZA.A")
       self.assertAlmostEqual(np.latitude, 38.877280483)
       self.assertAlmostEqual(np.longitude, 1.3690495)


if __name__ == "__main__":
   unittest.main()
