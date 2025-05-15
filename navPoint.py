class NavPoint:
   def __init__(self, id, name, lat, lon):
       self.id = int(id)
       self.name = name
       self.lat = float(lat)
       self.lon = float(lon)
       self.neighbors = []  # Lista de tuplas (id_vecino, distancia)


   def __repr__(self):
       return f"NavPoint({self.id}, {self.name}, {self.lat}, {self.lon})"
