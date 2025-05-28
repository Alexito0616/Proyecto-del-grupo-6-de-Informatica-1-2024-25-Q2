import unittest
from navAirport import NavAirport  # Reemplaza 'your_module' con el nombre real del archivo si es necesario


class TestNavAirport(unittest.TestCase):


   def test_initialization(self):
       airport = NavAirport("LEMD", ["SID1", "SID2"], ["STAR1", "STAR2"])
       self.assertEqual(airport.name, "LEMD")
       self.assertEqual(airport.sids, ["SID1", "SID2"])
       self.assertEqual(airport.stars, ["STAR1", "STAR2"])


   def test_empty_lists(self):
       airport = NavAirport("LEBL", [], [])
       self.assertEqual(airport.sids, [])
       self.assertEqual(airport.stars, [])


   def test_repr(self):
       airport = NavAirport("EGLL", ["SID3"], ["STAR5"])
       expected_repr = "NavAirport(EGLL, SIDs=['SID3'], STARs=['STAR5'])"
       self.assertEqual(repr(airport), expected_repr)


if __name__ == "__main__":
   unittest.main()



