from sqlalchemy.orm import Session
from . import models
import os
import json
from datetime import datetime
from parse import parse

def parse_filename(filename):
    # Example filename: PandoraXsY_CF_vZdYYYYMMDD.txt
    pattern = "Pandora{pandora_id:d}s{spectrometer_id:d}_CF_v{version:d}d{date}.txt"
    
    result = parse(pattern, filename)
    
    if result is None:
        raise ValueError(f"Failed to parse filename: {filename}")
    
    pandora_id = result['pandora_id']
    spectrometer_id = result['spectrometer_id']
    version = result['version']
    validity_date = datetime.strptime(result['date'], "%Y%m%d").date()
    
    return pandora_id, spectrometer_id, version, validity_date

def parse_and_store_calibration_file(db: Session, file_path: str):
    filename = os.path.basename(file_path)
    pandora_id, spectrometer_id, version, validity_date = parse_filename(filename)
    
    content = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ' -> ' in line:
                key, value = line.strip().split(' -> ')
                content[key.strip()] = value.strip()
                
    db_cf = models.CalibrationFile(
        filename=filename,
        pandora_id=pandora_id,
        spectrometer_id=spectrometer_id,
        version=version,
        validity_date=validity_date,
        content=content
    )
    db.add(db_cf)
    db.commit()
    db.refresh(db_cf)
    return db_cf

def query_calibration_files(db: Session, key: str):
    results = []
    cfs = db.query(models.CalibrationFile).all()
    for cf in cfs:
        if key in cf.content:
            results.append({
                "filename": cf.filename,
                "pandora_id": cf.pandora_id,
                "spectrometer_id": cf.spectrometer_id,
                "version": cf.version,
                "validity_date": cf.validity_date.isoformat(),
                key: cf.content[key]
            })
            
    return results

def get_calibration_file(db: Session, filename: str):
    return db.query(models.CalibrationFile).filter(models.CalibrationFile.filename == filename).first()

def get_key_from_file(db: Session, filename: str, key: str):
    cf = get_calibration_file(db, filename)
    if cf and key in cf.content:
        return {
            "filename": cf.filename,
            "pandora_id": cf.pandora_id,
            "spectrometer_id": cf.spectrometer_id,
            "version": cf.version,
            "validity_date": cf.validity_date.isoformat(),
            key: cf.content[key]
        }
    return None
    