from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_date = Column(DateTime, index=True)
    size_x = Column(Float, index=True)
    size_y = Column(Float, index=True)
    hole_diameter = Column(Integer, index=True)
    hole_coords = Column(String, index=True)
