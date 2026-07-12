from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

CREDIT = "@BRONX_ULTRA"

# ============ ALL APIs ============
FT_OSINT_API = "https://ft-osint-api.duckdns.org/api/vehicle"
BRONX_VEH2NUM_API = "https://bronx-web-api.onrender.com/api/key-bronx/veh2num"
WORKERS_API = "https://vehicleinfo.noobgamingv40.workers.dev/fetch"
NEW_API_1 = "https://ummmym.onrender.com"
NEW_API_2 = "https://carhayhaha.onrender.com/api/vehicle"

executor = ThreadPoolExecutor(max_workers=10)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def home():
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🚗 BRONX RC API V9</title>
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
<h1>🚗 BRONX RC API V9</h1>
<p style="color:#667;font-size:12px">ALL-IN-ONE • 7 Sources • Optimized</p>
<div style="margin:10px 0">
<span class="badge">👤 Owner</span><span class="badge">📱 Mobile</span><span class="badge">🚗 Vehicle</span><span class="badge">🏢 RTO</span>
</div>
<div class="section"><code>GET /api/vehicle?vehicle=GJ06RG5545</code></div>
<div class="section"><code>POST /api/vehicle</code></div>
<input type="text" id="rcInput" placeholder="RC Number (e.g., GJ06RG5545)">
<button onclick="lookup()">🔍 LOOKUP</button>
<div class="result" id="result"><pre id="resultData"></pre></div>
<p style="color:#667;font-size:10px;margin-top:14px">{CREDIT} | V9</p>
</div>
<script>
async function lookup(){{var n=document.getElementById('rcInput').value.trim();if(!n)return alert('Enter RC!');var d=document.getElementById('result'),p=document.getElementById('resultData');d.classList.add('show');p.style.color='#ffb400';p.textContent='🔍 Fetching...';try{{var r=await fetch('/api/vehicle?vehicle='+encodeURIComponent(n));var j=await r.json();p.style.color='#00ff88';p.textContent=JSON.stringify(j,null,2)}}catch(e){{p.style.color='#ff3366';p.textContent='❌ '+e.message}}}}
</script>
</body></html>'''


# ============ SOURCE FUNCTIONS ============
def get_ft_osint(rc_number):
    try:
        url = f"{FT_OSINT_API}?key=bronx-ultra-king-ft-bro-op&vehicle={rc_number}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return ("ft_osint", data if data and data.get('success') else None)
    except:
        return ("ft_osint", None)

def get_workers_data(rc_number):
    try:
        url = f"{WORKERS_API}?vehicle_number={rc_number}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return ("workers", data if data else None)
    except:
        return ("workers", None)

def get_bronx_veh2num(rc_number):
    try:
        url = f"{BRONX_VEH2NUM_API}?key=op&vehicle={rc_number}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        mobile = None
        if data:
            for key in ['mobile_number', 'mobile', 'phone', 'number']:
                if data.get(key):
                    mobile = str(data[key])
                    break
        return ("veh2num", mobile)
    except:
        return ("veh2num", None)

def get_vahanx_data(rc_number):
    try:
        url = f"https://vahanx.in/rc-search/{rc_number}"
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        
        def gv(label):
            try:
                span = soup.find("span", string=label)
                if span:
                    div = span.find_parent("div")
                    if div:
                        p = div.find("p")
                        if p: return p.get_text(strip=True)
                return None
            except: return None
        
        data = {
            "owner_name": gv("Owner Name"), "phone": gv("Phone"),
            "address": gv("Address"), "city": gv("City Name"),
            "rto": gv("Registered RTO"), "reg_date": gv("Registration Date"),
            "model": gv("Model Name"), "fuel": gv("Fuel Type"),
            "insurance_company": gv("Insurance Company"),
            "insurance_upto": gv("Insurance Upto"),
        }
        return ("vahanx", {k: v for k, v in data.items() if v})
    except:
        return ("vahanx", None)

def get_carinfo_rto(rc_number):
    try:
        url = f"https://www.carinfo.app/rto-vehicle-registration-detail/rto-details/{rc_number}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        info = {}
        match = re.match(r'^([A-Z]{2}\d{2})', rc_number)
        if match: info["rto_code"] = match.group(1)
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    k = cells[0].get_text(strip=True).lower()
                    v = cells[1].get_text(strip=True)
                    if 'state' in k: info['state'] = v
                    elif 'address' in k: info['rto_address'] = v
                    elif 'phone' in k: info['rto_phone'] = v
        return ("carinfo", info if info else None)
    except:
        return ("carinfo", None)

def get_new_api_1(rc_number):
    """ummmym API - RETRY 3x with delay"""
    for attempt in range(3):
        try:
            url = f"{NEW_API_1}/?rc={rc_number}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "https://ummmym.onrender.com/",
            }
            resp = requests.get(url, headers=headers, timeout=30)
            data = resp.json()
            if data.get("status") == "success" and data.get("data"):
                clean = data.get("data", {})
                clean.pop("_proxy", None)
                return ("ummmym", clean if clean else None)
            time.sleep(2)
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                print(f"ummmym failed: {e}")
    return ("ummmym", None)

def get_new_api_2(rc_number):
    """carhayhaha API"""
    try:
        url = f"{NEW_API_2}?vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        return ("carhayhaha", data if data and data.get("success") else None)
    except:
        return ("carhayhaha", None)


# ============ MAIN ENDPOINT ============
@app.route('/api/vehicle', methods=["GET", "POST", "OPTIONS"])
@app.route('/rc', methods=["GET", "POST", "OPTIONS"])
def vehicle_lookup():
    if request.method == "OPTIONS":
        return "", 204
    
    start_time = time.time()
    
    if request.method == "POST":
        d = request.get_json(silent=True) or {}
        rc_number = (d.get("vehicle_number") or d.get("vehicle") or d.get("num") or "").upper().strip()
    else:
        rc_number = (request.args.get("vehicle") or request.args.get("vehicle_number") or 
                     request.args.get("num") or "").upper().strip()
    
    if not rc_number or len(rc_number) < 4:
        return jsonify({
            "status": "error",
            "message": "Vehicle number required",
            "usage": "/api/vehicle?vehicle=GJ06RG5545"
        }), 400
    
    # Run all 7 in parallel
    futures = {
        executor.submit(get_ft_osint, rc_number): "ft",
        executor.submit(get_workers_data, rc_number): "workers",
        executor.submit(get_bronx_veh2num, rc_number): "veh2num",
        executor.submit(get_vahanx_data, rc_number): "vahanx",
        executor.submit(get_carinfo_rto, rc_number): "carinfo",
        executor.submit(get_new_api_1, rc_number): "ummmym",
        executor.submit(get_new_api_2, rc_number): "carhayhaha",
    }
    
    results = {}
    for future in as_completed(futures):
        try:
            name, data = future.result()
            results[name] = data
        except:
            pass
    
    response_time = round(time.time() - start_time, 2)
    
    ft = results.get("ft")
    worker = results.get("workers")
    v2n = results.get("veh2num")
    vx = results.get("vahanx")
    rto = results.get("carinfo")
    api1 = results.get("ummmym")
    api2 = results.get("carhayhaha")
    
    result = {
        "status": "success",
        "rc_number": rc_number,
        "credit": CREDIT,
        "response_time_seconds": response_time,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "sources": {
            "ft_osint": "✅" if ft else "❌",
            "workers": "✅" if worker else "❌",
            "veh2num": "✅" if v2n else "❌",
            "vahanx": "✅" if vx else "❌",
            "carinfo": "✅" if rto else "❌",
            "ummmym": "✅" if api1 else "❌",
            "carhayhaha": "✅" if api2 else "❌"
        }
    }
    
    if ft:
        o = ft.get("owner", {})
        a = ft.get("address", {})
        r = ft.get("registration", {})
        v = ft.get("vehicle", {})
        i = ft.get("insurance", {})
        idn = ft.get("identification", {})
        fi = ft.get("fitness", {})
        
        result["ft_osint"] = {k: v for k, v in {
            "owner_name": o.get("name"), "father_name": o.get("father_name"),
            "city": a.get("city"), "pincode": a.get("pincode"),
            "rto_code": r.get("rto_code"), "rto_name": r.get("rto"),
            "reg_date": r.get("date"), "manufacturer": v.get("manufacturer"),
            "model": v.get("model"), "fuel_type": v.get("fuel"),
            "chassis_number": idn.get("chassis"), "engine_number": idn.get("engine"),
            "insurance_company": i.get("company"),
            "insurance_valid_upto": i.get("valid_upto"),
            "fitness_upto": fi.get("fitness_upto"),
            "tax_upto": fi.get("tax_upto"),
        }.items() if v}
    
    if worker: result["workers_api"] = worker
    if v2n: result["mobile_number"] = v2n
    if vx: result["vahanx"] = vx
    if rto: result["carinfo_rto"] = rto
    if api1: result["ummmym_vehicle_details"] = api1
    if api2: result["carhayhaha_vehicle_details"] = api2
    
    # Summary
    result["📋_summary"] = {
        "owner_name": (
            (api2.get("owner", {}).get("name") if api2 else None) or
            (api1.get("owner_name") if api1 else None) or
            (ft.get("owner", {}).get("name") if ft else None) or
            (vx.get("owner_name") if vx else None) or "N/A"
        ),
        "mobile_number": v2n or (api1.get("mobile_number") if api1 else None) or "N/A",
        "model": (
            (api2.get("vehicle", {}).get("model") if api2 else None) or
            (api1.get("maker_model") if api1 else None) or
            (ft.get("vehicle", {}).get("model") if ft else None) or "N/A"
        ),
        "fuel_type": (
            (api2.get("vehicle", {}).get("fuel") if api2 else None) or
            (api1.get("fuel_type") if api1 else None) or
            (ft.get("vehicle", {}).get("fuel") if ft else None) or "N/A"
        ),
        "registration_date": (
            (api2.get("registration", {}).get("date") if api2 else None) or
            (api1.get("registration_date") if api1 else None) or
            (ft.get("registration", {}).get("date") if ft else None) or "N/A"
        ),
        "rto_name": (
            (api2.get("registration", {}).get("rto") if api2 else None) or
            (api1.get("registered_at") if api1 else None) or
            (ft.get("registration", {}).get("rto") if ft else None) or "N/A"
        )
    }
    
    return jsonify(result)


@app.route('/health')
def health():
    return jsonify({"status": "✅ ONLINE", "version": "V9", "credit": CREDIT})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"🚗 BRONX RC API V9 | Port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
