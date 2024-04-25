from pydantic import BaseModel


class DeviceForm(BaseModel):
    name: str
    producer: str
    description: str
