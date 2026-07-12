from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from datetime import datetime

app = Flask(__name__)

CREDIT = "@BRONX_ULTRA"

# ============ ALL APIs ============
FT_OSINT_API = "https://ft-osint-api.duckdns.org/api/vehicle"
BRONX_VEH2NUM_API = "https://bronx-web-api.onrender.com/api/key-bronx/veh2num"
WORKERS_API = "https://vehicleinfo.noobgamingv40.workers.dev/fetch"
NEW_API_1 = "https://ummmym.onrender.com"
NEW_API_2 = "https://carhayhaha.onrender.com/api/vehicle"

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# ============ HOME PAGE ============
@app.route('/')
def home():
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🚗 BRONX RC API V8 - ALL IN ONE</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#000a14;color:#d0d8f0;font-family:'Rajdhani',sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
body::before{{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(0,150,255,.06),transparent 60%),radial-gradient(ellipse at 80% 100%,rgba(139,0,255,.04),transparent 60%);pointer-events:none;z-index:0}}
.card{{background:rgba(5,15,35,.9);border:1px solid rgba(0,150,255,.1);border-radius:20px;padding:30px;max-width:700px;width:100%;text-align:center;position:relative;z-index:1;backdrop-filter:blur(20px)}}
h1{{font-family:'Orbitron',sans-serif;font-size:28px;background:linear-gradient(90deg,#0096ff,#00d4ff,#8b00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px}}
.badge{{display:inline-block;background:rgba(0,255,136,.06);color:#00ff88;padding:4px 14px;border-radius:20px;font-size:10px;border:1px solid rgba(0,255,136,.12);margin:4px}}
.section{{background:rgba(0,0,0,.5);border:1px solid rgba(0,150,255,.08);border-radius:12px;padding:16px;margin:14px 0;text-align:left}}
code{{color:#00ff88;font-family:monospace;font-size:11px;word-break:break-all;display:block;margin:6px 0;background:rgba(0,0,0,.3);padding:8px;border-radius:6px}}
input{{width:100%;padding:14px;background:rgba(0,0,0,.5);border:1px solid rgba(0,150,255,.08);border-radius:10px;color:#fff;font-size:14px;outline:none;margin:8px 0;font-family:'Rajdhani',sans-serif}}
input:focus{{border-color:#0096ff}}
button{{width:100%;padding:14px;background:linear-gradient(135deg,#0096ff,#0066cc);color:#fff;border:none;border-radius:10px;font-weight:700;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:14px;margin:6px 0;transition:.3s}}
button:hover{{transform:scale(1.02);box-shadow:0 0 25px rgba(0,150,255,.2)}}
.result{{background:rgba(0,0,0,.5);border:1px solid rgba(0,255,136,.08);border-radius:10px;padding:14px;margin-top:10px;text-align:left;display:none;max-height:600px;overflow:auto}}
.result.show{{display:block}}
pre{{color:#00ff88;font-family:monospace;font-size:10px;white-space:pre-wrap}}
</style></head>
<body>
<div class="card">
<h1>🚗 BRONX RC API V8</h1>
<p style="color:#667;font-size:12px">ALL-IN-ONE • 4 Sources • Proxy Hidden</p>
<div style="margin:10px 0">
<span class="badge">👤 Owner</span><span class="badge">📱 Mobile</span><span class="badge">🚗 Vehicle</span><span class="badge">🏢 RTO</span><span class="badge">🛡️ Insurance</span>
</div>
<div class="section"><p style="color:#0096ff;font-weight:700">🔗 API Endpoint</p><code>GET /rc?num=GJ06RG5545</code></div>
<input type="text" id="rcInput" placeholder="RC Number (e.g., GJ06RG5545)">
<button onclick="lookup()">🔍 LOOKUP ALL SOURCES</button>
<div class="result" id="result"><pre id="resultData"></pre></div>
<p style="color:#667;font-size:10px;margin-top:14px">{CREDIT} | V8 ALL-IN-ONE</p>
</div>
<script>
async function lookup(){{var n=document.getElementById('rcInput').value.trim();if(!n)return alert('Enter RC!');var d=document.getElementById('result'),p=document.getElementById('resultData');d.classList.add('show');p.style.color='#ffb400';p.textContent='🔍 Fetching from all sources...';try{{var r=await fetch('/rc?num='+encodeURIComponent(n));var j=await r.json();p.style.color='#00ff88';p.textContent=JSON.stringify(j,null,2)}}catch(e){{p.style.color='#ff3366';p.textContent='❌ '+e.message}}}}
</script>
</body></html>'''

# ============ SOURCE 1: FT-OSINT ============
def get_ft_osint(rc_number):
    try:
        url = f"{FT_OSINT_API}?key=bronx-ultra-king-ft-bro-op&vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data and data.get('success'):
            return data
        return None
    except:
        return None

# ============ SOURCE 2: Workers API ============
def get_workers_data(rc_number):
    try:
        url = f"{WORKERS_API}?vehicle_number={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data:
            return data
        return None
    except:
        return None

# ============ SOURCE 3: Bronx Veh2Num ============
def get_bronx_veh2num(rc_number):
    try:
        url = f"{BRONX_VEH2NUM_API}?key=op&vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data and data.get('mobile_number'):
            return data.get('mobile_number')
        if data and isinstance(data, dict):
            for key in ['mobile_number', 'mobile', 'phone', 'number', 'owner_number']:
                if data.get(key):
                    return str(data[key])
        return None
    except:
        return None

# ============ SOURCE 4: VahanX Scraper ============
def get_vahanx_data(rc_number):
    url = f"https://vahanx.in/rc-search/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        
        def gv(label):
            try:
                span = soup.find("span", string=label)
                if span:
                    div = span.find_parent("div")
                    if div:
                        p = div.find("p")
                        if p:
                            return p.get_text(strip=True)
                return None
            except:
                return None
        
        father = gv("Father's Name")
        if not father:
            so = re.search(r'(S/O|D/O|W/O)\s*SH\.?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
            if so:
                father = f"{so.group(1)} SH. {so.group(2).strip()}"
        
        return {
            "father_name": father,
            "owner_name": gv("Owner Name"),
            "phone": gv("Phone"),
            "address": gv("Address"),
            "city": gv("City Name"),
            "rto": gv("Registered RTO"),
            "reg_date": gv("Registration Date"),
            "model": gv("Model Name"),
            "fuel": gv("Fuel Type"),
            "insurance_company": gv("Insurance Company"),
            "insurance_upto": gv("Insurance Upto"),
            "fitness_upto": gv("Fitness Upto"),
            "tax_upto": gv("Tax Upto"),
            "puc_upto": gv("PUC Upto"),
        }
    except:
        return {}

# ============ SOURCE 5: CarInfo RTO ============
def get_carinfo_rto(rc_number):
    url = f"https://www.carinfo.app/rto-vehicle-registration-detail/rto-details/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        info = {}
        match = re.match(r'^([A-Z]{2}\d{2})', rc_number)
        if match:
            info["rto_code"] = match.group(1)
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    k = cells[0].get_text(strip=True).lower()
                    v = cells[1].get_text(strip=True)
                    if 'state' in k: info['state'] = v
                    elif 'address' in k: info['rto_address'] = v
                    elif 'phone' in k: info['rto_phone'] = v
                    elif 'email' in k: info['rto_email'] = v
                    elif 'city' in k: info['rto_city'] = v
        return info if len(info) > 1 else None
    except:
        return None

# ============ SOURCE 6: NEW API (ummmym) ============
def get_new_api_1(rc_number):
    """https://ummmym.onrender.com"""
    try:
        url = f"{NEW_API_1}/?rc={rc_number}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        if data.get("status") == "success" and data.get("data"):
            # Remove proxy info
            clean_data = data.get("data", {})
            clean_data.pop("_proxy", None)
            return clean_data
        return None
    except:
        return None

# ============ SOURCE 7: NEW API 2 (carhayhaha) ============
def get_new_api_2(rc_number):
    """https://carhayhaha.onrender.com/api/vehicle"""
    try:
        url = f"{NEW_API_2}?vehicle={rc_number}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        if data and data.get("success"):
            return data
        return None
    except:
        return None

# ============ MAIN RC ENDPOINT ============
@app.route('/rc')
def rc_lookup():
    start_time = time.time()
    rc_number = request.args.get('num', '').strip().upper().replace(' ', '').replace('-', '')
    
    if not rc_number:
        return jsonify({
            "status": "error",
            "message": "Missing RC number",
            "credit": CREDIT
        }), 400
    
    # Fetch from ALL sources
    ft = get_ft_osint(rc_number)
    worker = get_workers_data(rc_number)
    v2n = get_bronx_veh2num(rc_number)
    vx = get_vahanx_data(rc_number)
    rto = get_carinfo_rto(rc_number)
    api1 = get_new_api_1(rc_number)
    api2 = get_new_api_2(rc_number)
    
    response_time = round(time.time() - start_time, 2)
    
    # Build final response
    result = {
        "status": "success",
        "rc_number": rc_number,
        "credit": CREDIT,
        "powered_by": "@BRONX_ULTRA",
        "response_time_seconds": response_time,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "sources": {
            "ft_osint": "✅" if ft else "❌",
            "workers_api": "✅" if worker else "❌",
            "veh2num": "✅" if v2n else "❌",
            "vahanx": "✅" if vx else "❌",
            "carinfo": "✅" if rto else "❌",
            "ummmym_api": "✅" if api1 else "❌",
            "carhayhaha_api": "✅" if api2 else "❌"
        }
    }
    
    # ============ FT-OSINT DATA ============
    if ft:
        ft_owner = ft.get("owner", {})
        ft_addr = ft.get("address", {})
        ft_reg = ft.get("registration", {})
        ft_vehicle = ft.get("vehicle", {})
        ft_insurance = ft.get("insurance", {})
        ft_ident = ft.get("identification", {})
        ft_financier = ft.get("financier", {})
        ft_fitness = ft.get("fitness", {})
        ft_puc = ft.get("puc", {})
        
        result["ft_osint"] = {
            "owner_name": ft_owner.get("name"),
            "father_name": ft_owner.get("father_name"),
            "present_address": ft_addr.get("present"),
            "permanent_address": ft_addr.get("permanent"),
            "city": ft_addr.get("city"),
            "pincode": ft_addr.get("pincode"),
            "rto_code": ft_reg.get("rto_code"),
            "rto_name": ft_reg.get("rto"),
            "reg_date": ft_reg.get("date"),
            "manufacturer": ft_vehicle.get("manufacturer"),
            "model": ft_vehicle.get("model"),
            "fuel_type": ft_vehicle.get("fuel"),
            "engine_cc": ft_vehicle.get("cc"),
            "vehicle_class": ft_vehicle.get("class"),
            "chassis_number": ft_ident.get("chassis"),
            "engine_number": ft_ident.get("engine"),
            "insurance_company": ft_insurance.get("company"),
            "insurance_valid_upto": ft_insurance.get("valid_upto"),
            "insurance_policy_no": ft_insurance.get("policy_no"),
            "financier_name": ft_financier.get("name"),
            "fitness_valid_upto": ft_fitness.get("fitness_upto"),
            "tax_valid_upto": ft_fitness.get("tax_upto"),
            "puc_valid_upto": ft_puc.get("valid_upto"),
            "puc_number": ft_puc.get("no"),
        }
        result["ft_osint"] = {k: v for k, v in result["ft_osint"].items() if v}
    
    # ============ WORKERS API DATA ============
    if worker:
        result["workers_api"] = worker
    
    # ============ MOBILE NUMBER ============
    mobile = v2n or (vx.get("phone") if vx else None)
    if mobile:
        result["mobile_number"] = mobile
    
    # ============ VAHANX DATA ============
    if vx:
        vx_clean = {k: v for k, v in vx.items() if v}
        if vx_clean:
            result["vahanx"] = vx_clean
    
    # ============ CARINFO RTO DATA ============
    if rto:
        result["carinfo_rto"] = rto
    
    # ============ NEW API 1 (ummmym) - Proxy hidden ============
    if api1:
        result["ummmym_vehicle_details"] = api1
    
    # ============ NEW API 2 (carhayhaha) ============
    if api2:
        result["carhayhaha_vehicle_details"] = api2
    
    # ============ MERGED SUMMARY ============
    result["📋_summary"] = {
        "owner_name": (
            (ft.get("owner", {}).get("name") if ft else None) or
            (api1.get("owner_name") if api1 else None) or
            (api2.get("owner", {}).get("name") if api2 else None) or
            (worker.get("owner_name") if worker else None) or
            (vx.get("owner_name") if vx else None) or "N/A"
        ),
        "mobile_number": mobile or (api1.get("mobile_number") if api1 else None) or "N/A",
        "model": (
            (ft.get("vehicle", {}).get("model") if ft else None) or
            (api1.get("maker_model") if api1 else None) or
            (worker.get("model") if worker else None) or
            (vx.get("model") if vx else None) or "N/A"
        ),
        "fuel_type": (
            (ft.get("vehicle", {}).get("fuel") if ft else None) or
            (api1.get("fuel_type") if api1 else None) or
            (worker.get("fuel_type") if worker else None) or
            (vx.get("fuel") if vx else None) or "N/A"
        ),
        "registration_date": (
            (ft.get("registration", {}).get("date") if ft else None) or
            (api1.get("registration_date") if api1 else None) or
            (worker.get("registration_date") if worker else None) or
            (vx.get("reg_date") if vx else None) or "N/A"
        ),
        "rto_name": (
            (ft.get("registration", {}).get("rto") if ft else None) or
            (api1.get("registered_at") if api1 else None) or
            (vx.get("rto") if vx else None) or "N/A"
        ),
        "insurance_company": (
            (ft.get("insurance", {}).get("company") if ft else None) or
            (api1.get("insurance_company") if api1 else None) or
            (vx.get("insurance_company") if vx else None) or "N/A"
        )
    }
    
    return jsonify(result)


# ============ HEALTH CHECK ============
@app.route('/health')
@app.route('/test')
def test():
    return jsonify({
        "status": "✅ BRONX RC API V8 ONLINE",
        "version": "8.0 ALL-IN-ONE",
        "endpoint": "/rc?num=GJ06RG5545",
        "sources": [
            "FT-OSINT",
            "Workers API",
            "Veh2Num",
            "VahanX Scraper",
            "CarInfo RTO",
            "ummmym API (NEW)",
            "carhayhaha API (NEW)"
        ],
        "credit": CREDIT
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Not found",
        "home": "/",
        "api": "/rc?num=RC_NUMBER"
    }), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"""
    🚗 BRONX RC API V8 - ALL IN ONE
    📍 Port: {port}
    💡 Usage: /rc?num=GJ06RG5545
    """)
    app.run(host='0.0.0.0', port=port)
