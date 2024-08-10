from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, crud
from .database import SessionLocal, engine
import os

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
        
    return {"message": f"Parsed {len(parsed_files)} calibration files"}

@app.get("/get_calibration_key/")
def get_calibration_files(key: str, db: Session = Depends(get_db)):
    results = crud.query_calibration_files(db, key)
    return results

@app.get("/calibration_file/{filename}")
def get