from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport


class AirSpace:
   def __init__(self):
       self.navpoints = {}     # key: number, value: NavPoint
       self.navsegments = []   # List of NavSegment
       self.navairports = []   # List of NavAirport

   #Cargar todos los nodos
   def load_navpoints(self, filename: str):
       with open(filename, 'r') as f:
           for line in f:
               parts = line.strip().split()
               number = int(parts[0])
               name = parts[1]
               latitude = float(parts[2])
               longitude = float(parts[3])
               self.navpoints[number] = NavPoint(number, name, latitude, longitude)
               self.navpoints[number].neighbors = []  # Inicializa la lista de vecinos

   #Cargar los segmentos
   def load_navsegments(self, filename: str):
       with open(filename, 'r') as f:
           for line in f:
               parts = line.strip().split()
               origin = int(parts[0])
               dest = int(parts[1])
               dist = float(parts[2])
               self.navsegments.append(NavSegment(origin, dest, dist))
               self.navpoints[origin].neighbors.append((dest, dist))  # Añadir vecino

   #Cargar los aeropuertos
   def load_airports(self, filename: str):
       with open(filename, 'r') as f:
           lines = [line.strip() for line in f if line.strip()]
           i = 0
           while i < len(lines):
               name = lines[i]
               sids = []
               i += 1
               while i < len(lines) and lines[i].endswith(".D"):
                   sid = self._find_navpoint_by_name(lines[i])
                   if sid:
                       sids.append(sid)
                   i += 1
               stars = []
               while i < len(lines) and lines[i].endswith(".A"):
                   star = self._find_navpoint_by_name(lines[i])
                   if star:
                       stars.append(star)
                   i += 1
               self.navairports.append(NavAirport(name, sids, stars))

   #Buscar un nodo por su nombre
   def _find_navpoint_by_name(self, name: str):
       for navpoint in self.navpoints.values():
           if navpoint.name == name:
               return navpoint
       return None

   #Abrir los ficheros de seg,aer,nav
   def load_from_files(self, nav_file, seg_file, aer_file):
       self.load_navpoints(nav_file)
       self.load_navsegments(seg_file)
       self.load_airports(aer_file)

   #Encontrar los vecinos
   def get_neighbors(self, point_id):
       return [neighbor_id for neighbor_id, _ in self.navpoints[point_id].neighbors]
