from sqlalchemy import desc

from database import SessionLocal
from models import Device


def set_new_id(db: SessionLocal):
    last_user = db.query(Device).order_by(desc(Device.id)).first()
    new_user_id = (last_user.id + 1) if last_user else 1
    return new_user_id
