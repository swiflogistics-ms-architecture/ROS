from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import polyline

app = Flask(__name__)

load_dotenv()
GoogleMapsAPIKey = os.getenv("GOOGLE_MAPS_API_KEY")

    
def get_shortest_path(api_key, origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "OK":
        route = data["routes"][0]["legs"][0]
        distance = route["distance"]["text"]
        duration = route["duration"]["text"]
        
        polyline_str = route["steps"][0]["polyline"]["points"]
        coordinates = polyline.decode(polyline_str)
        return {
            "distance": distance,
            "duration": duration,
            "coordinates": coordinates
        }
    else:
        return {"error": data["status"]
}

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    srcAddress = data.get('srcAddress', '')
    addresses = data.get('addresses', [])
    vehicles = data.get('vehicles', [])
    optimized_routes = []
    for address in addresses:
        optimized_route = get_shortest_path(GoogleMapsAPIKey, srcAddress, address)
        optimized_routes.append(optimized_route)

    # Assign routes to vehicles (grouped per vehicle)
    from collections import defaultdict
    assignedRoutes = defaultdict(list)
    num_vehicles = len(vehicles)
    for i, optimized_route in enumerate(optimized_routes):
        if num_vehicles > 0:
            vehicle = vehicles[i % num_vehicles]
            assignedRoutes[vehicle].append(optimized_route)
        else:
            # No vehicles available
            assignedRoutes["All vehicles are currently occupied"].append(optimized_route)

    # Format result as list of dicts
    result = [{"vehicle": v, "routes": r} for v, r in assignedRoutes.items()]
    return jsonify({"routes": result})

if __name__ == '__main__':
    app.run(debug=True)
  