## Route Optimisation System (ROS) API

### POST /optimize

Accepts:

- `srcAddress`: Source address (string)
- `addresses`: List of destination addresses (array of strings)
- `vehicles`: List of available vehicles (array of strings)

Returns:

- `routes`: For each vehicle, returns a list of route objects. Each route object contains the shortest path (coordinates), distance, and duration for a destination address.

#### Example request (JSON):

{
"srcAddress": "1600 Amphitheatre Parkway, Mountain View, CA",
"addresses": [
"1 Infinite Loop, Cupertino, CA",
"500 Terry A Francois Blvd, San Francisco, CA"
],
"vehicles": ["Truck 1", "Truck 2"]
}

#### Example response:

{
"routes": [
{
"vehicle": "Truck 1",
"routes": [
{
"coordinates": [
[37.4224764, -122.0842499],
[37.33182, -122.03118],
[37.770715, -122.38718]
],
"distance": "9.4 mi",
"duration": "13 mins"
},
{
"coordinates": [
[37.4224764, -122.0842499],
[37.33182, -122.03118],
[37.770715, -122.38718]
],
"distance": "45.2 mi",
"duration": "1 hr 2 mins"
}
]
},
{
"vehicle": "Truck 2",
"routes": [
{
"coordinates": [
[37.4224764, -122.0842499],
[37.33182, -122.03118],
[37.770715, -122.38718]
],
"distance": "9.4 mi",
"duration": "13 mins"
},
{
"coordinates": [
[37.4224764, -122.0842499],
[37.33182, -122.03118],
[37.770715, -122.38718]
],
"distance": "45.2 mi",
"duration": "1 hr 2 mins"
}
]
}
]
}
