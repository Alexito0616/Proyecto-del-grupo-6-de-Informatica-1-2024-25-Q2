import unittest
from navPoint import NavPoint
from navAirport import NavAirport


class TestNavAirport(unittest.TestCase):
   def test_add_sid_and_star(self):
       airport = NavAirport("LEIB")
       sid = NavPoint(6062, "IZA.A", 38.87, 1.36)
       star = NavPoint(6063, "ZDA.B", 38.87, 1.74)


       airport.add_sid(sid)
       airport.add_star(star)


       self.assertEqual(len(airport.sids), 1)
       self.assertEqual(len(airport.stars), 1)
       self.assertEqual(airport.sids[0].name, "IZA.A")
       self.assertEqual(airport.stars[0].name, "ZDA.B")


if __name__ == "__main__":
   unittest.main()
