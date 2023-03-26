#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="state", cascade="all,delete")
    else:
        @property
        def cities(self):
            """Return list of cities with state_id equal to current state_id"""
            from models import storage
            return [city for city in storage.all("City").values() if city.state_id == self.id]
