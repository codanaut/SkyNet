from sqlalchemy import create_engine, Column, String, Integer, Float, Text, MetaData, exc, DateTime, Boolean, BIGINT, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
import requests
import json
import time
from datetime import datetime, timezone, timedelta
import sqlite3
import threading
import os

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'

    name = Column(String, primary_key=True, unique=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    range = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=True)
    in_progress = Column(Boolean, nullable=False, default=False)

class Aircraft(Base):
    __tablename__ = 'aircraft'

    hex = Column(String, primary_key=True)  # Unique identifier for the aircraft, often the Mode S code.
    flight = Column(String)  # Flight number.
    registration = Column(String)  # Aircraft registration number.
    
    description = Column(String)  # Description of the aircraft.
    aircraft_type = Column(String)  # Type of aircraft (e.g., CRJ9 for CRJ-900).
    owner = Column(String)  # Aircraft's operator or owner.
    
    #Aircraft Info
    serial_number = Column(String) # aircraft serial number assigned to the aircraft by the manufacturer
    aircraft_manufacturer = Column(String) # code assigned to the aircraft manufacturer, model and series.
    aircraft_model = Column(String) # Model of aircraft
    number_seats = Column(Integer)
    number_engines = Column(Integer)
    engine_manufacturer = Column(String) # code assigned to the engine manufacturer and model
    engine_model = Column(String)
    type_engine = Column(String)
    year_mfr = Column(String) # Year manufactured.
    type_aircraft = Column(String)
    kit_mfr = Column(String)
    kit_model = Column(String)
    manufacturer_code = Column(String)
    engine_code = Column(String)

    #Registrion Info
    type_registrant = Column(String)
    country = Column(String)
    street = Column(String)
    street2 = Column(String)
    city = Column(String)
    county = Column(String)
    state = Column(String)
    zip_code = Column(String)
    region = Column(String)
    last_action_date = Column(Date)
    cert_issue_date = Column(Date)
    certification = Column(String)
    status_code = Column(String)
    fract_owner = Column(String)
    other_names1 = Column(String)
    other_names2 = Column(String)
    other_names3 = Column(String)
    other_names4 = Column(String)
    other_names5 = Column(String)
    air_worth_date = Column(Date)
    expiration_date = Column(Date)
    mode_s_code_oct = Column(String)
    unique_id = Column(String)

    # ADSB Info
    alt_baro = Column(Integer)  # Barometric altitude (feet).
    alt_geom = Column(Integer)  # Geometric altitude (feet).
    ground_speed = Column(Float)  # Ground speed (knots).
    ias = Column(Float)  # Indicated airspeed (knots).
    tas = Column(Float)  # True airspeed (knots).
    mach = Column(Float)  # Mach number.
    wind_dir = Column(Integer)  # Wind direction (degrees from true north).
    wind_speed = Column(Integer)  # Wind speed (knots).
    oat = Column(Integer)  # Outside air temperature (Celsius).
    tat = Column(Integer)  # Total air temperature (Celsius).
    track = Column(Float)  # Direction of aircraft movement (degrees from true north).
    track_rate = Column(Float)  # Rate of change in track direction.
    roll = Column(Float)  # Roll angle (degrees).
    mag_heading = Column(Float)  # Magnetic heading (degrees).
    true_heading = Column(Float)  # True heading (degrees).
    baro_rate = Column(Float)  # Barometric rate of climb/descent (feet per minute).
    geom_rate = Column(Float)  # Geometric rate of climb/descent (feet per minute).
    squawk = Column(String)  # Squawk code (transponder code for ATC).
    emergency = Column(String)  # Emergency status.
    category = Column(String)  # Aircraft size/category.
    category_description= Column(String)
    nav_qnh = Column(Float)  # Atmospheric pressure adjusted to mean sea level (hPa).
    nav_altitude_mcp = Column(Integer)  # Altitude set in the aircraft's MCP (Mode Control Panel).
    nav_heading = Column(Integer) 
    nav_modes = Column(String )
    latitude = Column(Float)  # Latitude position.
    longitude = Column(Float)  # Longitude position.
    nic = Column(Integer)  # Navigation integrity category.
    rc = Column(Integer)  # Horizontal containment radius limit.
    seen_pos = Column(Float)  # Time since last position update.
    version = Column(Integer)  # Version of ADS-B.
    nic_baro = Column(Integer)  # Barometric pressure setting source integrity level.
    nac_p = Column(Integer)  # Navigation accuracy category for position.
    nac_v = Column(Integer)  # Navigation accuracy category for velocity.
    sil = Column(Integer)  # Source integrity level.
    sil_type = Column(String)  # Source integrity level type (measured per flight hour or per sample).
    gva = Column(Integer)  # Geometric vertical accuracy.
    sda = Column(Integer)  # System design assurance.
    alert = Column(Boolean)  # Alert flag (if the pilot has set an alert).
    spi = Column(Boolean)  # Special position identification (indicates an emergency or priority status).
    mlat = Column(String)  # Multilateration data (lists if position was derived from multilateration).
    tisb = Column(String)  # Traffic Information Service Broadcast (indicates if data comes from TIS-B).
    messages = Column(BIGINT)  # Number of ADS-B messages received.
    seen = Column(Float)  # Time since last update received.
    rssi = Column(Float)  # Received signal strength indicator.
    distance = Column(Float)  # Distance from the receiver (kilometers).
    direction = Column(Float)  # Direction of the aircraft from the receiver (degrees).
    dbFlags = Column(String) 
    source_type = Column(String)  # Type of ADS-B report.
    current_receiver_location = Column(String)
    last_receiver_location = Column(String)
    first_seen = Column(DateTime, default=datetime.now(timezone.utc))  # When the record was first seen.
    # Last Updated
    last_updated = Column(String)  # When the record was last updated.
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))  # Timestamp of the data entry.

def setup_database(engine):
    Base.metadata.create_all(engine)
    #create Location DB if not existing
    seed_locations(engine)

# Create skynet DB if not there
def create_database(engine, database_name):
    """Create PostgreSQL database if it does not exist."""
    engine = create_engine(engine, isolation_level='AUTOCOMMIT', connect_args={'connect_timeout': 10})
    conn = engine.connect()
    try:
        db_exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{database_name}'")).scalar()
        if db_exists:
            print(f"Database {database_name} already exists.")
        else:
            try:
                conn.execute(text(f"CREATE DATABASE {database_name}"))
                print(f"Database {database_name} created successfully.")
            except exc.ProgrammingError as e:
                print(f"Failed to create database {database_name}: {str(e)}")
    finally:
        conn.close()

def seed_locations(engine):
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    try:
        # Check if locations are already present to avoid duplicate seeding
        existing_count = session.query(Location).count()
        if existing_count == 0:
            locations = [
                ("LAX Airport, Los Angeles, CA", 33.9416, -118.4085, 50),
                ("DEN Airport, Denver, CO", 39.8561, -104.6737, 100),
                ("JFK Airport, New York, NY", 40.6413, -73.7781, 50),
                ("MIA Airport, Miami, FL", 25.7959, -80.2870, 100),
                ("DFW Airport, Dallas, TX", 32.8998, -97.0403, 50)
            ]
            for name, latitude, longitude, range_ in locations:
                location = Location(name=name, latitude=latitude, longitude=longitude, range=range_)
                session.add(location)
            session.commit()
            print("Seeded initial locations successfully.")
        else:
            print("Locations table already has data, skipping seeding.")
    except exc.SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding locations: {e}")
    finally:
        session.close()


def find_country_by_registration(registration):
    filepath = "aircraft-country-codes.json"
    
    def load_data(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    data = load_data(filepath)
    # Create a dictionary for quick lookup from registration codes to country
    prefix_lookup = {entry['code']: entry['country'] for entry in data['registrations']}
    # Special identifier for UK military when handling ambiguous 'ZK' and 'ZM'
    special_uk_military = "UK Military"

    # Extract the registration prefix from the registration number
    def extract_prefix(reg_number):
        # Handle UK military codes 'ZK' and 'ZM' specifically
        if reg_number.startswith(("ZK", "ZM")):
            # If followed by numeric characters, assign special UK military identifier
            if len(reg_number) > 2 and reg_number[2:].isdigit():
                return special_uk_military

        # Ignore purely numeric registrations
        if reg_number.isdigit():
            return None

        # Find the position of the hyphen (if any)
        hyphen_index = reg_number.find('-')
        if hyphen_index != -1:
            # Consider prefix up to the hyphen
            prefix_part = reg_number[:hyphen_index]
        else:
            # No hyphen, consider the full registration number or its subsets
            prefix_part = reg_number

        # Check for the longest possible matching prefix
        for i in range(min(3, len(prefix_part)), 0, -1):
            if prefix_part[:i] in prefix_lookup:
                return prefix_part[:i]
        return None

    # Find the country based on the registration prefix
    def get_country(prefix):
        if prefix == special_uk_military:
            return "United Kingdom (Military)"
        elif prefix:
            return prefix_lookup.get(prefix, "N/A")
        return "N/A"

    prefix = extract_prefix(registration)
    return get_country(prefix)


def get_category_description(type_code):
    aircraft_types = {
        "A0": "Unspecified powered aircraft",
        "A1": "Light (< 15 500 lbs.)",
        "A2": "Small (15 500 to 75 000 lbs.)",
        "A3": "Large (75 000 to 300 000 lbs.)",
        "A4": "High Vortex Large",
        "A5": "Heavy (> 300 000 lbs.)",
        "A6": "High Performance (> 5 g acceleration and > 400kts)",
        "A7": "Rotorcraft",
        "B0": "Unspecified unpowered aircraft or UAV or spacecraft",
        "B1": "Glider/sailplane",
        "B2": "Lighter-than-Air",
        "B3": "Parachutist/Skydiver",
        "B4": "Ultralight/hang-glider/paraglider",
        "B5": "Reserved",
        "B6": "Unmanned Aerial Vehicle",
        "B7": "Space/Trans-atmospheric vehicle",
        "C0": "Unspecified ground installation or vehicle",
        "C1": "Surface Vehicle - Emergency Vehicle",
        "C2": "Surface Vehicle - Service Vehicle",
        "C3": "Fixed Ground or Tethered Obstruction"
    }
    
    return aircraft_types.get(type_code, "Unknown aircraft type")

def fetch_and_update(engine, url, location):
    api_url = url
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
        else:
            print("Failed to fetch data: HTTP Status", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    ac_data = data['aircraft'] if 'aircraft' in data else data['ac']

    for aircraft in ac_data:
        hex_code = aircraft.get('hex')
        if not hex_code or hex_code.startswith('~'):
            continue

        existing = session.query(Aircraft).filter_by(hex=hex_code).first()
        try:
            if not existing:
                existing = Aircraft(hex=hex_code)
                existing.first_seen = datetime.now(timezone.utc)
                session.add(existing)
                #print(f"Added new aircraft: {hex_code}")

            # Set Custom Varibles

            dbFlags = 'Military' if aircraft.get('dbFlags') == 1 else 'LADD' if aircraft.get('dbFlags') == 8 else 'PIA' if aircraft.get('dbFlags') == 4 else str(aircraft.get('dbFlags', 'N/A'))
            if dbFlags == "Military":
                country = "Military"
            else:
                registration = aircraft.get('r') if aircraft.get('r') else 'N/A'
                country = find_country_by_registration(registration) if registration is not None else 'Not Found'

            if existing.current_receiver_location != location or existing.current_receiver_location in [None, 'N/A']:
                existing.last_receiver_location = existing.current_receiver_location
                existing.current_receiver_location = location


            # Ensure that updates to current_location and last_location are done as needed



            alt_baro =aircraft.get('alt_baro', 0)
            if alt_baro == "ground":
                    alt_baro = 0 
            
            category = aircraft.get('category', '') if aircraft.get('category') else 'N/A'

            # -----------------

            updates = []
            attributes = {
                'flight': aircraft.get('flight', 'N/A').strip(),
                'registration': aircraft.get('r', 'N/A'),
                'description': aircraft.get('desc', 'N/A'),
                'aircraft_type': aircraft.get('t', 'N/A'),
                'owner': aircraft.get('ownOp', 'N/A'),
                'year_mfr': aircraft.get('year', 'N/A'),
                'country': country,
                'alt_baro': alt_baro,
                'alt_geom': aircraft.get('alt_geom', 0),
                'ground_speed': aircraft.get('gs', 0.0),
                'ias': aircraft.get('ias', 0.0),
                'tas': aircraft.get('tas', 0.0),
                'mach': aircraft.get('mach', 0.0),
                'wind_dir': aircraft.get('wd', 0),
                'wind_speed': aircraft.get('ws', 0),
                'oat': aircraft.get('oat', 0),
                'tat': aircraft.get('tat', 0),
                'track': aircraft.get('track', 0.0),
                'track_rate': aircraft.get('track_rate', 0.0),
                'roll': aircraft.get('roll', 0.0),
                'mag_heading': aircraft.get('mag_heading', 0.0),
                'true_heading': aircraft.get('true_heading', 0.0),
                'baro_rate': aircraft.get('baro_rate', 0.0),
                'geom_rate': aircraft.get('geom_rate', 0.0),
                'squawk': aircraft.get('squawk', 'N/A'),
                'emergency': aircraft.get('emergency', 'N/A'),
                'category':  aircraft.get('category', 'N/A'),
                'category_description': get_category_description(category),
                'nav_qnh': aircraft.get('nav_qnh', 1013.25),  # Standard sea-level pressure in hPa
                'nav_altitude_mcp': aircraft.get('nav_altitude_mcp', 0),
                'nav_heading': aircraft.get('nav_heading', 0.0),
                'nav_modes': aircraft.get('nav_modes', 'N/A'),
                'latitude': aircraft.get('lat', 0.0),
                'longitude': aircraft.get('lon', 0.0),
                'nic': aircraft.get('nic', 0),
                'rc': aircraft.get('rc', 0),
                'seen_pos': aircraft.get('seen_pos', 0.0),
                'version': aircraft.get('version', 0),
                'nic_baro': aircraft.get('nic_baro', 0),
                'nac_p': aircraft.get('nac_p', 0),
                'nac_v': aircraft.get('nac_v', 0),
                'sil': aircraft.get('sil', 0),
                'sil_type': aircraft.get('sil_type', 'N/A'),
                'gva': aircraft.get('gva', 0),
                'sda': aircraft.get('sda', 0),
                'alert': aircraft.get('alert', False),
                'spi': aircraft.get('spi', False),
                'mlat': aircraft.get('mlat', 'N/A'),
                'tisb': aircraft.get('tisb', 'N/A'),
                'messages': aircraft.get('messages', 0),
                'seen': aircraft.get('seen', 0.0),
                'rssi': aircraft.get('rssi', 0.0),
                'distance': aircraft.get('dst', 0.0),
                'direction': aircraft.get('dir', 0.0),
                'source_type': aircraft.get('type', 'N/A'),
                'dbFlags': dbFlags,
                'current_receiver_location': existing.current_receiver_location if existing else 'N/A',
                'last_receiver_location': existing.last_receiver_location if existing else 'N/A',
                'last_updated': aircraft.get('last_updated', 'N/A'),
                'timestamp': datetime.now(timezone.utc),
            }

            # Iterate over each attribute and update if necessary
            for attr, new_value in attributes.items():
                if getattr(existing, attr, None) != new_value:
                    updates.append(f"{attr} - {getattr(existing, attr, 'N/A')} -> {new_value}")
                    setattr(existing, attr, new_value)

            if updates:
                if not existing.first_seen:
                    existing.first_seen = datetime.now(timezone.utc)  # Set first_seen if not already set
                existing.last_updated = datetime.now().strftime('%m/%d/%Y %I:%M %p')
                existing.timestamp = datetime.now(timezone.utc)
                session.commit()
                #print(f"Updated {hex_code}")

        except IntegrityError:
            session.rollback()
            print(f"Aircraft with hex {hex_code} already exists. Rolling back.")

    session.close()
    #print(f"Update completed: {location} - {datetime.now().strftime('%I:%M %p')}")

def with_retries(engine, function, max_retries=5, backoff_factor=1):
    retries = 0
    while retries < max_retries:
        try:
            function(engine)
            return
        except (exc.OperationalError, exc.DisconnectionError) as e:
            retries += 1
            wait_time = backoff_factor * (2 ** retries)
            print(f"Database error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    print("Max retries exceeded. Exiting.")
    raise Exception("Max retries exceeded")


def reset_stuck_locations(engine):
    """
    Reset locations that are stuck with in_progress=True and have not been updated for a long time.
    This is useful in case the script gets stopped mid-update and locations remain locked.
    """
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    try:
        threshold_time = datetime.now(timezone.utc) - timedelta(minutes=4)  # Define a threshold time for "stuck" locations
        stuck_locations = session.query(Location).filter(
            Location.in_progress == True,
            Location.last_updated < threshold_time
        ).all()
        for location in stuck_locations:
            location.in_progress = False
            print(f"Resetting stuck location: {location.name}")
        session.commit()
    except exc.SQLAlchemyError as e:
        session.rollback()
        print(f"Error resetting stuck locations: {e}")
    finally:
        session.close()

def get_oldest_location(session, worker_id):
    try:
        # Define the threshold time of two minutes ago
        two_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=2)

        # Query to fetch the location that hasn't been updated recently and is not in progress
        location = (
            session.query(Location)
            .filter(
                (Location.last_updated == None) | (Location.last_updated < two_minutes_ago),
                Location.in_progress == False
            )
            .order_by(Location.last_updated.nullsfirst())  # Order by last_updated to get the oldest one first, handle nulls
            .with_for_update(skip_locked=True)  # Add row-level locking to prevent workers from picking the same record
            .first()
        )

        if location:
            # Mark the location as in progress to ensure no other worker picks it
            location.in_progress = True
            location.last_updated = datetime.now(timezone.utc)  # Set last_updated to current time to avoid re-picking
            session.commit()  # Commit the changes to the database
            return location
        else:
            print(f"Worker {worker_id}: No locations older than 2 minutes found, sleeping...")
            time.sleep(120)  # Sleep for 2 minutes if no suitable location is found
    except exc.SQLAlchemyError as e:
        session.rollback()
        print(f"Error fetching oldest location: {e}")
    return None



def update_location(engine, location, worker_id, api):
    if api == "adsbfi":
        url = f"https://opendata.adsb.fi/api/v2/lat/{location.latitude}/lon/{location.longitude}/dist/{location.range}"
    elif api == "airplaneslive":
        url = f"https://api.airplanes.live/v2/point/{location.latitude}/{location.longitude}/{location.range}"
    else:
        print("No valid API specified.")
        exit()
    

    try:
        # Fetch and update data using the provided URL
        with_retries(engine, lambda engine: fetch_and_update(engine, url, location.name))
        
        # Update the location's last_updated timestamp and mark it as not in progress
        Session = sessionmaker(bind=engine, expire_on_commit=False)
        session = Session()
        try:
            loc = session.query(Location).filter_by(name=location.name).first()
            if loc:
                loc.last_updated = datetime.now(timezone.utc)
                loc.in_progress = False
                session.commit()
                print(f"Worker {worker_id}: Update completed and unlocked: {location.name}")
            else:
                print(f"Error: Location {location.name} not found when trying to update.")
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating location timestamp: {e}")
        finally:
            session.close()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while updating {location.name}: {e}")

# Login to PG
# Check if required environment variables are already set
def check_and_load_env_variables():
    required_variables = ['user', 'password', 'host', 'database_name', 'api']
    missing_variables = [var for var in required_variables if not os.getenv(var)]

    # If any required variables are missing, load from .env file
    if missing_variables:
        load_dotenv('.env')

    # After attempting to load from .env, check if variables are still missing
    still_missing_variables = [var for var in required_variables if not os.getenv(var)]
    if still_missing_variables:
        raise ValueError(f"Missing required environment variables: {', '.join(still_missing_variables)}")

# Function to load environment variables from a .env file
def load_dotenv(filepath):
    try:
        with open(filepath) as f:
            for line in f:
                # Ignore comments and empty lines
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    # Only set the variable if it's not already set
                    if not os.getenv(key):
                        os.environ[key] = value
    except FileNotFoundError:
        print(f"Warning: .env file not found at {filepath}")


def main():
    check_and_load_env_variables()
    user = os.getenv('user')
    password = os.getenv('password')
    host = os.getenv('host')
    database_name = os.getenv('database_name')
    api = os.getenv('api')
    
    engine_url = f'postgresql://{user}:{password}@{host}/'
    full_engine = create_engine(f'{engine_url}{database_name}', pool_pre_ping=True, pool_recycle=3600, pool_timeout=30)
    
    # Create DB if not existing
    create_database(engine_url, database_name)
    
    
    setup_database(full_engine)

    print(f"API Set As: {api}")
    

    def worker(worker_id):
        time.sleep(worker_id * 5)  # Add a delay based on worker ID to stagger their start times
        while True:
            # Create a new session for each worker iteration to ensure updated information
            Session = sessionmaker(bind=full_engine, expire_on_commit=False)
            session = Session()
            reset_stuck_locations(full_engine)

            try:
                location = get_oldest_location(session,worker_id)
                if location:
                    print(f"Worker {worker_id}: Fetching data for: {location.name}")
                    update_location(full_engine, location, worker_id, api)
                
                    

                time.sleep(5)  # Slight delay to prevent hammering the database too hard
            except exc.SQLAlchemyError as e:
                session.rollback()
                print(f"Worker {worker_id}: Error during processing: {e}")
            finally:
                session.close()


    # Start multiple threads to handle different locations concurrently
    num_threads = 5  # Adjust this number as needed
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
