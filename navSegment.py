class NavSegment:
   def __init__(self, origin_id, dest_id, distance):
       self.origin_id = int(origin_id)
       self.dest_id = int(dest_id)
       self.distance = float(distance)


   def __repr__(self):
       return f"NavSegment({self.origin_id} -> {self.dest_id}, {self.distance} km)"
