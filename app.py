from flask import Flask, request, jsonify, Response
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
import traceback

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# API URLs - SAFE STORAGE
API_LIST = {
    'api1': 'https://ummmym.onrender.com/?rc=',
    'api2': 'https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number=',
    'api3': 'https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle=',
    'api4': 'https://carhayhaha.onrender.com/api/vehicle?vehicle='
}

def deep_clean_data(obj):
    """Remove proxy, sensitive info, clean everything"""
    if isinstance(obj, dict):
        # Proxy fields remove
        keys_to_delete = ['_proxy', 'proxy', 'proxy_used', 'proxy_info', 'session_id', 'pool_size', 'total_fetched', 'tested', 'credit', 'note', 'device']
        for key in keys_to_delete:
            if key in obj:
                del obj[key]
        
        # Clean nested
        for key, value in obj.items():
            obj[key] = deep_clean_data(value)
    
    elif isinstance(obj, list):
        return [deep_clean_data(item) for item in obj]
    
    return obj

def safe_error_message():
    """Generic safe error messages - NO HOST/URL LEAK"""
    return {
        "status": "failed",
        "message": "Service temporarily unavailable",
        "retry": "Please try again in few seconds"
    }

def fetch_api_with_retry(api_key, url, vehicle, max_retries=2):
    """Fetch with retry logic - 100% better success rate"""
    
    full_url = f"{url}{vehicle}"
    
    for attempt in range(max_retries):
        try:
            # Longer timeout for slow free APIs
            response = requests.get(
                full_url,
                timeout=45,  # 45 seconds timeout
                verify=False,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                },
                allow_redirects=True
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    cleaned = deep_clean_data(data)
                    return api_key, {"success": True, "data": cleaned}
                except json.JSONDecodeError:
                    # Maybe HTML or text response
                    text_data = response.text[:5000]
                    return api_key, {"success": True, "raw_response": text_data}
            
            elif response.status_code == 503 or response.status_code == 502:
                # Server busy - retry
                time.sleep(2)
                continue
            else:
                return api_key, safe_error_message()
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return api_key, safe_error_message()
            
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return api_key, safe_error_message()
            
        except Exception:
            return api_key, safe_error_message()
    
    return api_key, safe_error_message()

@app.route('/api/vehicle')
def get_vehicle_info():
    """Main endpoint - FAST PARALLEL FETCHING"""
    
    vehicle = request.args.get('vehicle', '')
    
    if not vehicle:
        return jsonify({
            "error": True,
            "message": "Vehicle number required",
            "example": "/api/vehicle?vehicle=GJ06RG5545"
        }), 400
    
    vehicle = vehicle.strip().upper().replace(' ', '')
    
    # Parallel fetching with ThreadPoolExecutor
    results = {}
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Submit all tasks
        future_to_api = {
            executor.submit(fetch_api_with_retry, api_key, url, vehicle): api_key
            for api_key, url in API_LIST.items()
        }
        
        # Collect as they complete
        for future in as_completed(future_to_api):
            api_key = future_to_api[future]
            try:
                key, data = future.result(timeout=60)
                results[key] = data
            except Exception:
                results[api_key] = safe_error_message()
    
    # Build final response
    successful = sum(1 for r in results.values() if r.get('success'))
    
    final = {
        "status": True,
        "vehicle_number": vehicle,
        "total_sources": len(API_LIST),
        "successful_sources": successful,
        "response_time": f"{time.time() - start_time:.2f}s",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "results": results
    }
    
    return Response(
        json.dumps(final, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8',
        headers={
            'X-Content-Type-Options': 'nosniff',
            'Access-Control-Allow-Origin': '*'
        }
    )

@app.route('/')
def index():
    return jsonify({
        "service": "Vehicle Information API",
        "status": "Operational",
        "usage": "/api/vehicle?vehicle=VEHICLE_NUMBER",
        "example": "/api/vehicle?vehicle=GJ06RG5545",
        "features": [
            "Multi-source data",
            "No proxy/host leaks",
            "Parallel fetching",
            "Auto retry on failure"
        ]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime": "running"})

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
