import unittest
import tempfile
import os


from Airspace import AirSpace


# Mocks de las clases externas sin modificar nada del código original
class NavPoint:
   def __init__(self, number, name, lat, lon):
       self.number = number
       self.name = name
       self.latitude = lat
       self.longitude = lon
       self.neighbors = []


class NavSegment:
   def __init__(self, origin, dest, dist):
       self.origin = origin
       self.dest = dest
       self.dist = dist


class NavAirport:
   def __init__(self, name, sids, stars):
       self.name = name
       self.sids = sids
       self.stars = stars


class TestAirSpace(unittest.TestCase):


   def setUp(self):
       self.airspace = AirSpace()
       # Patch the actual classes
       import sys
       sys.modules['navPoint'] = sys.modules[__name__]
       sys.modules['navSegment'] = sys.modules[__name__]
       sys.modules['navAirport'] = sys.modules[__name__]


   def create_temp_file(self, content: str):
       tmp = tempfile.NamedTemporaryFile(delete=False, mode='w+t')
       tmp.write(content)
       tmp.close()
       return tmp.name


   def tearDown(self):
       # Limpia archivos temporales si se usan
       pass


   def test_load_navpoints(self):
       content = "1 WP1 40.0 -3.5\n2 WP2 41.0 -3.6\n"
       nav_file = self.create_temp_file(content)
       self.airspace.load_navpoints(nav_file)
       os.unlink(nav_file)


       self.assertEqual(len(self.airspace.navpoints), 2)
       self.assertEqual(self.airspace.navpoints[1].name, "WP1")


   def test_load_navsegments(self):
       nav_content = "1 WP1 40.0 -3.5\n2 WP2 41.0 -3.6\n"
       seg_content = "1 2 50.0\n"


       nav_file = self.create_temp_file(nav_content)
       seg_file = self.create_temp_file(seg_content)


       self.airspace.load_navpoints(nav_file)
       self.airspace.load_navsegments(seg_file)


       os.unlink(nav_file)
       os.unlink(seg_file)


       self.assertEqual(len(self.airspace.navsegments), 1)
       self.assertEqual(self.airspace.navpoints[1].neighbors, [(2, 50.0)])


   def test_load_airports(self):
       nav_content = "1 SID1.D 40.0 -3.5\n2 STAR1.A 41.0 -3.6\n"
       airport_content = "LEMD\nSID1.D\nSTAR1.A\n"


       nav_file = self.create_temp_file(nav_content)
       airport_file = self.create_temp_file(airport_content)


       self.airspace.load_navpoints(nav_file)
       self.airspace.load_airports(airport_file)


       os.unlink(nav_file)
       os.unlink(airport_file)


       self.assertEqual(len(self.airspace.navairports), 1)
       self.assertEqual(self.airspace.navairports[0].name, "LEMD")
       self.assertEqual(self.airspace.navairports[0].sids[0].name, "SID1.D")
       self.assertEqual(self.airspace.navairports[0].stars[0].name, "STAR1.A")


   def test_get_neighbors(self):
       nav_content = "1 WP1 40.0 -3.5\n2 WP2 41.0 -3.6\n"
       seg_content = "1 2 50.0\n"


       nav_file = self.create_temp_file(nav_content)
       seg_file = self.create_temp_file(seg_content)


       self.airspace.load_navpoints(nav_file)
       self.airspace.load_navsegments(seg_file)


       os.unlink(nav_file)
       os.unlink(seg_file)


       neighbors = self.airspace.get_neighbors(1)
       self.assertEqual(neighbors, [2])




if __name__ == "__main__":
   unittest.main()



