import unittest
from navSegment import NavSegment


class TestNavSegment(unittest.TestCase):
   def test_creation(self):
       seg = NavSegment(6063, 6062, 40.879793)
       self.assertEqual(seg.origin_number, 6063)
       self.assertEqual(seg.destination_number, 6062)
       self.assertAlmostEqual(seg.distance, 40.879793)


if __name__ == "__main__":
   unittest.main()
