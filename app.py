from flask import Flask, request, jsonify, Response
import requests
import json
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

def clean_text_response(text):
    """Clean text response by removing _proxy block"""
    try:
        # Try to parse as JSON and remove _proxy
        data = json.loads(text)
        data = remove_proxy_field(data)
        return json.dumps(data, indent=2)
    except:
        # Remove _proxy from raw text
        lines = text.split('\n')
        cleaned_lines = []
        skip_proxy = False
        for line in lines:
            if '"_proxy"' in line or '_proxy' in line:
                skip_proxy = True
                continue
            if skip_proxy:
                if '}' in line and not '{' in line:
                    skip_proxy = False
                continue
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

@app.route('/api/vehicle')
def get_vehicle_info():
    vehicle = request.args.get('vehicle', '')
    
    if not vehicle:
        return jsonify({"error": "Vehicle number required"}), 400
    
    def generate():
        # API 1 - ummmym (slow response, 10-15 seconds)
        try:
            url1 = f"https://ummmym.onrender.com/?rc={vehicle}"
            resp1 = requests.get(url1, timeout=30)
            yield clean_text_response(resp1.text) + "\n\n"
        except Exception as e:
            yield f"API Error: {str(e)}\n\n"
        
        # API 2 - vehicleinfo
        try:
            url2 = f"https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number={vehicle}"
            resp2 = requests.get(url2, timeout=15)
            yield clean_text_response(resp2.text) + "\n\n"
        except Exception as e:
            yield f"API Error: {str(e)}\n\n"
        
        # API 3 - bronx
        try:
            url3 = f"https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle={vehicle}"
            resp3 = requests.get(url3, timeout=15)
            yield clean_text_response(resp3.text) + "\n\n"
        except Exception as e:
            yield f"API Error: {str(e)}\n\n"
        
        # API 4 - carhayhaha
        try:
            url4 = f"https://carhayhaha.onrender.com/api/vehicle?vehicle={vehicle}"
            resp4 = requests.get(url4, timeout=15)
            yield clean_text_response(resp4.text)
        except Exception as e:
            yield f"API Error: {str(e)}"
    
    return Response(generate(), mimetype='text/plain')

@app.route('/')
def home():
    return jsonify({
        "status": "API Running ✅",
        "usage": "/api/vehicle?vehicle=GJ06RG5545",
        "response": "All 4 APIs response one by one"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
