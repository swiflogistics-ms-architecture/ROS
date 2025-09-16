## Route Optimisation System (ROS) API

### POST /optimize

Accepts:

- `srcAddress`: Source address (string)
- `addresses`: List of destination addresses (array of strings)
- `vehicles`: List of available vehicles (array of strings)

Returns:

- `routes`: For each vehicle, returns a sequenced route covering all addresses, starting from the source address and visiting each destination in the nearest-neighbor order.

---

### Running the Flask Server

1. Make sure you have Python, Flask, requests, polyline, and python-dotenv installed in your environment.
2. Set your Google Maps API key in a `.env` file:
   ```
   GOOGLE_MAPS_API_KEY=your_actual_api_key
   ```
3. Start the Flask server:
   ```bash
   python app.py
   ```
   The server will run at `http://127.0.0.1:5000/` by default.

### Testing the API

You can test the `/optimize` endpoint using `curl`:

```bash
curl -X POST http://127.0.0.1:5000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "srcAddress": "1600 Amphitheatre Parkway, Mountain View, CA",
    "addresses": [
      "1 Infinite Loop, Cupertino, CA",
      "500 Terry A Francois Blvd, San Francisco, CA"
    ],
    "vehicles": ["Truck 1", "Truck 2"]
  }'
```

Or use Postman to send a POST request with the same JSON body.

#### Example request (JSON):

```json
{
  "srcAddress": "1600 Amphitheatre Parkway, Mountain View, CA",
  "addresses": [
    "1 Infinite Loop, Cupertino, CA",
    "500 Terry A Francois Blvd, San Francisco, CA"
  ],
  "vehicles": ["Truck 1", "Truck 2"]
}
```

#### Example response:

```json
{
  "routes": [
    {
      "vehicle": "Truck 1",
      "route": [
        "1600 Amphitheatre Parkway, Mountain View, CA",
        "1 Infinite Loop, Cupertino, CA"
      ]
    },
    {
      "vehicle": "Truck 2",
      "route": [
        "1600 Amphitheatre Parkway, Mountain View, CA",
        "500 Terry A Francois Blvd, San Francisco, CA"
      ]
    }
  ]
}
```

---

### Using the JavaScript Adapter

You can interact with the Flask API from a Node.js or JavaScript project using an adapter function. This adapter sends a POST request to the `/optimize` endpoint and returns the optimized routes.

**How it works:**

1. The adapter function (e.g., `optimizeRoutes`) takes the source address, destination addresses, and vehicles as arguments.
2. It sends these as a JSON POST request to the Flask server's `/optimize` endpoint using `axios`.
3. The Flask server processes the request and returns the optimized routes.
4. The adapter receives the response and returns it to your JavaScript code for further use.

**Example usage:**

```js
const { optimizeRoutes } = require("./rosAdapter");

// srcAddress, addresses, vehicles
optimizeRoutes(
  "1600 Amphitheatre Parkway, Mountain View, CA", // srcAddress
  [
    "1 Infinite Loop, Cupertino, CA", // address
    "500 Terry A Francois Blvd, San Francisco, CA", // address
  ], // addresses
  ["Truck 1", "Truck 2"] // vehicles
).then((data) => console.log(JSON.stringify(data, null, 2)));
```

This will print the optimized routes to your console. Make sure your Flask server is running before calling the adapter.
