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
executor = ThreadPoolExecutor(max_workers=6)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def home():
    return jsonify({"service":"BRONX RC API","credit":CREDIT,"usage":"/api/vehicle?vehicle=GJ06RG5545"})

# ============ WORKERS API - FIXED ============
def get_workers(rc):
    try:
        # 🔥 CORRECT URL
        url = f"https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number={rc}"
        r = requests.get(url, timeout=10)
        return ("workers", r.json())
    except Exception as e:
        return ("workers", None)

def get_mobile(rc):
    try:
        url = f"https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle={rc}"
        r = requests.get(url, timeout=8)
        d = r.json()
        for k in ['mobile_number','mobile','phone']:
            if d.get(k): return ("mobile", str(d[k]))
        return ("mobile", None)
    except:
        return ("mobile", None)

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

def get_carhayhaha(rc):
    try:
        r = requests.get(f"https://carhayhaha.onrender.com/api/vehicle?vehicle={rc}", timeout=12)
        d = r.json()
        return ("carhayhaha", d if d and d.get("success") else None)
    except:
        return ("carhayhaha", None)

def get_ummmym(rc):
    try:
        r = requests.get(f"https://ummmym.onrender.com/?rc={rc}",
                        headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"}, timeout=15)
        d = r.json()
        if d.get("status")=="success" and d.get("data"):
            clean = d["data"]
            clean.pop("_proxy",None)
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
    
    futures = {
        executor.submit(get_workers, rc): "workers",
        executor.submit(get_mobile, rc): "mobile",
        executor.submit(get_vahanx, rc): "vahanx",
        executor.submit(get_carhayhaha, rc): "carhayhaha",
        executor.submit(get_ummmym, rc): "ummmym",
    }
    
    results = {}
    for f in as_completed(futures):
        try:
            k,v = f.result()
            results[k] = v
        except:
            pass
    
    rt = round(time.time()-start, 2)
    
    w = results.get("workers")
    m = results.get("mobile")
    vx = results.get("vahanx")
    ch = results.get("carhayhaha")
    um = results.get("ummmym")
    
    resp = {
        "status":"success",
        "rc_number":rc,
        "credit":CREDIT,
        "response_time":rt,
        "timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    if w: resp["workers_api"] = w
    if m: resp["mobile_number"] = m
    if vx: resp["vahanx"] = vx
    if ch: resp["carhayhaha_vehicle_details"] = ch
    if um: resp["ummmym_vehicle_details"] = um
    
    resp["summary"] = {
        "owner": (ch.get("owner",{}).get("name") if ch else None) or
                 (um.get("owner_name") if um else None) or
                 (w.get("owner_name") if w else None) or
                 (vx.get("owner_name") if vx else None) or "N/A",
        "mobile": m or (um.get("mobile_number") if um else None) or "N/A",
        "model": (ch.get("vehicle",{}).get("model") if ch else None) or
                 (um.get("maker_model") if um else None) or
                 (w.get("model") if w else None) or "N/A",
        "fuel": (ch.get("vehicle",{}).get("fuel") if ch else None) or
                (um.get("fuel_type") if um else None) or
                (w.get("fuel_type") if w else None) or "N/A",
    }
    
    return jsonify(resp)

@app.route('/health')
def health():
    return jsonify({"status":"ONLINE","credit":CREDIT})

if __name__=='__main__':
    port = int(os.environ.get('PORT',3000))
    app.run(host='0.0.0.0',port=port,debug=False)
