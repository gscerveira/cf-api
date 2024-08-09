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