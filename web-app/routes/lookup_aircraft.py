from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from modules.database import get_db
from database_classes.aircraft_info import Aircraft
from dependencies import get_db_session
from modules.fetch_image import get_aircraft_picture as fetch_image

router = APIRouter()

# Helper function to fetch aircraft data and image
def fetch_aircraft_data(aircraft, db_session):
    aircraft_dict = {column.name: getattr(aircraft, column.name) for column in aircraft.__table__.columns}
    image = fetch_image(aircraft_dict['hex'], aircraft_dict['registration'])
    if image:
        aircraft_dict['image'] = image
    return aircraft_dict

# Unified function to get aircraft by hex, tail number, or registration
@router.get("/{identifier}")
def get_aircraft(identifier: str, db: Session = Depends(get_db_session)):
    identifier = identifier.strip()
    
    try:
        # Attempt to find aircraft by hex code
        aircraft = db.query(Aircraft).filter_by(hex=identifier.lower()).first()
        if aircraft:
            return fetch_aircraft_data(aircraft, db)
        
        
        # Attempt to find aircraft by registration
        aircraft = db.query(Aircraft).filter_by(registration=identifier.upper()).first()
        if aircraft:
            return fetch_aircraft_data(aircraft, db)
        
        # Attempt to find aircraft by flight
        aircraft = db.query(Aircraft).filter_by(flight=identifier.upper()).first()
        if aircraft:
            return fetch_aircraft_data(aircraft, db)

        # If no aircraft is found, return None
        return {"detail": "Aircraft not found"}
    
    except SQLAlchemyError as e:
        # Rollback the transaction and handle the error
        db.rollback()
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()
