from fastapi import FastAPI, HTTPException 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
from pathlib import Path
import json
from datetime import datetime
import os
from typing import Dict, Optional
from datetime import datetime
import random
import string

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
DATA_FILE = 'deliveries.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'deliveries': {}, 'status_history': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

if not os.path.exists(DATA_FILE):
    save_data({'deliveries': {}, 'status_history': {}})

def generate_tracking_code():
    digits = ''.join(random.choices(string.digits, k=6))
    return f"E{digits}PX"
templates = Jinja2Templates(directory="templates")

deliveries_db: Dict[str, dict] = {}

class Delivery(BaseModel):
    tracking_code: str
    status: str
    origin: str
    destination: str
    estimated_delivery: Optional[str] = None

class DeliveryUpdate(BaseModel):
    status: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin")
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/deliveries/")
def create_delivery(delivery: Delivery):
    data = load_data()
    if delivery.tracking_code in data['deliveries']:
        raise HTTPException(status_code=400, detail="Tracking code already exists")

    delivery_dict = delivery.model_dump()
    delivery_dict['created_at'] = datetime.now().isoformat()
    data['deliveries'][delivery.tracking_code] = delivery_dict

    if delivery.tracking_code not in data['status_history']:
        data['status_history'][delivery.tracking_code] = []
    data['status_history'][delivery.tracking_code].append({
        'status': delivery.status,
        'created_at': datetime.now().isoformat()
    })

    save_data(data)
    return delivery

@app.get("/deliveries/{tracking_code}")
def get_delivery(tracking_code: str):
    data = load_data()
    if tracking_code not in data['deliveries']:
        raise HTTPException(status_code=404, detail="Delivery not found")

    delivery = data['deliveries'][tracking_code]
    delivery['status_history'] = data['status_history'].get(tracking_code, [])
    return delivery

@app.put("/deliveries/{tracking_code}")
def update_delivery_status(tracking_code: str, update: DeliveryUpdate):
    data = load_data()
    if tracking_code not in data['deliveries']:
        raise HTTPException(status_code=404, detail="Delivery not found")

    data['deliveries'][tracking_code]['status'] = update.status
    data['status_history'][tracking_code].append({
        'status': update.status,
        'created_at': datetime.now().isoformat()
    })

    save_data(data)
    return data['deliveries'][tracking_code]

@app.delete("/deliveries/{tracking_code}")
def delete_delivery(tracking_code: str):
    data = load_data()
    if tracking_code not in data['deliveries']:
        raise HTTPException(status_code=404, detail="Delivery not found")

    del data['deliveries'][tracking_code]
    if tracking_code in data['status_history']:
        del data['status_history'][tracking_code]

    save_data(data)
    return {"message": "Delivery deleted successfully"}

@app.get("/deliveries")
def get_all_deliveries():
    data = load_data()
    return list(data['deliveries'].values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)