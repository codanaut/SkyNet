from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


from modules.database import get_db
from database_classes.aircraft_info import Aircraft
from dependencies import get_db_session
from modules.fetch_image import get_aircraft_picture as fetch_image

router = APIRouter()

# Function to get aircraft by hex code
@router.get("/{tail_number}")
def get_aircraft_by_tail(tail_number,db: Session = Depends(get_db_session)):
    
    session = db
    try:
        tail_number = tail_number.strip().upper()
        aircraft = session.query(Aircraft).filter_by(tail_number=tail_number).first()
        if aircraft:
            aircraft_dict = {column.name: getattr(aircraft, column.name) for column in aircraft.__table__.columns}
            image = fetch_image(aircraft_dict['hex'], aircraft_dict['registration'])
            if image:
                aircraft_dict['image'] = image
            return aircraft_dict
        else:
            return None
    except SQLAlchemyError as e:
        # Rollback the transaction and handle the error
        session.rollback()
        print("An error occurred:", e)
        return None
    finally:
        session.close()