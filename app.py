from flask import Flask, request, jsonify, Response
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor
import urllib3

# Disable SSL warnings for faster requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# API Configuration - Saari APIs
API_LIST = {
    'api1_ummmym': 'https://ummmym.onrender.com/?rc=',
    'api2_vehicleinfo': 'https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number=',
    'api3_bronx': 'https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle=',
    'api4_carhayhaha': 'https://carhayhaha.onrender.com/api/vehicle?vehicle='
}

def clean_data(data):
    """Proxy info hatane ka function"""
    if isinstance(data, dict):
        # _proxy field ko hatao
        if '_proxy' in data:
            del data['_proxy']
        
        # Deep clean for nested data
        for key in list(data.keys()):
            if isinstance(data[key], (dict, list)):
                data[key] = clean_data(data[key])
    
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], (dict, list)):
                data[i] = clean_data(data[i])
    
    return data

def fetch_single_api(api_name, url, vehicle):
    """Single API se data fetch karo - FAST"""
    try:
        full_url = f"{url}{vehicle}"
        
        # Quick request with timeout
        response = requests.get(
            full_url, 
            timeout=15,  # 15 sec timeout
            verify=False,  # SSL skip for speed
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            }
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                return api_name, clean_data(data)
            except:
                return api_name, {"raw_text": response.text[:1000]}
        else:
            return api_name, {"error": f"Status: {response.status_code}"}
            
    except Exception as e:
        return api_name, {"error": str(e)[:200]}

@app.route('/api/vehicle')
def get_all_vehicle_data():
    """SARAA DATA EK SAATH - PARALLEL FETCHING"""
    
    vehicle = request.args.get('vehicle', '').strip().upper()
    
    if not vehicle:
        return jsonify({
            "error": "❌ Vehicle number daalo!",
            "example": "/api/vehicle?vehicle=GJ06RG5545"
        }), 400
    
    # PARALLEL FETCHING - Saari APIs ek saath call hongi
    results = {}
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for api_name, url in API_LIST.items():
            future = executor.submit(fetch_single_api, api_name, url, vehicle)
            futures.append(future)
        
        # Results collect karo jaise hi aaye
        for future in futures:
            try:
                api_name, data = future.result(timeout=20)
                results[api_name] = data
            except:
                results[api_name] = {"error": "Timeout ya failed"}
    
    # Final clean response - NO PROXY INFO
    final_response = {
        "vehicle": vehicle,
        "success": True,
        "total_apis": len(API_LIST),
        "fetched": len([r for r in results.values() if "error" not in str(r).lower()]),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data": results
    }
    
    # JSON response with proper encoding
    return Response(
        json.dumps(final_response, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8'
    )

@app.route('/')
def home():
    """Welcome page"""
    return jsonify({
        "🚗": "Unified Vehicle API",
        "creator": "Made with ❤️",
        "usage": "/api/vehicle?vehicle=NUMBER",
        "test": "/api/vehicle?vehicle=GJ06RG5545",
        "apis": ["ummmym", "vehicleinfo", "bronx", "carhayhaha"],
        "feature": "✅ NO PROXY INFO IN RESPONSE",
        "speed": "⚡ Parallel fetching - Fast response"
    })

# Health check - Render ke liye zaroori
@app.route('/health')
def health():
    return jsonify({"status": "✅ Alive!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
