from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"api": "/api/vehicle?vehicle=MH02FZ0555", "status": "online"})

@app.route('/api/vehicle')
def get_vehicle():
    vehicle = request.args.get('vehicle', '')
    
    if not vehicle:
        return jsonify({"error": "Missing vehicle number"})
    
    result = {"vehicle_number": vehicle}
    
    # API 1: 91Wheels
    try:
        r1 = requests.get(f"https://ummmym.onrender.com/?rc={vehicle}", timeout=30)
        data1 = r1.json()
        if '_proxy' in data1:
            del data1['_proxy']
        result["91wheels"] = data1
    except Exception as e:
        result["91wheels"] = {"error": str(e)}

    # API 2: VehicleInfo
    try:
        r2 = requests.get(f"https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number={vehicle}", timeout=15)
        result["vehicleinfo"] = r2.json()
    except Exception as e:
        result["vehicleinfo"] = {"error": str(e)}

    # API 3: Veh2Num
    try:
        r3 = requests.get(f"https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle={vehicle}", timeout=15)
        result["veh2num_mobile"] = r3.json()
    except Exception as e:
        result["veh2num_mobile"] = {"error": str(e)}

    # API 4: CarHayHaha
    try:
        r4 = requests.get(f"https://carhayhaha.onrender.com/api/vehicle?vehicle={vehicle}", timeout=15)
        result["carhayhaha"] = r4.json()
    except Exception as e:
        result["carhayhaha"] = {"error": str(e)}

    result["credit"] = "@BRONX_ULTRA"
    
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
