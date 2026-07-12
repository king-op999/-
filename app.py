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
executor = ThreadPoolExecutor(max_workers=4)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def home():
    return jsonify({
        "service": "BRONX RC API V5.0",
        "credit": CREDIT,
        "usage": "/api/vehicle?vehicle=GJ06RG5545"
    })

# ============ SOURCE 1: carhayhaha ============
def get_carhayhaha(rc):
    try:
        r = requests.get(f"https://carhayhaha.onrender.com/api/vehicle?vehicle={rc}", timeout=10)
        d = r.json()
        return ("carhayhaha", d if d and d.get("success") else None)
    except:
        return ("carhayhaha", None)

# ============ SOURCE 2: Veh2Num ============
def get_mobile(rc):
    try:
        r = requests.get(f"https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle={rc}", timeout=8)
        d = r.json()
        for k in ['mobile_number','mobile','phone']:
            if d.get(k): return ("mobile", str(d[k]))
        return ("mobile", None)
    except:
        return ("mobile", None)

# ============ SOURCE 3: VahanX ============
def get_vahanx(rc):
    try:
        r = requests.get(f"https://vahanx.in/rc-search/{rc}", headers={"User-Agent":"Mozilla/5.0"}, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        def gv(l):
            try:
                s=soup.find("span",string=l)
                return s.find_parent("div").find("p").get_text(strip=True) if s else None
            except: return None
        d = {"owner_name":gv("Owner Name"),"phone":gv("Phone"),"address":gv("Address"),
             "city":gv("City Name"),"rto":gv("Registered RTO"),"reg_date":gv("Registration Date"),
             "model":gv("Model Name"),"fuel":gv("Fuel Type")}
        return ("vahanx", {k:v for k,v in d.items() if v})
    except:
        return ("vahanx", None)

# ============ SOURCE 4: ummmym (QUICK - no retry) ============
def get_ummmym(rc):
    try:
        r = requests.get(f"https://ummmym.onrender.com/?rc={rc}",
                        headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"}, 
                        timeout=5)  # SHORT timeout
        d = r.json()
        if d.get("status") == "success" and d.get("data"):
            clean = d["data"]
            clean.pop("_proxy", None)
            return ("ummmym", clean)
        return ("ummmym", None)
    except:
        return ("ummmym", None)


@app.route('/api/vehicle', methods=["GET","POST","OPTIONS"])
@app.route('/rc', methods=["GET","POST","OPTIONS"])
def lookup():
    if request.method=="OPTIONS": return "",204
    
    start = time.time()
    
    if request.method=="POST":
        d = request.get_json(silent=True) or {}
        rc = (d.get("vehicle_number") or d.get("vehicle") or d.get("num") or "").upper().strip()
    else:
        rc = (request.args.get("vehicle") or request.args.get("vehicle_number") or 
              request.args.get("num") or "").upper().strip()
    
    if not rc or len(rc)<4:
        return jsonify({"error":"RC required"}),400
    
    # ALL 4 parallel
    futures = {
        executor.submit(get_carhayhaha, rc): "carhayhaha",
        executor.submit(get_mobile, rc): "mobile",
        executor.submit(get_vahanx, rc): "vahanx",
        executor.submit(get_ummmym, rc): "ummmym",
    }
    
    results = {}
    for f in as_completed(futures):
        try:
            k,v = f.result()
            if v: results[k] = v
        except:
            pass
    
    rt = round(time.time()-start, 2)
    
    ch = results.get("carhayhaha")
    m = results.get("mobile")
    vx = results.get("vahanx")
    um = results.get("ummmym")
    
    resp = {
        "status":"success",
        "rc_number":rc,
        "credit":CREDIT,
        "response_time_seconds":rt,
        "timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # CARHAYHAHA
    if ch:
        resp["vehicle_details"] = {
            "owner_name": ch.get("owner",{}).get("name"),
            "father_name": ch.get("owner",{}).get("father_name"),
            "registration_date": ch.get("registration",{}).get("date"),
            "rto": ch.get("registration",{}).get("rto"),
            "rto_code": ch.get("registration",{}).get("rto_code"),
            "manufacturer": ch.get("vehicle",{}).get("manufacturer"),
            "model": ch.get("vehicle",{}).get("model"),
            "variant": ch.get("vehicle",{}).get("variant"),
            "fuel_type": ch.get("vehicle",{}).get("fuel"),
            "vehicle_class": ch.get("vehicle",{}).get("class"),
            "chassis_number": ch.get("identification",{}).get("chassis"),
            "engine_number": ch.get("identification",{}).get("engine"),
            "insurance_company": ch.get("insurance",{}).get("company"),
            "insurance_valid_upto": ch.get("insurance",{}).get("valid_upto"),
            "insurance_policy_no": ch.get("insurance",{}).get("policy_no"),
            "address": ch.get("address",{}).get("present"),
            "city": ch.get("address",{}).get("city"),
            "rto_phone": ch.get("rto_contact",{}).get("phone"),
        }
        resp["vehicle_details"] = {k:v for k,v in resp["vehicle_details"].items() if v}
    
    # UMMMYM (agar aaya to add karo)
    if um:
        resp["ummmym_details"] = um
    
    # MOBILE
    if m:
        resp["mobile_number"] = m
    
    # VAHANX
    if vx:
        resp["extra_info"] = vx
    
    return jsonify(resp)


@app.route('/health')
def health():
    return jsonify({"status":"ONLINE","version":"V5.0","credit":CREDIT})


if __name__=='__main__':
    port = int(os.environ.get('PORT',3000))
    app.run(host='0.0.0.0',port=port,debug=False)
