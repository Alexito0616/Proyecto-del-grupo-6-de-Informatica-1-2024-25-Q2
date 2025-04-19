class Flightplan:
    def __init__(self):
        self.name = ""
        self.waypoints = []

def Addwaypoint(flightplan,waypoint)
                
    flightplan.waypoints.append(waypoint)

def Showflightplan(flightplan):
    print(f"Flight Plan Name: {flightplan.name}")
    print("Waypoints:")
    for index, waypoint in enumerate(flightplan.waypoints, start=1):
        print(f"  {index}. {waypoint}")


