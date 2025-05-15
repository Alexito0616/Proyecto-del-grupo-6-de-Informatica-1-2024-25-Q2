from navSegment import NavSegment
from navAirport import NavAirport
from navPoint import NavPoint








class AirSpace:
  def __init__(self):
      self.navpoints = {}      # ID -> NavPoint
      self.navsegments = []    # Lista de NavSegment
      self.airports = []       # Lista de NavAirport




  def load_from_files(self, nav_file, seg_file, aer_file):
      self._load_navpoints(nav_file)
      self._load_navsegments(seg_file)
      self._load_airports(aer_file)




  def _load_navpoints(self, filename):
      with open(filename) as f:
          for line in f:
              parts = line.strip().split()
              id = parts[0]
              name = parts[1]
              lat = parts[2]
              lon = parts[3]
              self.navpoints[int(id)] = NavPoint(id, name, lat, lon)




  def _load_navsegments(self, filename):
      with open(filename) as f:
          for line in f:
              origin, dest, dist = line.strip().split()
              segment = NavSegment(origin, dest, dist)
              self.navsegments.append(segment)
              self.navpoints[int(origin)].neighbors.append((int(dest), float(dist)))


  def _load_airports(self, filename):
      with open(filename) as f:
          for line in f:
              parts = line.strip().split()
              name = parts[0]
              sids = []
              stars = []
              section = 'SID'


              for item in parts[1:]:
                  if item.lower() == 'arrival':
                      section = 'STAR'
                      continue
                  navpoint_name = item.strip(',')  # puede ser nombre, no ID
                  # Buscar el ID a partir del nombre
                  matching = [np_id for np_id, np in self.navpoints.items() if np.name == navpoint_name]
                  if matching:
                      if section == 'SID':
                          sids.append(matching[0])
                      else:
                          stars.append(matching[0])
                  else:
                      print(f"[WARNING] Punto de navegación '{navpoint_name}' no encontrado para aeropuerto '{name}'")


              self.airports.append(NavAirport(name, sids, stars))


  def show_neighbors(self, point_id):
      point = self.navpoints[point_id]
      print(f"Vecinos de {point.name} ({point.id}):")
      for neighbor_id, dist in point.neighbors:
          neighbor = self.navpoints[neighbor_id]
          print(f"  -> {neighbor.name} ({neighbor.id}) a {dist} km")




  def shortest_path(self, start_id, end_id):
      import heapq
      distances = {id: float('inf') for id in self.navpoints}
      previous = {}
      distances[start_id] = 0
      queue = [(0, start_id)]




      while queue:
          current_dist, current_id = heapq.heappop(queue)




          if current_id == end_id:
              break




          for neighbor_id, dist in self.navpoints[current_id].neighbors:
              new_dist = current_dist + dist
              if new_dist < distances[neighbor_id]:
                  distances[neighbor_id] = new_dist
                  previous[neighbor_id] = current_id
                  heapq.heappush(queue, (new_dist, neighbor_id))




      # Reconstruir camino
      path = []
      current = end_id
      while current in previous:
          path.insert(0, current)
          current = previous[current]
      if path:
          path.insert(0, start_id)
      return path




  def get_closest(self, lon, lat):
      min_dist = float('inf')
      closest = None
      for navpoint in self.navpoints.values():
          dist = ((float(navpoint.lon) - lon) ** 2 + (float(navpoint.lat) - lat) ** 2) ** 0.5
          if dist < min_dist:
              min_dist = dist
              closest = navpoint
      return closest




  def get_neighbors(self, point_id):
      return [neighbor_id for neighbor_id, _ in self.navpoints[point_id].neighbors]



