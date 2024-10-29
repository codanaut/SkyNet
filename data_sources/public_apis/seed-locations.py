from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean, exc
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
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

def seed_locations(engine):
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    try:
        locations = [
            ("SNY Airport, Sidney, NE", 41.0995,-102.9827, 200),
            ("DEN Airport, Denver, CO", 39.8561, -104.6737, 100),
            ("DCA Airport, Washington D.C.", 38.8512, -77.0402, 25),
            ("JFK Airport, New York, NY", 40.6413, -73.7781, 50),
            ("LAX Airport, Los Angeles, CA", 33.9416, -118.4085, 50),
            ("ORD Airport, Chicago, IL", 41.9742, -87.9073, 50),
            ("ATL Airport, Atlanta, GA", 33.6407, -84.4277, 50),
            ("DFW Airport, Dallas, TX", 32.8998, -97.0403, 50),
            ("ABQ Airport, Albuquerque, NM", 35.0402, -106.6090, 100),
            ("MEM Airport, Memphis, TN", 35.0421, -89.9792, 100),
            ("OMA Airport, Omaha, NE", 41.3032, -95.8941, 100),
            ("BNA Airport, Nashville, TN", 36.1263, -86.6774, 100),
            ("SLC Airport, Salt Lake City, UT", 40.7899, -111.9791, 100),
            ("SEA Airport, Seattle, WA", 47.4502, -122.3088, 100),
            ("SMF Airport, Sacramento, CA", 38.6954, -121.5908, 50),
            ("PDX Airport, Portland, OR", 45.5898, -122.5973, 100),
            ("BIS Airport, Bismarck, ND", 46.7727, -100.7462, 250),
            ("JAX Airport, Jacksonville, FL", 30.4941, -81.6879, 100),
            ("RDU Airport, Raleigh-Durham, NC", 35.8776, -78.7875, 100),
            ("BZN Airport, Bozeman, MT", 45.7775, -111.1525, 100),
            ("White Sands Missile Range, NM", 32.991,-106.975, 100),
            ("LAS Airport, Las Vegas, NV", 36.0840, -115.1537, 100),
            ("MCI Airport, Kansas City, MO", 39.2976, -94.7139, 100),
            ("MSP Airport, Minneapolis, MN", 44.8848, -93.2223, 100),
            ("SFO Airport, San Francisco, CA", 37.6213, -122.3790, 100),
            ("MIA Airport, Miami, FL", 25.7959, -80.2870, 100),
            ("IAH Airport, Houston, TX", 29.9902, -95.3368, 100),
            ("ANC Airport, Anchorage, AK", 61.1743, -149.9982, 100),
            ("BOS Airport, Boston, MA", 42.3656, -71.0096, 100),
            ("CLT Airport, Charlotte, NC", 35.214, -80.9431, 100),
            ("PHX Airport, Phoenix, AZ", 33.4343, -112.0117, 100),
            ("SAN Airport, San Diego, CA", 32.7338, -117.1933, 50),
            ("TPA Airport, Tampa, FL", 27.9755, -82.5332, 100),
            ("DTW Airport, Detroit, MI", 42.2162, -83.3554, 100),
            ("LHR Airport, London Heathrow, UK", 51.4700, -0.4543, 50),
            ("CDG Airport, Paris Charles de Gaulle, France", 49.0097, 2.5479, 50),
            ("FRA Airport, Frankfurt, Germany", 50.0379, 8.5622, 50),
            ("AMS Airport, Amsterdam Schiphol, Netherlands", 52.3105, 4.7683, 50),
            ("MAD Airport, Madrid Barajas, Spain", 40.4983, -3.5676, 50),
            ("BCN Airport, Barcelona El Prat, Spain", 41.2974, 2.0833, 50),
            ("MUC Airport, Munich, Germany", 48.3538, 11.7861, 50),
            ("FCO Airport, Rome Fiumicino, Italy", 41.7999, 12.2462, 50),
            ("ZRH Airport, Zurich, Switzerland", 47.4647, 8.5492, 50),
            ("VIE Airport, Vienna, Austria", 48.1103, 16.5697, 50),
            ("LGW Airport, London Gatwick, UK", 51.1537, -0.1821, 50),
            ("CPH Airport, Copenhagen, Denmark", 55.6181, 12.6560, 50),
            ("BRU Airport, Brussels, Belgium", 50.9010, 4.4844, 50),
            ("OSL Airport, Oslo Gardermoen, Norway", 60.1939, 11.1004, 50),
            ("ARN Airport, Stockholm Arlanda, Sweden", 59.6519, 17.9186, 50),
            ("HEL Airport, Helsinki Vantaa, Finland", 60.3172, 24.9633, 50),
            ("DUB Airport, Dublin, Ireland", 53.4273, -6.2436, 50),
            ("IST Airport, Istanbul, Turkey", 41.2753, 28.7519, 50),
            ("MAN Airport, Manchester, UK", 53.3654, -2.2728, 50),
            ("WAW Airport, Warsaw Chopin, Poland", 52.1657, 20.9672, 50),
            ("PRG Airport, Prague Vaclav Havel, Czech Republic", 50.1008, 14.2632, 50),
            ("LIS Airport, Lisbon Humberto Delgado, Portugal", 38.7742, -9.1342, 50)
        ]
        
        for name, latitude, longitude, range_ in locations:
            existing_location = session.query(Location).filter_by(name=name).first()
            if not existing_location:
                location = Location(name=name, latitude=latitude, longitude=longitude, range=range_)
                session.add(location)
                print(f"Added new location: {name}")
            else:
                print(f"Location {name} already exists, skipping.")
        
        session.commit()
        print("Seeding completed.")
    except exc.SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding locations: {e}")
    finally:
        session.close()

def main():
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
    
    engine_url = f'postgresql://{user}:{password}@{host}/{database_name}'
    engine = create_engine(engine_url, pool_pre_ping=True, pool_recycle=3600, pool_timeout=30)
    
    Base.metadata.create_all(engine)
    seed_locations(engine)

if __name__ == '__main__':
    main()
