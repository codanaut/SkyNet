from sqlalchemy import create_engine, text, exc, DateTime
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float, Boolean, Date
from datetime import datetime, timezone
import os

# Define your Base model
Base = declarative_base()

class Watchlist(Base):
    __tablename__ = 'watchlist'

    hex = Column(String, primary_key=True)  # Unique identifier for the aircraft, often the Mode S code.
    tail_number = Column(String)
    description = Column(String)
    alert = Column(Boolean)
    alert_location = Column(String)

# Your Aircraft model
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
    messages = Column(Integer)  # Number of ADS-B messages received.
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

# Function to create database if it doesn't exist
def create_database(engine_url, database_name):
    """Create PostgreSQL database if it does not exist."""
    engine = create_engine(engine_url, isolation_level='AUTOCOMMIT', connect_args={'connect_timeout': 10})
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

# Function to check and create tables in the database
def check_and_create_table(db_url):
    engine = create_engine(db_url)
    
    inspector = inspect(engine)
    if 'aircraft' not in inspector.get_table_names():
        print("Creating Aircraft table...")
        Aircraft.__table__.create(engine, checkfirst=True)

    if 'watchlist' not in inspector.get_table_names():
        print("Creating watchlist...")
        Watchlist.__table__.create(engine, checkfirst=True)
    

# Check if required environment variables are already set
def check_and_load_env_variables():
    required_variables = ['user', 'password', 'host', 'database_name']
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

# Call the function to check and load environment variables
check_and_load_env_variables()

# Retrieve environment variables
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
database_name = os.getenv('database_name')

# Build the initial engine URL to connect to the server (without a database)
server_url = f"postgresql://{user}:{password}@{host}/postgres"

# Create the database if it doesn't exist
create_database(server_url, database_name)

# Build the database URL for the actual database connection
db_url = f"postgresql://{user}:{password}@{host}/{database_name}"

# Step 2: Create the table if it doesn't exist
check_and_create_table(db_url)
