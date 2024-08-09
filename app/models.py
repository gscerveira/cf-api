from sqlalchemy import Column, Integer, String, JSON, Date
from .database import Base

class CalibrationFile(Base):
    __tablename__ = "calibration_files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    pandora_id = Column(Integer, index=True)
    spectrometer_id = Column(Integer)
    version = Column(Integer)
    validity_date = Column(Date)
    content = Column(JSON)