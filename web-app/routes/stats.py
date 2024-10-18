from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, func
from sqlalchemy.orm import Session

from dependencies import get_db_session
from database_classes.aircraft_info import Aircraft

router = APIRouter()

# Function to get aircraft count
@router.get("")
def aircraft_logged_count(db: Session = Depends(get_db_session)):
    #session = db
    try:
        count = db.query(func.count(Aircraft.hex)).scalar()
        return {"count": count}
    except SQLAlchemyError as e:
        # Rollback the transaction and handle the error
        db.rollback()
        print("An error occurred:", e)
        return None
    finally:
        db.close()