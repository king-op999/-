# ============================================
# 🚗 BRONX ALL-IN-ONE VEHICLE API
# 4 APIs Combined • Raw Response • 60s Timeout
# ============================================
from flask import Flask, request, jsonify
import requests
import time
import os
import urllib3
urllib3.disable_warnings()

app = Flask(__name__)

API_91WHEELS = "https://ummmym.onrender.com"
API_VEHICLEINFO = "https://vehicleinfo.noobgamingv40.workers.dev/fetch"
API_VEH2NUM = "https://bronx-web-api.onrender.com/api/key-bronx/veh2num"
API_CARHAYHAHA = "https://carhayhaha.onrender.com/api/vehicle"

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🚗 BRONX ALL-IN-ONE</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000510;color:#d0d8f0;font-family:Arial,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.card{background:rgba(5,15,35,.95);border:2px solid rgba(0,255,136,.3);border-radius:24px;padding:30px;max-width:700px;width:100%;text-align:center}
h1{font-size:24px;background:linear-gradient(90deg,#00ff88,#0096ff,#8b00ff,#ff0080);background-size:300% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:rainbow 3s linear infinite}
@keyframes rainbow{0%{background-position:0% 50%}100%{background-position:300% 50%}}
.subtitle{color:#555;font-size:10px;letter-spacing:2px;margin:5px 0 12px}
.badges{display:flex;justify-content:center;flex-wrap:wrap;gap:5px;margin:8px 0}
.badge{display:inline-block;padding:4px 10px;border-radius:20px;font-size:8px;font-weight:700;background:rgba(0,255,136,.1);color:#00ff88;border:1px solid rgba(0,255,136,.3)}
code{color:#ffb400;font-family:monospace;font-size:10px;display:block;margin:8px 0;background:rgba(0,0,0,.4);padding:10px;border-radius:8px;word-break:break-all}
input{width:100%;padding:12px;background:rgba(0,0,0,.6);border:2px solid rgba(0,255,136,.2);border-radius:12px;color:#fff;font-size:14px;outline:none;margin:5px 0}
input:focus{border-color:#00ff88}
button{width:100%;padding:14px;background:linear-gradient(135deg,#00ff88,#0096ff,#8b00ff);color:#fff;border:none;border-radius:12px;font-weight:900;cursor:pointer;font-size:14px;margin:6px 0}
button:hover{transform:scale(1.02)}
.result{background:rgba(0,0,0,.6);border:1px solid rgba(0,255,136,.1);border-radius:12px;padding:14px;margin-top:10px;text-align:left;display:none;max-height:500px;overflow:auto}
.result.show{display:block}
pre{color:#00ff88;font-family:monospace;font-size:10px;white-space:pre-wrap}
footer{color:#333;font-size:9px;margin-top:12px}
</style></head>
<body>
<div class="card">
<h1>🚗 BRONX ALL-IN-ONE</h1>
<p class="subtitle">4 APIs • Raw Response • 60s Timeout</p>
<div class="badges">
<span class="badge">📱 91Wheels</span>
<span class="badge">🌐 VehicleInfo</span>
<span class="badge">📞 Veh2Num</span>
<span class="badge">🚗 CarHay</span>
</div>
<code>GET /api/vehicle?vehicle=GJ06RG5545</code>
<input type="text" id="rcInput" placeholder="Enter Vehicle Number..." autocomplete="off">
<button onclick="fetchData()">🔍 FETCH ALL DATA</button>
<div class="result" id="result"><pre id="data"></pre></div>
<footer>@BRONX_ULTRA</footer>
</div>
<script>
async function fetchData(){
var n=document.getElementById('rcInput').value.trim();
if(!n)return;
var r=document.getElementById('result'),d=document.getElementById('data');
r.classList.add('show');d.style.color='#ffb400';d.textContent='⏳ Fetching from 4 APIs (may take 15-30s)...';
try{
var resp=await fetch('/api/vehicle?vehicle='+encodeURIComponent(n));
var json=await resp.json();
d.style.color='#00ff88';d.textContent=JSON.stringify(json,null,2);
}catch(e){
d.style.color='#ff0080';d.textContent='Error: '+e.message;
}
}
</script>
</body></html>'''

def clean_response(data):
    """Remove _proxy from response"""
    if isinstance(data, dict):
        if '_proxy' in data:
            del data['_proxy']
        # Also clean nested
        for key in list(data.keys()):
            if key.startswith('_proxy') or key == 'credit' or key == 'powered_by':
                del data[key]
    return data

def fetch_api(url, timeout=60):
    """Fetch API with long timeout"""
    try:
        resp = requests.get(url, timeout=timeout, verify=False)
        try:
            data = resp.json()
            return clean_response(data)
        except:
            return resp.text[:10000]
    except requests.exceptions.Timeout:
        return {"error": "Timeout - API took too long"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API"}
    except Exception as e:
        return {"error": str(e)[:200]}

@app.route('/api/vehicle')
def all_in_one():
    vehicle = request.args.get('vehicle', '').strip().upper().replace(' ', '').replace('-', '')
    
    if not vehicle:
        return jsonify({"status": "error", "message": "Missing vehicle number"}), 400
    
    result = {
        "status": "success",
        "vehicle_number": vehicle,
    }
    
    # API 1: 91Wheels (15-20 sec timeout for proxy)
    result["bronx"] = fetch_api(f"{API_91WHEELS}/?rc={vehicle}", timeout=30)
    
    # API 2: VehicleInfo Worker
    result["vehicleinfo"] = fetch_api(f"{API_VEHICLEINFO}?vehicle_number={vehicle}", timeout=20)
    
    # API 3: Veh2Num Mobile
    result["veh2num_mobile"] = fetch_api(f"{API_VEH2NUM}?key=op&vehicle={vehicle}", timeout=20)
    
    # API 4: CarHayHaha
    result["info"] = fetch_api(f"{API_CARHAYHAHA}?vehicle={vehicle}", timeout=20)
    
    result["credit"] = "@BRONX_ULTRA"
    
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "ONLINE"})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "api": "/api/vehicle?vehicle=GJ06RG5545"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"🚗 ALL-IN-ONE API :{port}")
    app.run(host='0.0.0.0', port=port)
