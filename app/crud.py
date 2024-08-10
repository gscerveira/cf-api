from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models
import os
from datetime import datetime
from parse import parse
from typing import Optional

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
            if ' ->' in line:
                key, value = line.strip().split(' ->')
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

def query_calibration_files(
    db: Session,
    filename: Optional[str] = None,
    pandora_id: Optional[int] = None,
    spectrometer_id: Optional[int] = None,
    version: Optional[int] = None,
    validity_date: Optional[str] = None,
    key: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    query = db.query(models.CalibrationFile)
    
    if filename:
        query = query.filter(models.CalibrationFile.filename == filename)
    if pandora_id:
        query = query.filter(models.CalibrationFile.pandora_id == pandora_id)
    if spectrometer_id:
        query = query.filter(models.CalibrationFile.spectrometer_id == spectrometer_id)
    if version:
        query = query.filter(models.CalibrationFile.version == version)
    if validity_date:
        query = query.filter(models.CalibrationFile.validity_date == datetime.strptime(validity_date, "%Y-%m-%d").date())
    
    results = query.offset(offset).limit(limit).all()
    
    if key:
        filtered_results = []
        for cf in results:
            if key in cf.content:
                filtered_results.append({
                    "filename": cf.filename,
                    "pandora_id": cf.pandora_id,
                    "spectrometer_id": cf.spectrometer_id,
                    "version": cf.version,
                    "validity_date": cf.validity_date.isoformat(),
                    key: cf.content[key]
                })
        return filtered_results
    else:
        [{
            "filename": cf.filename,
            "pandora_id": cf.pandora_id,
            "spectrometer_id": cf.spectrometer_id,
            "version": cf.version,
            "validity_date": cf.validity_date.isoformat(),
            "content": cf.content
        } for cf in results]
    
    