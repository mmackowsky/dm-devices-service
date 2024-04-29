from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status

from config import get_settings
from database import SessionLocal, engine
from models import Device
from schemas import DeviceForm
from utils import set_new_id

settings = get_settings()
app = FastAPI()
db = SessionLocal()


@app.post("/api/devices", status_code=status.HTTP_201_CREATED)
async def add_device(device_form: DeviceForm, request: Request):
    name = db.query(Device).filter(Device.name == device_form.name).first()
    if name:
        raise HTTPException(
            detail="Device already exists", status_code=status.HTTP_409_CONFLICT
        )

    device = Device(
        id=set_new_id(db),
        user=int(request.headers.get("request-user-id")),
        name=device_form.name,
        producer=device_form.producer,
        description=device_form.description,
    )

    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@app.get("/api/devices", status_code=status.HTTP_200_OK)
async def get_devices(request: Request):
    return db.query(Device).all()


@app.get("/api/devices/{id}", status_code=status.HTTP_200_OK)
async def get_device_by_id(request: Request, id: int):
    return db.query(Device).filter(Device.id == id).first()


@app.delete("/api/devices/{id}", status_code=status.HTTP_200_OK)
async def delete_device(request: Request, id: int):
    device = db.query(Device).filter(Device.id == id).first()
    if not device:
        raise HTTPException(
            detail="Device not found", status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully."}


if __name__ == "__main__":
    Device.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
