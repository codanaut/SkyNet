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
    working = Column(Boolean, nullable=True, default=None)

def seed_locations(engine):
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    try:
        # Airports Across The World
        locations = [
            # United States

            # Alaska
            ("ANC Airport, Anchorage, AK", 61.1743, -149.9982, 100),

            # Arizona
            ("PHX Airport, Phoenix, AZ", 33.4343, -112.0117, 100),

            # California
            ("LAX Airport, Los Angeles, CA", 33.9416, -118.4085, 50),
            ("SMF Airport, Sacramento, CA", 38.6954, -121.5908, 50),
            ("SFO Airport, San Francisco, CA", 37.6213, -122.3790, 100),
            ("SAN Airport, San Diego, CA", 32.7338, -117.1933, 50),

            # Colorado
            ("DEN Airport, Denver, CO", 39.8561, -104.6737, 100),

            # District of Columbia
            ("DCA Airport, Washington D.C.", 38.8512, -77.0402, 25),

            # Florida
            ("JAX Airport, Jacksonville, FL", 30.4941, -81.6879, 100),
            ("MIA Airport, Miami, FL", 25.7959, -80.2870, 100),
            ("TPA Airport, Tampa, FL", 27.9755, -82.5332, 100),

            # Georgia
            ("ATL Airport, Atlanta, GA", 33.6407, -84.4277, 50),

            # Illinois
            ("ORD Airport, Chicago, IL", 41.9742, -87.9073, 50),

            # Massachusetts
            ("BOS Airport, Boston, MA", 42.3656, -71.0096, 100),

            # Michigan
            ("DTW Airport, Detroit, MI", 42.2162, -83.3554, 100),

            # Minnesota
            ("MSP Airport, Minneapolis, MN", 44.8848, -93.2223, 100),

            # Missouri
            ("MCI Airport, Kansas City, MO", 39.2976, -94.7139, 100),

            # Montana
            ("BZN Airport, Bozeman, MT", 45.7775, -111.1525, 100),

            # North Carolina
            ("RDU Airport, Raleigh-Durham, NC", 35.8776, -78.7875, 100),
            ("CLT Airport, Charlotte, NC", 35.2140, -80.9431, 100),

            # North Dakota
            ("BIS Airport, Bismarck, ND", 46.7727, -100.7462, 250),

            # Nebraska
            ("SNY Airport, Sidney, NE", 41.0995, -102.9827, 200),
            ("OMA Airport, Omaha, NE", 41.3032, -95.8941, 100),

            # Nevada
            ("LAS Airport, Las Vegas, NV", 36.0840, -115.1537, 100),

            # New Mexico
            ("ABQ Airport, Albuquerque, NM", 35.0402, -106.6090, 100),
            ("White Sands Missile Range, NM", 32.9910, -106.9750, 100),

            # New York
            ("JFK Airport, New York, NY", 40.6413, -73.7781, 50),

            # Oregon
            ("PDX Airport, Portland, OR", 45.5898, -122.5973, 100),

            # Tennessee
            ("MEM Airport, Memphis, TN", 35.0421, -89.9792, 100),
            ("BNA Airport, Nashville, TN", 36.1263, -86.6774, 100),

            # Texas
            ("DFW Airport, Dallas, TX", 32.8998, -97.0403, 50),
            ("IAH Airport, Houston, TX", 29.9902, -95.3368, 100),

            # Utah
            ("SLC Airport, Salt Lake City, UT", 40.7899, -111.9791, 100),

            # Washington
            ("SEA Airport, Seattle, WA", 47.4502, -122.3088, 100),

            # Canada
            ("YYZ Airport, Toronto Pearson, Canada", 43.6777, -79.6248, 200),
            ("YVR Airport, Vancouver, Canada", 49.1951, -123.1779, 200),
            ("YUL Airport, Montreal, Canada", 45.4706, -73.7408, 200),

            # Mexico
            ("MEX Airport, Mexico City, Mexico", 19.4361, -99.0719, 200),

            # United Kingdom
            ("LHR Airport, London Heathrow, UK", 51.4700, -0.4543, 100),
            ("LGW Airport, London Gatwick, UK", 51.1537, -0.1821, 100),
            ("MAN Airport, Manchester, UK", 53.3654, -2.2728, 100),
            ("EDI Airport, Edinburgh, UK", 55.9508, -3.3615, 100),
            ("BFS Airport, Belfast International, UK", 54.6575, -6.2158, 100),
            ("BHX Airport, Birmingham, UK", 52.4539, -1.7480, 100),
            ("BRS Airport, Bristol, UK", 51.3827, -2.7191, 100),
            ("GLA Airport, Glasgow, UK", 55.8642, -4.4331, 100),
            ("NCL Airport, Newcastle, UK", 55.0375, -1.6917, 100),

            # Europe
            ("CDG Airport, Paris Charles de Gaulle, France", 49.0097, 2.5479, 50),
            ("LYS Airport, Lyon, France", 45.7256, 5.0811, 100),
            ("NCE Airport, Nice, France", 43.6653, 7.2150, 100),
            ("FRA Airport, Frankfurt, Germany", 50.0379, 8.5622, 50),
            ("MUC Airport, Munich, Germany", 48.3538, 11.7861, 50),
            ("HAM Airport, Hamburg, Germany", 53.6304, 9.9882, 100),
            ("DUS Airport, Dusseldorf, Germany", 51.2895, 6.7668, 100),
            ("STR Airport, Stuttgart, Germany", 48.6900, 9.2219, 100),
            ("TXL Airport, Berlin Tegel, Germany", 52.5597, 13.2877, 100),
            ("AMS Airport, Amsterdam Schiphol, Netherlands", 52.3105, 4.7683, 50),
            ("ZRH Airport, Zurich, Switzerland", 47.4647, 8.5492, 50),
            ("GVA Airport, Geneva, Switzerland", 46.2381, 6.1090, 100),
            ("VIE Airport, Vienna, Austria", 48.1103, 16.5697, 50),
            ("BRU Airport, Brussels, Belgium", 50.9010, 4.4844, 50),
            ("CPH Airport, Copenhagen, Denmark", 55.6181, 12.6560, 50),
            ("OSL Airport, Oslo Gardermoen, Norway", 60.1939, 11.1004, 50),
            ("ARN Airport, Stockholm Arlanda, Sweden", 59.6519, 17.9186, 50),
            ("HEL Airport, Helsinki Vantaa, Finland", 60.3172, 24.9633, 50),
            ("DUB Airport, Dublin, Ireland", 53.4273, -6.2436, 50),
            ("MAD Airport, Madrid Barajas, Spain", 40.4983, -3.5676, 50),
            ("BCN Airport, Barcelona El Prat, Spain", 41.2974, 2.0833, 50),
            ("LIS Airport, Lisbon Humberto Delgado, Portugal", 38.7742, -9.1342, 50),
            ("PRG Airport, Prague Vaclav Havel, Czech Republic", 50.1008, 14.2632, 50),
            ("OSR Airport, Ostrava, Czech Republic", 49.6963, 18.1110, 100),
            ("KRK Airport, Krakow, Poland", 50.0777, 19.7848, 100),
            ("WAW Airport, Warsaw Chopin, Poland", 52.1657, 20.9672, 50),
            ("KUN Airport, Kaunas, Lithuania", 54.9639, 24.0848, 100),
            ("VNO Airport, Vilnius, Lithuania", 54.6431, 25.2791, 100),
            ("RIX Airport, Riga, Latvia", 56.9236, 23.9711, 100),
            ("TLL Airport, Tallinn, Estonia", 59.4133, 24.8328, 100),
            ("ATH Airport, Athens, Greece", 37.9364, 23.9475, 100),
            ("LJU Airport, Ljubljana, Slovenia", 46.2237, 14.4576, 100),
            ("SOF Airport, Sofia, Bulgaria", 42.6952, 23.4062, 100),
            ("BEG Airport, Belgrade, Serbia", 44.8184, 20.3091, 100),
            ("OTP Airport, Bucharest, Romania", 44.5711, 26.0850, 100),
            ("KBP Airport, Kyiv Boryspil, Ukraine", 50.3450, 30.8947, 100),
            ("IST Airport, Istanbul Airport, Turkey", 41.2753, 28.7519, 100),
            ("DME Airport, Moscow Domodedovo, Russia", 55.4088, 37.9063, 100),
            ("SVO Airport, Moscow Sheremetyevo, Russia", 55.9726, 37.4146, 100),
            ("LED Airport, St. Petersburg, Russia", 59.8003, 30.2625, 100),

            # Africa
            ("JNB Airport, Johannesburg, South Africa", -26.1337, 28.2420, 200),
            ("CPT Airport, Cape Town, South Africa", -33.9694, 18.5972, 200),
            ("DUR Airport, Durban, South Africa", -29.6144, 31.1197, 200),
            ("CAI Airport, Cairo, Egypt", 30.1120, 31.4000, 200),
            ("CMN Airport, Casablanca, Morocco", 33.3675, -7.5898, 200),
            ("LOS Airport, Lagos, Nigeria", 6.5774, 3.3212, 200),
            ("ABV Airport, Abuja, Nigeria", 9.0068, 7.2632, 200),
            ("NBO Airport, Nairobi, Kenya", -1.3192, 36.9278, 200),
            ("ADD Airport, Addis Ababa, Ethiopia", 8.9779, 38.7993, 200),
            ("ACC Airport, Accra, Ghana", 5.6052, -0.1668, 200),
            ("ALG Airport, Algiers, Algeria", 36.6910, 3.2154, 200),
            ("TUN Airport, Tunis, Tunisia", 36.8510, 10.2272, 200),
            ("DAR Airport, Dar es Salaam, Tanzania", -6.8781, 39.2026, 200),
            ("ZNZ Airport, Zanzibar, Tanzania", -6.2220, 39.2249, 200),
            ("KGL Airport, Kigali, Rwanda", -1.9686, 30.1395, 200),
            ("KRT Airport, Khartoum, Sudan", 15.5895, 32.5532, 200),
            ("FIH Airport, Kinshasa, DR Congo", -4.3858, 15.4446, 200),
            ("EBB Airport, Entebbe, Uganda", 0.0424, 32.4432, 200),
            ("SEZ Airport, Seychelles", -4.6743, 55.5218, 200),
            ("MRU Airport, Mauritius", -20.4302, 57.6836, 200),

            # Asia
            ("HND Airport, Tokyo Haneda, Japan", 35.5494, 139.7798, 200),
            ("NRT Airport, Tokyo Narita, Japan", 35.7719, 140.3929, 200),
            ("PEK Airport, Beijing Capital, China", 40.0799, 116.6031, 200),
            ("PVG Airport, Shanghai Pudong, China", 31.1443, 121.8083, 200),
            ("HKG Airport, Hong Kong", 22.3080, 113.9185, 200),
            ("SIN Airport, Singapore Changi", 1.3644, 103.9915, 200),
            ("ICN Airport, Seoul Incheon, South Korea", 37.4602, 126.4407, 200),
            ("DEL Airport, New Delhi, India", 28.5562, 77.1000, 200),
            ("BOM Airport, Mumbai, India", 19.0896, 72.8656, 200),
            ("BKK Airport, Bangkok Suvarnabhumi, Thailand", 13.6900, 100.7501, 200),
            ("KUL Airport, Kuala Lumpur, Malaysia", 2.7456, 101.7072, 200),
            ("MNL Airport, Manila, Philippines", 14.5086, 121.0194, 200),
            ("CGK Airport, Jakarta, Indonesia", -6.1256, 106.6559, 200),

            # Middle East
            ("DXB Airport, Dubai, UAE", 25.2532, 55.3657, 200),
            ("DOH Airport, Doha, Qatar", 25.2736, 51.6080, 200),
            ("RUH Airport, Riyadh, Saudi Arabia", 24.9576, 46.6988, 200),
            ("JED Airport, Jeddah, Saudi Arabia", 21.6702, 39.1515, 200),
            ("TLV Airport, Tel Aviv, Israel", 32.0055, 34.8854, 200),
            ("AMM Airport, Amman, Jordan", 31.7226, 35.9932, 200),
            ("KWI Airport, Kuwait City, Kuwait", 29.2269, 47.9800, 200),
            ("BAH Airport, Bahrain International", 26.2708, 50.6336, 200),
            ("MCT Airport, Muscat, Oman", 23.5933, 58.2844, 200),
            ("IKA Airport, Tehran, Iran", 35.4161, 51.1522, 200),

            # Oceania
            ("SYD Airport, Sydney, Australia", -33.9399, 151.1753, 200),
            ("MEL Airport, Melbourne, Australia", -37.6733, 144.8430, 200),
            ("BNE Airport, Brisbane, Australia", -27.3842, 153.1175, 200),
            ("PER Airport, Perth, Australia", -31.9403, 115.9670, 200),
            ("AKL Airport, Auckland, New Zealand", -37.0082, 174.7917, 200),
            ("CHC Airport, Christchurch, New Zealand", -43.4894, 172.5322, 200),
            ("WLG Airport, Wellington, New Zealand", -41.3272, 174.8056, 200),

            # South America
            ("GRU Airport, São Paulo, Brazil", -23.4356, -46.4731, 200),
            ("GIG Airport, Rio de Janeiro, Brazil", -22.8089, -43.2436, 200),
            ("EZE Airport, Buenos Aires, Argentina", -34.8222, -58.5358, 200),
            ("SCL Airport, Santiago, Chile", -33.3928, -70.7858, 200),
            ("LIM Airport, Lima, Peru", -12.0219, -77.1143, 200),
            ("BOG Airport, Bogotá, Colombia", 4.7016, -74.1469, 200),
            ("UIO Airport, Quito, Ecuador", -0.1175, -78.3547, 200),
            ("CCS Airport, Caracas, Venezuela", 10.6031, -66.9906, 200),
            ("PTY Airport, Panama City, Panama", 9.0714, -79.3835, 200),
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
