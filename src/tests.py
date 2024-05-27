import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings
from database import get_db
from main import app
from models import Device

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Device.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class TestDevicesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.client = TestClient(app)
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

    def tearDown(self):
        db = TestingSessionLocal()
        db.query(Device).delete()
        db.commit()
        db.close()

    def test_get_devices(self):
        response = self.client.get("/api/devices")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_get_device_by_id(self):
        response = self.client.get("/api/devices/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_delete_device(self):
        response = self.client.delete("/api/devices/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")


if __name__ == "__main__":
    unittest.main()
