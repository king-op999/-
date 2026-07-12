from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from datetime import datetime

app = Flask(__name__)
CREDIT = "@BRONX_ULTRA"

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def home():
    return jsonify({"service":"RC API","credit":CREDIT,"usage":"/api/vehicle?vehicle=GJ06RG5545"})


def fetch_ummmym(rc):
    try:
        r = requests.get(f"https://ummmym.onrender.com/?rc={rc}",
                        headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"}, timeout=15)
        d = r.json()
        if d.get("status")=="success" and d.get("data"):
            clean = d["data"]
            clean.pop("_proxy",None)  # 🔥 PROXY HIDE
            # Extra fields hide
            clean.pop("client_id",None)
            clean.pop("less_info",None)
            clean.pop("masked_name",None)
            clean.pop("response_metadata",None)
            clean.pop("makeData",None)
            clean.pop("modelData",None)
            clean.pop("latest_by",None)
            return clean
        return None
    except:
        return None

def fetch_workers(rc):
    try:
        r = requests.get(f"https://vehicleinfo.noobgamingv40.workers.dev/fetch?vehicle_number={rc}",
                        headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        return r.json()
    except:
        return None

def fetch_carhayhaha(rc):
    try:
        r = requests.get(f"https://carhayhaha.onrender.com/api/vehicle?vehicle={rc}", timeout=15)
        return r.json()
    except:
        return None

def fetch_mobile(rc):
    try:
        r = requests.get(f"https://bronx-web-api.onrender.com/api/key-bronx/veh2num?key=op&vehicle={rc}", timeout=10)
        d = r.json()
        for k in ['mobile_number','mobile','phone','number']:
            if d.get(k): return str(d[k])
        return None
    except:
        return None

def fetch_vahanx(rc):
    try:
        r = requests.get(f"https://vahanx.in/rc-search/{rc}", headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        def gv(l):
            try:
                s=soup.find("span",string=l)
                return s.find_parent("div").find("p").get_text(strip=True) if s else None
            except: return None
        d = {
            "owner_name":gv("Owner Name"),"father_name":gv("Father's Name"),
            "phone":gv("Phone"),"address":gv("Address"),"city":gv("City Name"),
            "rto":gv("Registered RTO"),"reg_date":gv("Registration Date"),
            "model":gv("Model Name"),"fuel":gv("Fuel Type"),
            "insurance":gv("Insurance Company"),"insurance_upto":gv("Insurance Upto"),
            "fitness_upto":gv("Fitness Upto"),"tax_upto":gv("Tax Upto"),
        }
        return {k:v for k,v in d.items() if v} if any(d.values()) else None
    except:
        return None


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
    
    # Sequential fetch
    um = fetch_ummmym(rc)
    wk = fetch_workers(rc)
    ch = fetch_carhayhaha(rc)
    mb = fetch_mobile(rc)
    vx = fetch_vahanx(rc)
    
    rt = round(time.time()-start, 2)
    
    # 🔥 CLEAN MERGED RESPONSE - NO SOURCE NAMES
    resp = {
        "status": "success",
        "rc_number": rc,
        "credit": CREDIT,
        "response_time": rt,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # OWNER DETAILS
    resp["owner_name"] = (
        (um.get("owner_name") if um else None) or
        (ch.get("owner",{}).get("name") if ch else None) or
        (wk.get("owner_name") if wk else None) or
        (vx.get("owner_name") if vx else None) or "N/A"
    )
    resp["father_name"] = (
        (um.get("father_name") if um else None) or
        (ch.get("owner",{}).get("father_name") if ch else None) or
        (vx.get("father_name") if vx else None) or ""
    )
    resp["mobile_number"] = mb or (um.get("mobile_number") if um else None) or (vx.get("phone") if vx else None) or "N/A"
    
    # VEHICLE DETAILS
    resp["manufacturer"] = (
        (um.get("maker_description") if um else None) or
        (ch.get("vehicle",{}).get("manufacturer") if ch else None) or "N/A"
    )
    resp["model"] = (
        (um.get("maker_model") if um else None) or
        (ch.get("vehicle",{}).get("model") if ch else None) or
        (vx.get("model") if vx else None) or "N/A"
    )
    resp["variant"] = (
        (ch.get("vehicle",{}).get("variant") if ch else None) or "N/A"
    )
    resp["fuel_type"] = (
        (um.get("fuel_type") if um else None) or
        (ch.get("vehicle",{}).get("fuel") if ch else None) or
        (vx.get("fuel") if vx else None) or "N/A"
    )
    resp["vehicle_class"] = (
        (um.get("vehicle_category_description") if um else None) or
        (ch.get("vehicle",{}).get("class") if ch else None) or "N/A"
    )
    resp["body_type"] = (um.get("body_type") if um else None) or "N/A"
    resp["color"] = (um.get("color") if um else None) or "N/A"
    resp["seating_capacity"] = (
        (um.get("seat_capacity") if um else None) or
        (ch.get("vehicle",{}).get("seating") if ch else None) or "N/A"
    )
    resp["cubic_capacity"] = (um.get("cubic_capacity") if um else None) or "N/A"
    resp["vehicle_gross_weight"] = (um.get("vehicle_gross_weight") if um else None) or "N/A"
    resp["wheelbase"] = (um.get("wheelbase") if um else None) or "N/A"
    resp["norms_type"] = (um.get("norms_type") if um else None) or "N/A"
    
    # IDENTIFICATION
    resp["chassis_number"] = (
        (um.get("vehicle_chasi_number") if um else None) or
        (ch.get("identification",{}).get("chassis") if ch else None) or "N/A"
    )
    resp["engine_number"] = (
        (um.get("vehicle_engine_number") if um else None) or
        (ch.get("identification",{}).get("engine") if ch else None) or "N/A"
    )
    
    # REGISTRATION
    resp["registration_date"] = (
        (um.get("registration_date") if um else None) or
        (ch.get("registration",{}).get("date") if ch else None) or
        (vx.get("reg_date") if vx else None) or "N/A"
    )
    resp["registered_at"] = (
        (um.get("registered_at") if um else None) or
        (ch.get("registration",{}).get("authority") if ch else None) or "N/A"
    )
    resp["rto_name"] = (
        (ch.get("registration",{}).get("rto") if ch else None) or
        (vx.get("rto") if vx else None) or "N/A"
    )
    resp["rto_code"] = (
        (um.get("rto_code") if um else None) or
        (ch.get("registration",{}).get("rto_code") if ch else None) or "N/A"
    )
    resp["manufacturing_date"] = (um.get("manufacturing_date_formatted") if um else None) or "N/A"
    resp["rc_status"] = (um.get("rc_status") if um else None) or "N/A"
    resp["owner_number"] = (um.get("owner_number") if um else None) or "N/A"
    
    # INSURANCE
    resp["insurance_company"] = (
        (um.get("insurance_company") if um else None) or
        (ch.get("insurance",{}).get("company") if ch else None) or
        (vx.get("insurance") if vx else None) or "N/A"
    )
    resp["insurance_policy_number"] = (
        (um.get("insurance_policy_number") if um else None) or
        (ch.get("insurance",{}).get("policy_no") if ch else None) or "N/A"
    )
    resp["insurance_valid_upto"] = (
        (um.get("insurance_upto") if um else None) or
        (ch.get("insurance",{}).get("valid_upto") if ch else None) or
        (vx.get("insurance_upto") if vx else None) or "N/A"
    )
    
    # FITNESS & TAX
    resp["fit_up_to"] = (um.get("fit_up_to") if um else None) or "N/A"
    resp["tax_valid_upto"] = (
        (um.get("tax_upto") if um else None) or
        (vx.get("tax_upto") if vx else None) or "N/A"
    )
    resp["fitness_valid_upto"] = (vx.get("fitness_upto") if vx else None) or "N/A"
    
    # PUC
    resp["puc_number"] = (um.get("pucc_number") if um else None) or "N/A"
    resp["puc_valid_upto"] = (um.get("pucc_upto") if um else None) or "N/A"
    
    # FINANCIER
    resp["financier"] = (
        (um.get("financer") if um else None) or
        (ch.get("financier",{}).get("name") if ch else None) or "N/A"
    )
    
    # ADDRESS
    resp["present_address"] = (
        (um.get("present_address") if um else None) or
        (ch.get("address",{}).get("present") if ch else None) or
        (vx.get("address") if vx else None) or "N/A"
    )
    resp["permanent_address"] = (
        (um.get("permanent_address") if um else None) or
        (ch.get("address",{}).get("permanent") if ch else None) or "N/A"
    )
    resp["city"] = (
        (um.get("city") if um else None) or
        (ch.get("address",{}).get("city") if ch else None) or
        (vx.get("city") if vx else None) or "N/A"
    )
    resp["pincode"] = (
        (ch.get("address",{}).get("pincode") if ch else None) or "N/A"
    )
    
    # Remove N/A values (optional - comment out if you want all fields)
    resp = {k:v for k,v in resp.items() if v != "N/A" and v != ""}
    
    return jsonify(resp)


@app.route('/health')
def health():
    return jsonify({"status":"ONLINE","credit":CREDIT})


if __name__=='__main__':
    port = int(os.environ.get('PORT',3000))
    app.run(host='0.0.0.0',port=port,debug=False)
