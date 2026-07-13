from flask import Flask, request, jsonify, Response
import requests
import json
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def remove_proxy_field(data):
    """Remove _proxy field from response"""
    if isinstance(data, dict):
        if '_proxy' in data:
            del data['_proxy']
        for key, value in data.items():
            if isinstance(value, dict):
                remove_proxy_field(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        remove_proxy_field(item)
    return data

def clean_response(response_text):
    """Clean response by removing _proxy block"""
    try:
        data = json.loads(response_text)
        data = remove_proxy_field(data)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except:
        # If not JSON, remove _proxy from text
        if '"_proxy"' in response_text:
            import re
            response_text = re.sub(r',?\s*"_proxy"\s*:\s*\{[^}]*\}', '', response_text)
        return response_text

def fetch_with_retry(url, max_retries=2, timeout=60):
    """Fetch URL with retry logic"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    
    for attempt in range(max_retries):
        try:
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=timeout, verify=False)
            return response.text
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return "Timeout: Server response time exceeded"
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return "Connection Error: Server not reachable"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Error: Max retries exceeded"

@app.route('/api/vehicle')
def get_vehicle_info():
    vehicle = request.args.get('vehicle', '')
    
    if not vehicle:
        return jsonify({"error": "Vehicle number required"}), 400
    
    def generate():
        # API 1 - ummmym (with 60s timeout and retries)
        url1 = f"https://ummmym.onrender.com/?rc={vehicle}"
        resp1 = fetch_with_retry(url1, max_retries=2, timeout=60)
        yield clean_response(resp1)
        yield "\n---\n\n"
        
        # API 2 - vehicleinfo
        url2 = f"https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number={vehicle}"
        resp2 = fetch_with_retry(url2, max_retries=2, timeout=30)
        yield clean_response(resp2)
        yield "\n---\n\n"
        
        # API 3 - bronx
        url3 = f"https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle={vehicle}"
        resp3 = fetch_with_retry(url3, max_retries=2, timeout=30)
        yield clean_response(resp3)
        yield "\n---\n\n"
        
        # API 4 - carhayhaha
        url4 = f"https://carhayhaha.onrender.com/api/vehicle?vehicle={vehicle}"
        resp4 = fetch_with_retry(url4, max_retries=2, timeout=30)
        yield clean_response(resp4)
    
    return Response(generate(), mimetype='text/plain; charset=utf-8')

@app.route('/')
def home():
    return jsonify({
        "status": "API Running ✅",
        "usage": "/api/vehicle?vehicle=GJ06RG5545",
        "timeout": "60s for slow APIs"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
