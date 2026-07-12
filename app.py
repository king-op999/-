# ============================================
# 🚗 BRONX ALL-IN-ONE VEHICLE API
# 4 APIs Raw Response • No Modification • Clean
# ============================================
from flask import Flask, request, jsonify
import requests
import time
import os

app = Flask(__name__)

# APIs
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

# ============ HOME ============
@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🚗 BRONX ALL-IN-ONE API</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000510;color:#d0d8f0;font-family:'Segoe UI',Arial,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.card{background:rgba(5,15,35,.95);border:2px solid rgba(0,255,136,.3);border-radius:24px;padding:35px;max-width:750px;width:100%;text-align:center}
h1{font-size:26px;background:linear-gradient(90deg,#00ff88,#0096ff,#8b00ff,#ff0080);background-size:300% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:rainbow 3s linear infinite}
@keyframes rainbow{0%{background-position:0% 50%}100%{background-position:300% 50%}}
.subtitle{color:#555;font-size:11px;letter-spacing:2px;margin:5px 0 15px}
.badges{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin:10px 0}
.badge{display:inline-block;padding:5px 12px;border-radius:20px;font-size:8px;font-weight:700;background:rgba(0,255,136,.1);color:#00ff88;border:1px solid rgba(0,255,136,.3)}
code{color:#ffb400;font-family:monospace;font-size:11px;display:block;margin:8px 0;background:rgba(0,0,0,.4);padding:10px;border-radius:8px;word-break:break-all}
input{width:100%;padding:14px;background:rgba(0,0,0,.6);border:2px solid rgba(0,255,136,.2);border-radius:12px;color:#fff;font-size:15px;outline:none;margin:6px 0}
input:focus{border-color:#00ff88}
button{width:100%;padding:16px;background:linear-gradient(135deg,#00ff88,#0096ff,#8b00ff);background-size:200% 200%;color:#fff;border:none;border-radius:12px;font-weight:900;cursor:pointer;font-size:15px;margin:8px 0}
button:hover{transform:scale(1.02)}
.result{background:rgba(0,0,0,.6);border:1px solid rgba(0,255,136,.1);border-radius:12px;padding:14px;margin-top:12px;text-align:left;display:none;max-height:500px;overflow:auto}
.result.show{display:block}
pre{color:#00ff88;font-family:monospace;font-size:10px;white-space:pre-wrap}
footer{color:#333;font-size:9px;margin-top:15px}
</style></head>
<body>
<div class="card">
<h1>🚗 BRONX ALL-IN-ONE API</h1>
<p class="subtitle">4 APIs Combined • Raw Response</p>
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
r.classList.add('show');d.style.color='#ffb400';d.textContent='⏳ Fetching from 4 APIs...';
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

# ============ HELPER: Fetch API ============
def fetch_api(url, timeout=15):
    """Fetch API and return raw response"""
    try:
        resp = requests.get(url, timeout=timeout, verify=False)
        try:
            return resp.json()
        except:
            return resp.text
    except Exception as e:
        return {"error": str(e)}

# ============ MAIN ALL-IN-ONE ENDPOINT ============
@app.route('/api/vehicle')
def all_in_one():
    vehicle = request.args.get('vehicle', '').strip().upper().replace(' ', '').replace('-', '')
    
    if not vehicle:
        return jsonify({
            "status": "error",
            "message": "Missing vehicle number. Use /api/vehicle?vehicle=GJ06RG5545"
        }), 400
    
    start_time = time.time()
    
    # ============ FETCH ALL 4 APIs (RAW) ============
    
    # API 1: 91Wheels
    api1_raw = fetch_api(f"{API_91WHEELS}/?rc={vehicle}")
    
    # API 2: VehicleInfo Worker
    api2_raw = fetch_api(f"{API_VEHICLEINFO}?vehicle_number={vehicle}")
    
    # API 3: Veh2Num (Mobile Number)
    api3_raw = fetch_api(f"{API_VEH2NUM}?key=op&vehicle={vehicle}")
    
    # API 4: CarHayHaha
    api4_raw = fetch_api(f"{API_CARHAYHAHA}?vehicle={vehicle}")
    
    # ============ BUILD RESPONSE ============
    result = {
        "status": "success",
        "vehicle_number": vehicle,
    }
    
    # Add raw responses as-is
    if api1_raw:
        # Remove _proxy if exists
        if isinstance(api1_raw, dict) and '_proxy' in api1_raw:
            del api1_raw['_proxy']
        result["bronx"] = api1_raw
    
    if api2_raw:
        result["bronx"] = api2_raw
    
    if api3_raw:
        result["veh2num_mobile"] = api3_raw
    
    if api4_raw:
        result["bronx"] = api4_raw
    
    elapsed = round(time.time() - start_time, 2)
    result["response_time"] = f"{elapsed}s"
    result["credit"] = "@BRONX_ULTRA"
    
    return jsonify(result)

# ============ HEALTH ============
@app.route('/health')
def health():
    return jsonify({"status": "ONLINE", "credit": "@BRONX_ULTRA"})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "api": "/api/vehicle?vehicle=GJ06RG5545"}), 404

if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings()
    port = int(os.environ.get('PORT', 3000))
    print("🚗 BRONX ALL-IN-ONE API ONLINE!")
    print(f"🚀 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)
