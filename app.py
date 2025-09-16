from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import polyline

app = Flask(__name__)

load_dotenv()
GoogleMapsAPIKey = os.getenv("GOOGLE_MAPS_API_KEY")

def get_next_nearest_address(api_key, origin, destinations):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": "|".join(destinations),
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "OK":
        distances = data["rows"][0]["elements"]
        min_distance = float('inf')
        nearest_address = None
        for i, element in enumerate(distances):
            if element["status"] == "OK":
                distance_value = element["distance"]["value"]
                if distance_value < min_distance:
                    min_distance = distance_value
                    nearest_address = destinations[i]
        return nearest_address
    else:
        return None
    


@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    srcAddress = data.get('srcAddress', '')
    addresses = data.get('addresses', [])
    vehicles = data.get('vehicles', [])

    # Split addresses evenly among vehicles
    from math import ceil
    num_vehicles = len(vehicles)
    result = []
    if num_vehicles == 0:
        return jsonify({"routes": [{"vehicle": "Unassigned", "route": addresses}]})

    chunk_size = ceil(len(addresses) / num_vehicles)
    for i, vehicle in enumerate(vehicles):
        # Get the chunk of addresses for this vehicle
        start = i * chunk_size
        end = start + chunk_size
        vehicle_addresses = addresses[start:end]
        route = [srcAddress]
        current_location = srcAddress
        remaining = vehicle_addresses.copy()
        while remaining:
            next_address = get_next_nearest_address(GoogleMapsAPIKey, current_location, remaining)
            if next_address:
                route.append(next_address)
                remaining.remove(next_address)
                current_location = next_address
            else:
                break
        if len(route) > 1:
            result.append({"vehicle": vehicle, "route": route})

    return jsonify({"routes": result})


if __name__ == '__main__':
    app.run(debug=True)
  