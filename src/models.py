from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Device(Base):
    __tablename__ = "devices"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    producer = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return (
            f"{self.id}, {self.user}, {self.name}, {self.producer}, {self.description}"
        )
