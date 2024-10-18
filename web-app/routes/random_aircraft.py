import random
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from modules.database import get_db
from database_classes.aircraft_info import Aircraft
from dependencies import get_db_session
from modules.fetch_image import get_aircraft_picture as fetch_image

router = APIRouter()

# Function to get a random aircraft
@router.get("")
def get_random_aircraft(db: Session = Depends(get_db_session)):
    
    session = db
    try:
        # Query all hex codes from the Aircraft table
        hex_codes = session.query(Aircraft.hex).all()
        if not hex_codes:
            raise HTTPException(status_code=404, detail="No aircraft data found")
        
        # Randomly select one hex code
        random_hex_code = random.choice(hex_codes)[0]  # hex_codes is a list of tuples, so we take the first item
        print(random_hex_code)
        
        # Now proceed with the aircraft lookup logic
        aircraft = session.query(Aircraft).filter_by(hex=random_hex_code).first()
        if aircraft:
            aircraft_dict = {column.name: getattr(aircraft, column.name) for column in aircraft.__table__.columns}
            image = fetch_image(aircraft_dict['hex'], aircraft_dict['registration'])
            if image:
                aircraft_dict['image'] = image
            return aircraft_dict
        else:
            raise HTTPException(status_code=404, detail="Aircraft not found")
    
    except SQLAlchemyError as e:
        # Rollback the transaction and handle the error
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
    finally:
        session.close()
