from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from . import models, crud
from .database import SessionLocal, engine
import os
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/parse_calibration_files/")
def parse_calibration_files(db: Session = Depends(get_db)):
    calibration_folder = "calibration_files"
    if not os.path.exists(calibration_folder):
        raise HTTPException(status_code=404, detail="Calibration files folder not found")
    
    files = [f for f in os.listdir(calibration_folder) if f.endswith('.txt')]
    parsed_files = []
    
    for file in files:
        file_path = os.path.join(calibration_folder, file)
        cf_data = crud.parse_and_store_calibration_file(db, file_path)
        parsed_files.append(cf_data)
        print(f"Parsed: {file}")
        
    return {"message": f"Parsed {len(parsed_files)} calibration files"}

@app.get("/calibration_files/")
def query_calibration_files(
    db: Session = Depends(get_db),
    filename: Optional[str] = Query(None),
    pandora_id: Optional[int] = Query(None),
    spectrometer_id: Optional[int] = Query(None),
    version: Optional[int] = Query(None),
    validity_date: Optional[str] = Query(None),
    key: Optional[str] = Query(None),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0)    
):
    return crud.query_calibration_files(db, filename, pandora_id, spectrometer_id, version, validity_date, key, limit, offset)