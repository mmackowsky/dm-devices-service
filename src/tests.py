import unittest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from config import get_settings
from database import Base, get_db
from main import app
from src.models import Device

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
db = TestingSessionLocal()
energy = Device(
    id=1,
    user=1,
    name="DeviceName",
    producer="DeviceProducer",
    description="DeviceDescription",
)
db.add(energy)
db.commit()
db.refresh(energy)


print(db.query(Device).all())


class TestEnergyAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_devices(self):
        response = self.client.get("/api/devices")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_get_device_by_id(self):
        response = self.client.get("/api/devices/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")


if __name__ == "__main__":
    unittest.main()
