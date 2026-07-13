from flask import Flask, request, jsonify
import requests
import concurrent.futures
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def remove_proxy_field(data):
    """Remove _proxy field if exists"""
    if isinstance(data, dict):
        if '_proxy' in data:
            del data['_proxy']
        # Also remove from nested structures
        for key, value in data.items():
            if isinstance(value, dict):
                remove_proxy_field(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        remove_proxy_field(item)
    return data

def fetch_vehicle_data(url):
    """Fetch vehicle data from given URL"""
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            try:
                data = response.json()
                data = remove_proxy_field(data)
                return data
            except:
                return response.text
        return None
    except:
        return None

@app.route('/api/vehicle')
def get_vehicle_info():
    vehicle = request.args.get('vehicle', '')
    
    if not vehicle:
        return jsonify({"error": "Vehicle number required"}), 400
    
    urls = [
        f"https://ummmym.onrender.com/?rc={vehicle}",
        f"https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number={vehicle}",
        f"https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle={vehicle}",
        f"https://carhayhaha.onrender.com/api/vehicle?vehicle={vehicle}"
    ]
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(fetch_vehicle_data, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                if isinstance(result, list):
                    results.extend(result)
                elif isinstance(result, dict):
                    results.append(result)
    
    # Merge all results into single clean response
    final_response = {}
    
    for item in results:
        if isinstance(item, dict):
            for key, value in item.items():
                if key != '_proxy':
                    if key in final_response:
                        if isinstance(final_response[key], list):
                            if isinstance(value, list):
                                final_response[key].extend(value)
                            else:
                                final_response[key].append(value)
                        else:
                            if isinstance(value, list):
                                final_response[key] = [final_response[key]] + value
                            else:
                                final_response[key] = [final_response[key], value]
                    else:
                        final_response[key] = value
    
    return jsonify(final_response)

@app.route('/')
def home():
    return jsonify({"status": "API Running", "usage": "/api/vehicle?vehicle=VEHICLE_NUMBER"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
