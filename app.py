# ============================================
# 🚗 BRONX ALL-IN-ONE VEHICLE API
# 4 APIs Combined • Clean Response • Fast
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
<title>🚗 BRONX ALL-IN-ONE VEHICLE API</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000510;color:#d0d8f0;font-family:'Segoe UI',Arial,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.card{background:rgba(5,15,35,.95);border:2px solid rgba(0,255,136,.3);border-radius:24px;padding:35px;max-width:750px;width:100%;text-align:center}
h1{font-size:26px;background:linear-gradient(90deg,#00ff88,#0096ff,#8b00ff,#ff0080);background-size:300% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:rainbow 3s linear infinite}
@keyframes rainbow{0%{background-position:0% 50%}100%{background-position:300% 50%}}
.subtitle{color:#555;font-size:11px;letter-spacing:2px;margin:5px 0 15px}
.badges{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin:10px 0}
.badge{display:inline-block;padding:5px 12px;border-radius:20px;font-size:8px;font-weight:700;background:rgba(0,255,136,.1);color:#00ff88;border:1px solid rgba(0,255,136,.3)}
.badge.b{background:rgba(0,150,255,.1);color:#0096ff;border-color:rgba(0,150,255,.3)}
.badge.p{background:rgba(139,0,255,.1);color:#8b00ff;border-color:rgba(139,0,255,.3)}
.badge.r{background:rgba(255,0,128,.1);color:#ff0080;border-color:rgba(255,0,128,.3)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:15px 0}
.stat{background:rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.03);border-radius:10px;padding:12px}
.stat .num{font-size:20px;font-weight:900;color:#00ff88}
.stat .lbl{font-size:7px;color:#555;text-transform:uppercase}
code{color:#ffb400;font-family:monospace;font-size:11px;display:block;margin:8px 0;background:rgba(0,0,0,.4);padding:10px;border-radius:8px;word-break:break-all}
input{width:100%;padding:14px;background:rgba(0,0,0,.6);border:2px solid rgba(0,255,136,.2);border-radius:12px;color:#fff;font-size:15px;outline:none;margin:6px 0}
input:focus{border-color:#00ff88;box-shadow:0 0 30px rgba(0,255,136,.1)}
button{width:100%;padding:16px;background:linear-gradient(135deg,#00ff88,#0096ff,#8b00ff);background-size:200% 200%;color:#fff;border:none;border-radius:12px;font-weight:900;cursor:pointer;font-size:15px;margin:8px 0;letter-spacing:2px}
button:hover{transform:scale(1.02);box-shadow:0 0 40px rgba(0,255,136,.2)}
.result{background:rgba(0,0,0,.6);border:1px solid rgba(0,255,136,.1);border-radius:12px;padding:14px;margin-top:12px;text-align:left;display:none;max-height:500px;overflow:auto}
.result.show{display:block}
pre{color:#00ff88;font-family:monospace;font-size:10px;white-space:pre-wrap}
footer{color:#333;font-size:9px;margin-top:15px}
</style></head>
<body>
<div class="card">
<h1>🚗 BRONX ALL-IN-ONE API</h1>
<p class="subtitle">4 APIs Combined • Clean Response</p>
<div class="badges">
<span class="badge">📱 91Wheels</span><span class="badge b">🌐 VehicleInfo</span>
<span class="badge p">🔍 Veh2Num</span><span class="badge r">🚗 CarHay</span>
</div>
<code>GET /api/vehicle?vehicle=MH02FZ0555</code>
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

# ============ API 1: 91Wheels ============
def get_91wheels(vehicle):
    try:
        url = f"{API_91WHEELS}/?rc={vehicle}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        
        # Remove _proxy if present
        if '_proxy' in data:
            del data['_proxy']
        
        if data.get('success') or data.get('data'):
            return data
        return None
    except:
        return None

# ============ API 2: VehicleInfo Worker ============
def get_vehicleinfo(vehicle):
    try:
        url = f"{API_VEHICLEINFO}?vehicle_number={vehicle}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        
        if data.get('success'):
            vd = data.get('vehicle_data', {})
            return {
                "owner_name": vd.get('owner', ''),
                "father_name": vd.get('ownerFatherName', ''),
                "manufacturer": vd.get('manufacturer', ''),
                "model": vd.get('vehicle', ''),
                "variant": vd.get('variant', ''),
                "fuel_type": vd.get('fuelType', ''),
                "engine_cc": vd.get('cubicCapacity', ''),
                "vehicle_class": vd.get('vehicleClass', ''),
                "seating_capacity": vd.get('seatCapacity', ''),
                "registration_date": vd.get('regDate', ''),
                "insurance_company": vd.get('insuranceCompanyName', ''),
                "insurance_upto": vd.get('insuranceUpto', ''),
                "chassis": vd.get('chassis', ''),
                "engine": vd.get('engine', ''),
                "pincode": vd.get('pincode', ''),
            }
        return None
    except:
        return None

# ============ API 3: Veh2Num (Mobile Number) ============
def get_veh2num(vehicle):
    try:
        url = f"{API_VEH2NUM}?key=op&vehicle={vehicle}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        
        if isinstance(data, dict):
            for key in ['mobile_number', 'mobile', 'phone', 'number', 'owner_number']:
                if data.get(key):
                    return str(data[key])
        return None
    except:
        return None

# ============ API 4: CarHayHaha ============
def get_carhayhaha(vehicle):
    try:
        url = f"{API_CARHAYHAHA}?vehicle={vehicle}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        
        if data and isinstance(data, dict):
            # Remove any proxy/cache info
            clean = {}
            for k, v in data.items():
                if not k.startswith('_') and k not in ['credit', 'api_by', 'powered_by', 'cache', 'proxy']:
                    clean[k] = v
            return clean if clean else None
        return None
    except:
        return None

# ============ MAIN ALL-IN-ONE ENDPOINT ============
@app.route('/api/vehicle')
def all_in_one():
    vehicle = request.args.get('vehicle', '').strip().upper().replace(' ', '').replace('-', '')
    
    if not vehicle:
        return jsonify({
            "status": "error",
            "message": "Missing vehicle number. Use /api/vehicle?vehicle=MH02FZ0555"
        }), 400
    
    start_time = time.time()
    
    # Fetch from all 4 APIs
    data_91wheels = get_91wheels(vehicle)
    data_vehicleinfo = get_vehicleinfo(vehicle)
    mobile_veh2num = get_veh2num(vehicle)
    data_carhayhaha = get_carhayhaha(vehicle)
    
    # ============ BUILD CLEAN RESPONSE ============
    result = {
        "status": "success",
        "vehicle_number": vehicle,
        "sources": []
    }
    
    # Track which sources contributed
    if data_91wheels: result["sources"].append("91wheels")
    if data_vehicleinfo: result["sources"].append("vehicleinfo")
    if mobile_veh2num: result["sources"].append("veh2num")
    if data_carhayhaha: result["sources"].append("carhayhaha")
    
    # ============ OWNER DETAILS ============
    owner = {}
    
    # From 91Wheels
    if data_91wheels:
        d = data_91wheels.get('data', {})
        owner["owner_name"] = d.get('owner_name', '')
        owner["father_name"] = d.get('father_name', '')
        owner["present_address"] = d.get('present_address', '')
        owner["permanent_address"] = d.get('permanent_address', '')
    
    # From VehicleInfo
    if data_vehicleinfo:
        if not owner.get("owner_name"):
            owner["owner_name"] = data_vehicleinfo.get("owner_name", '')
        if not owner.get("father_name"):
            owner["father_name"] = data_vehicleinfo.get("father_name", '')
    
    # Mobile number
    owner["mobile_number"] = mobile_veh2num or (data_91wheels.get('data', {}).get('mobile_number', '')) or ''
    
    owner = {k: v for k, v in owner.items() if v}
    if owner:
        result["owner_details"] = owner
    
    # ============ VEHICLE DETAILS ============
    vehicle_details = {}
    
    if data_91wheels:
        d = data_91wheels.get('data', {})
        vehicle_details.update({
            "manufacturer": d.get('maker_description', ''),
            "model": d.get('maker_model', ''),
            "fuel_type": d.get('fuel_type', ''),
            "engine_cc": d.get('cubic_capacity', ''),
            "cylinders": d.get('no_cylinders', ''),
            "vehicle_class": d.get('vehicle_category_description', ''),
            "body_type": d.get('body_type', ''),
            "color": d.get('color', ''),
            "seating_capacity": d.get('seat_capacity', ''),
            "gross_weight": d.get('vehicle_gross_weight', ''),
            "unladen_weight": d.get('unladen_weight', ''),
            "wheelbase": d.get('wheelbase', ''),
            "manufacturing_date": d.get('manufacturing_date_formatted', ''),
        })
    
    if data_vehicleinfo:
        if not vehicle_details.get("manufacturer"):
            vehicle_details["manufacturer"] = data_vehicleinfo.get("manufacturer", '')
        if not vehicle_details.get("model"):
            vehicle_details["model"] = data_vehicleinfo.get("model", '')
        if not vehicle_details.get("fuel_type"):
            vehicle_details["fuel_type"] = data_vehicleinfo.get("fuel_type", '')
        if not vehicle_details.get("engine_cc"):
            vehicle_details["engine_cc"] = str(data_vehicleinfo.get("engine_cc", ''))
        if not vehicle_details.get("vehicle_class"):
            vehicle_details["vehicle_class"] = data_vehicleinfo.get("vehicle_class", '')
        if not vehicle_details.get("seating_capacity"):
            vehicle_details["seating_capacity"] = str(data_vehicleinfo.get("seating_capacity", ''))
    
    vehicle_details = {k: v for k, v in vehicle_details.items() if v}
    if vehicle_details:
        result["vehicle_details"] = vehicle_details
    
    # ============ REGISTRATION ============
    reg = {}
    
    if data_91wheels:
        d = data_91wheels.get('data', {})
        reg.update({
            "registration_date": d.get('registration_date', ''),
            "registered_at": d.get('registered_at', ''),
            "rto_code": d.get('rto_code', ''),
            "rc_status": d.get('rc_status', ''),
            "owner_number": d.get('owner_number', ''),
        })
    
    if data_vehicleinfo:
        if not reg.get("registration_date"):
            reg["registration_date"] = data_vehicleinfo.get("registration_date", '')
        if not reg.get("pincode"):
            reg["pincode"] = data_vehicleinfo.get("pincode", '')
    
    reg = {k: v for k, v in reg.items() if v}
    if reg:
        result["registration"] = reg
    
    # ============ INSURANCE ============
    ins = {}
    
    if data_91wheels:
        d = data_91wheels.get('data', {})
        ins.update({
            "company": d.get('insurance_company', ''),
            "policy_number": d.get('insurance_policy_number', ''),
            "valid_upto": d.get('insurance_upto', ''),
        })
    
    if data_vehicleinfo:
        if not ins.get("company"):
            ins["company"] = data_vehicleinfo.get("insurance_company", '')
        if not ins.get("valid_upto"):
            ins["valid_upto"] = data_vehicleinfo.get("insurance_upto", '')
    
    ins = {k: v for k, v in ins.items() if v}
    if ins:
        result["insurance"] = ins
    
    # ============ IDENTIFICATION ============
    ident = {}
    
    if data_91wheels:
        d = data_91wheels.get('data', {})
        ident["chassis_number"] = d.get('vehicle_chasi_number', '')
        ident["engine_number"] = d.get('vehicle_engine_number', '')
    
    if data_vehicleinfo:
        if not ident.get("chassis_number"):
            ident["chassis_number"] = data_vehicleinfo.get("chassis", '')
        if not ident.get("engine_number"):
            ident["engine_number"] = data_vehicleinfo.get("engine", '')
    
    ident = {k: v for k, v in ident.items() if v}
    if ident:
        result["identification"] = ident
    
    # ============ TAX & FITNESS ============
    tax = {}
    
    if data_91wheels:
        d = data_91wheels.get('data', {})
        tax["tax_valid_upto"] = d.get('tax_upto', '')
        tax["fitness_valid_upto"] = d.get('fit_up_to', '')
        tax["puc_number"] = d.get('pucc_number', '')
        tax["puc_valid_upto"] = d.get('pucc_upto', '')
    
    tax = {k: v for k, v in tax.items() if v}
    if tax:
        result["fitness_tax_puc"] = tax
    
    # ============ EXTRA (CarHayHaha) ============
    if data_carhayhaha:
        result["extra_data"] = data_carhayhaha
    
    # ============ FINAL ============
    elapsed = round(time.time() - start_time, 2)
    result["response_time"] = f"{elapsed}s"
    result["credit"] = "@BRONX_ULTRA"
    
    return jsonify(result)

# ============ HEALTH CHECK ============
@app.route('/health')
def health():
    return jsonify({
        "status": "✅ BRONX ALL-IN-ONE VEHICLE API ONLINE",
        "apis": ["91wheels", "vehicleinfo", "veh2num", "carhayhaha"],
        "credit": "@BRONX_ULTRA"
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "api": "/api/vehicle?vehicle=GJ06RG5545"}), 404

if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings()
    port = int(os.environ.get('PORT', 3000))
    print("🚗 BRONX ALL-IN-ONE VEHICLE API")
    print(f"🚀 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)
