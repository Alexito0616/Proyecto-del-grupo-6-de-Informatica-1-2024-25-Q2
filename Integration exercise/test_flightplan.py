# test_flightplan.py

from flightplan import Flightplan, Addwaypoint, Showflightplan

# Create a FlightPlan object with the name 'myPlan'
myPlan = Flightplan("myPlan")

# Add the 4 waypoints (I'm inventing example waypoints since you mentioned a "previous table" but didn't paste it)
Addwaypoint(myPlan,"New York")
Addwaypoint(myPlan,"London")
Addwaypoint(myPlan,"Paris")
Addwaypoint(myPlan,"Rome")

# Show the flight plan
Showflightplan(myPlan)