# Download faa data imports
import csv
import sqlite3
import re
import os
import requests
import zipfile
import shutil
# Update db imports
from sqlalchemy import create_engine, Column, String, DateTime, Date, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import json

def download_data():
    def clean_identifier(identifier):
        identifier = identifier.replace(' ', '_').replace('-', '_')
        identifier = re.sub(r'\W+', '', identifier)
        identifier = identifier.lstrip('\ufeff')  # Remove BOM if present
        return identifier


    def download_and_unzip(url, tmp_dir):
        print("Staring Download")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        zip_file_path = os.path.join(tmp_dir, 'downloaded.zip')

        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(zip_file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)

        os.remove(zip_file_path)
        print("Download completed successfully.")

    def create_db_from_csv(csv_file_paths, db_file_path):
        if os.path.exists(db_file_path):
            os.remove(db_file_path)
            print("Removed Old DB")

        print("Building new DB")    
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        for csv_file_path in csv_file_paths:
            base_name = os.path.basename(csv_file_path)
            table_name = clean_identifier(os.path.splitext(base_name)[0])

            with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile)
                original_headers = next(reader)
                headers = [clean_identifier(header) for header in original_headers]

                columns = ', '.join([f'"{header}" TEXT' for header in headers])
                create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})'
                cursor.execute(create_table_sql)

                placeholders = ', '.join(['?'] * len(headers))
                insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
                for row in reader:
                    cursor.execute(insert_sql, row)

        conn.commit()
        conn.close()
        print("Building DB completed successfully.")

    def cleanup_dir(directory):
        print("Cleaning up")
        shutil.rmtree(directory)

    # URL of the zip file and temp directory
    url = 'https://registry.faa.gov/database/ReleasableAircraft.zip'
    tmp_dir = './tmp_download'

    # Download and unzip
    download_and_unzip(url, tmp_dir)

    # Specify the files you're interested in
    interested_files = [
        'MASTER.txt',
        'ACFTREF.txt',
        'ENGINE.txt',
    ]

    # Build paths for the interested files
    csv_file_paths = [os.path.join(tmp_dir, filename) for filename in interested_files]

    # Specify the database file path and create the database
    db_file_path = 'plane_info.db'
    create_db_from_csv(csv_file_paths, db_file_path)

    # Cleanup the temporary directory
    cleanup_dir(tmp_dir)

    print("Process completed successfully.")


download_data()


# ------  Update DB ----- #


def update_db():
    
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

    # SQLite file path
    sqlite_file = 'plane_info.db'

    # SQLAlchemy base and session setup for PostgreSQL
    Base = declarative_base()

    # Aircraft table class (PostgreSQL)
    class Aircraft(Base):
        __tablename__ = 'aircraft'

        hex = Column(String, primary_key=True)  # Unique identifier for the aircraft, often the Mode S code.
        registration = Column(String)  # Aircraft registration number.
        owner = Column(String)  # Aircraft's operator or owner.
        
        #Aircraft Info
        serial_number = Column(String) # aircraft serial number assigned to the aircraft by the manufacturer
        aircraft_manufacturer = Column(String) # code assigned to the aircraft manufacturer, model and series.
        aircraft_model = Column(String)
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
        state = Column(String)
        zip_code = Column(String)
        region = Column(String)
        county = Column(String)
        
        
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
        last_updated = Column(String)  # When the record was last updated.
        timestamp = Column(DateTime, default=datetime.now(timezone.utc))  # Timestamp of the data entry.
        
    # Create engine and session for PostgreSQL
    pg_engine = create_engine(f'postgresql://{user}:{password}@{host}/{database_name}')
    Session = sessionmaker(bind=pg_engine)
    pg_session = Session()

    # Function to clean and process data
    def clean_data(row):
        def clean_string(value):
            return value.rstrip() if value else None  # Strip trailing spaces
        
        # Clean the entire row
        cleaned_row = {key: clean_string(row[key]) for key in row.keys()}
        return cleaned_row


    #
    # Helper Functions
    #
    def process_country(country_code):
        # Custom logic for handling or cleaning country codes
        if country_code == 'US':
            return 'United States'
        return country_code


    def convert_date(date_str):
        if not date_str or date_str == "":  # Handle empty strings or None values
            return None
        if len(date_str) == 8:  # Ensure the date is in the correct format (YYYYMMDD)
            try:
                return datetime.strptime(date_str, '%Y%m%d').date()
            except ValueError:
                return None  # Handle invalid dates
        return None  # Return None for any other invalid formats


    # Load JSON data from files
    def load_json(filename):
        with open(filename, 'r') as file:
            return json.load(file)



    # Function to get full names based on state and county codes
    def format_location(state_abbr, county_code):
        # Load the JSON data
        state_abbr_to_name = load_json('state_abbr_to_name.json')
        state_abbr_to_incits_code = load_json('state_abbr_to_incits_code.json')
        json_data = load_json('county-codes.json')
        
        state_name = state_abbr_to_name.get(state_abbr, 'Unknown State')
        state_code = state_abbr_to_incits_code.get(state_abbr, '00')  # Default to '00' if not found
        full_incits_code = state_code + county_code
        county_info = json_data.get(full_incits_code, {"County": "Unknown County", "State": state_name})

        # Verify if the state from the JSON matches the state from the separate state column
        if county_info["State"] != state_name:
            return {
                "county": "Mismatch",
                "state": state_name
            }
        
        return {
            "county": county_info["County"],
            "state": county_info["State"]
        }

    def get_registrant_type(registrant_code):
        registrant_types = {
            "1": "Individual",
            "2": "Partnership",
            "3": "Corporation",
            "4": "Co-Owned",
            "5": "Government",
            "7": "LLC",
            "8": "Non Citizen Corporation",
            "9": "Non Citizen Co-Owned"
        }
        return registrant_types.get(registrant_code, "Unknown")  # 'Unknown' for unmapped values


    def get_aircraft_type(aircraft_types_code):
        aircraft_types = {
            "1": "Glider",
            "2": "Balloon",
            "3": "Blimp/Dirigible",
            "4": "Fixed wing single engine",
            "5": "Fixed wing multi engine",
            "6": "Rotorcraft",
            "7": "Weight-shift-control",
            "8": "Powered Parachute",
            "9": "Gyroplane",
            "H": "Hybrid Lift",
            "O": "Other"
        }
        return aircraft_types.get(aircraft_types_code, "Unknown")  # 'Unknown' for unmapped values

    def get_engine_type(engine_types_code):
        engine_types = {
            "0": "None",
            "1": "Reciprocating",
            "2": "Turbo-prop",
            "3": "Turbo-shaft",
            "4": "Turbo-jet",
            "5": "Turbo-fan",
            "6": "Ramjet",
            "7": "2 Cycle",
            "8": "4 Cycle",
            "9": "Unknown",
            "10": "Electric",
            "11": "Rotary"
        }
        return engine_types.get(engine_types_code, "Unknown")  # 'Unknown' for unmapped values

    def get_region(region):
        region_types = {
            "1": "Eastern",
            "2": "Southwestern",
            "3": "Central",
            "4": "Western-Pacific",
            "5": "Alaskan",
            "7": "Southern",
            "8": "European",
            "C": "Great Lakes",
            "E": "New England",
            "S": "Northwest Mountain"
        }
        return region_types.get(region, "Unknown")  # 'Unknown' for unmapped values

    def get_status_description(status_code):
        status_code_mapping = {
            "A": "The Triennial Aircraft Registration form was mailed and has not been returned by the Post Office",
            "D": "Expired Dealer",
            "E": "The Certificate of Aircraft Registration was revoked by enforcement action",
            "M": "Valid - Aircraft assigned to the manufacturer under the manufacturer’s Dealer Certificate",
            "N": "Non-citizen Corporations which have not returned their flight hour reports",
            "R": "Registration pending",
            "S": "Second Triennial Aircraft Registration Form has been mailed and has not been returned by the Post Office",
            "T": "Valid Registration from a Trainee",
            "V": "Valid Registration",
            "W": "Certificate of Registration has been deemed Ineffective or Invalid",
            "X": "Enforcement Letter",
            "Z": "Permanent Reserved",
            "1": "Triennial Aircraft Registration form was returned by the Post Office as undeliverable",
            "2": "N-Number Assigned – but has not yet been registered",
            "3": "N-Number assigned as a Non Type Certificated aircraft - but has not yet been registered",
            "4": "N-Number assigned as import - but has not yet been registered",
            "5": "Reserved N-Number",
            "6": "Administratively canceled",
            "7": "Sale reported",
            "8": "A second attempt has been made at mailing a Triennial Aircraft Registration form to the owner with no response",
            "9": "Certificate of Registration has been revoked",
            "10": "N-Number assigned, has not been registered and is pending cancellation",
            "11": "N-Number assigned as a Non Type Certificated (Amateur) but has not been registered that is pending cancellation",
            "12": "N-Number assigned as import but has not been registered that is pending cancellation",
            "13": "Registration Expired",
            "14": "First Notice for Re-Registration/Renewal",
            "15": "Second Notice for Re-Registration/Renewal",
            "16": "Registration Expired – Pending Cancellation",
            "17": "Sale Reported – Pending Cancellation",
            "18": "Sale Reported – Canceled",
            "19": "Registration Pending – Pending Cancellation",
            "20": "Registration Pending – Canceled",
            "21": "Revoked – Pending Cancellation",
            "22": "Revoked – Canceled",
            "23": "Expired Dealer (Pending Cancellation)",
            "24": "Third Notice for Re-Registration/Renewal",
            "25": "First Notice for Registration Renewal",
            "26": "Second Notice for Registration Renewal",
            "27": "Registration Expired",
            "28": "Third Notice for Registration Renewal",
            "29": "Registration Expired – Pending Cancellation"
        }

        return status_code_mapping.get(status_code, "Unknown status code")

    def get_certification_type(data):
        # Dictionary mappings for airworthiness and operation codes
        airworthiness_code_map = {
            '1': 'Standard',
            '2': 'Limited',
            '3': 'Restricted',
            '4': 'Experimental',
            '5': 'Provisional',
            '6': 'Multiple',
            '7': 'Primary',
            '8': 'Special Flight Permit',
            '9': 'Light Sport',
        }
        
        # Operation codes for Standard (position 239 for Standard)
        standard_op_codes = {
            'N': 'Normal',
            'U': 'Utility',
            'A': 'Acrobatic',
            'T': 'Transport',
            'G': 'Glider',
            'B': 'Balloon',
            'C': 'Commuter',
            'O': 'Other',
        }
        
        # Restricted operation codes (position 239-245 for Restricted)
        restricted_op_codes = {
            '0': 'Other',
            '1': 'Agriculture and Pest Control',
            '2': 'Aerial Surveying',
            '3': 'Aerial Advertising',
            '4': 'Forest',
            '5': 'Patrolling',
            '6': 'Weather Control',
            '7': 'Carriage of Cargo',
        }
        
        # Experimental operation codes (position 239-245 for Experimental)
        experimental_op_codes = {
            '0': 'To show compliance with FAR',
            '1': 'Research and Development',
            '2': 'Amateur Built',
            '3': 'Exhibition',
            '4': 'Racing',
            '5': 'Crew Training',
            '6': 'Market Survey',
            '7': 'Operating Kit Built Aircraft',
            '8A': 'Light-Sport Kit-Built (Prior to 01/31/08)',
            '9A': 'Unmanned Aircraft - Research and Development',
            '9B': 'Unmanned Aircraft - Market Survey',
            '9C': 'Unmanned Aircraft - Crew Training',
            '9D': 'Unmanned Aircraft - Exhibition',
            '9E': 'Unmanned Aircraft - Compliance With CFR',
        }
        
        # Provisional operation codes (position 239 for Provisional)
        provisional_op_codes = {
            '1': 'Class I',
            '2': 'Class II',
        }
        
        # Multiple operation codes (position 239-240 for Multiple)
        multiple_op_codes = {
            '1': 'Standard',
            '2': 'Limited',
            '3': 'Restricted',
        }
        
        # Special Flight Permit operation codes (position 239-247 for Special Flight Permit)
        special_flight_permit_op_codes = {
            '1': 'Ferry flight for repairs, alterations, maintenance or storage',
            '2': 'Evacuate from area of impending danger',
            '3': 'Operation in excess of maximum certificated',
            '4': 'Delivery or export',
            '5': 'Production flight testing',
            '6': 'Customer Demo',
        }
        
        # Light Sport operation codes (position 239 for Light Sport)
        light_sport_op_codes = {
            'A': 'Airplane',
            'G': 'Glider',
            'L': 'Lighter than Air',
            'P': 'Power-Parachute',
            'W': 'Weight-Shift-Control',
        }

        if not data or len(data) < 1:
            return "N/A"
        
        # Get the Airworthiness class from position 238 (first character in data)
        airworthiness_class = airworthiness_code_map.get(data[0], 'Unknown Classification')

        # Initialize result with the Airworthiness class
        result = f"Classification: {airworthiness_class}"

        # Handle Standard operations (position 239)
        if airworthiness_class == 'Standard':
            if len(data) > 1:
                operation_code = data[1]
                result += f", Operation: {standard_op_codes.get(operation_code, 'Unknown Operation')}"
        
        # Handle Restricted operations (positions 239-245, can have multiple)
        elif airworthiness_class == 'Restricted':
            operations = []
            for char in data[1:]:
                operation = restricted_op_codes.get(char)
                if operation:
                    operations.append(operation)
            result += f", Operations: {', '.join(operations)}"
        
        # Handle Experimental operations (positions 239-245, can have multiple)
        elif airworthiness_class == 'Experimental':
            operations = []
            for char in data[1:]:
                operation = experimental_op_codes.get(char)
                if operation:
                    operations.append(operation)
            result += f", Operations: {', '.join(operations)}"

        # Handle Provisional operations (position 239)
        elif airworthiness_class == 'Provisional':
            if len(data) > 1:
                provisional_code = data[1]
                result += f", Class: {provisional_op_codes.get(provisional_code, 'Unknown Class')}"
        
        # Handle Multiple operations (positions 239-240)
        elif airworthiness_class == 'Multiple':
            if len(data) > 1:
                multiple_code = data[1]
                operations = [multiple_op_codes.get(multiple_code, 'Unknown Operation')]
                if len(data) > 2:
                    additional_code = data[2]
                    operations.append(multiple_op_codes.get(additional_code, 'Unknown Operation'))
                result += f", Operations: {', '.join(operations)}"
        
        # Handle Special Flight Permit operations (positions 239-247)
        elif airworthiness_class == 'Special Flight Permit':
            if len(data) > 1:
                special_code = data[1]
                result += f", Operation: {special_flight_permit_op_codes.get(special_code, 'Unknown Operation')}"
        
        # Handle Light Sport operations (position 239)
        elif airworthiness_class == 'Light Sport':
            if len(data) > 1:
                sport_code = data[1]
                result += f", Type: {light_sport_op_codes.get(sport_code, 'Unknown Type')}"

        return result

    #
    #
    # Process Data
    def process_data(row):

        formatted_data = format_location(row['STATE'], row['COUNTY'])
        formatted_county = formatted_data['county']
        formatted_state = formatted_data['state']
        # Map cleaned data to PostgreSQL format
        return {
            "hex": row['MODE_S_CODE_HEX'].lower(),  # No additional cleaning here
            "registration": f"N{row['Registration'].upper()}",  # No additional cleaning here
            "owner": row['NAME'],  # No additional cleaning here
            "serial_number": row['SERIAL_NUMBER'],
            "aircraft_manufacturer": row['Aircraft_Man'],
            "aircraft_model": row['Aircraft_Model'],
            "number_seats": int(row['NO_SEATS']) if row['NO_SEATS'] else None,
            "number_engines": int(row['NO_ENG']) if row['NO_ENG'] else None,
            "engine_manufacturer": row['Eng_MFR'],
            "engine_model": row['Eng_Model'],
            "type_engine": get_engine_type(row['TYPE_ENGINE']),
            "year_mfr": row['YEAR_MFR'].strip() if row['YEAR_MFR'] and row['YEAR_MFR'].strip() else None,
            "type_aircraft": get_aircraft_type(row['TYPE_AIRCRAFT']),
            "kit_mfr": row['KIT_MFR'],
            "kit_model": row['_KIT_MODEL'],
            "manufacturer_code": row['MFR_MDL_CODE'],
            "engine_code": row['ENG_MFR_MDL'],
            "type_registrant": get_registrant_type(row['TYPE_REGISTRANT']),
            "country": process_country(row['COUNTRY']),
            "street": row['STREET'],
            "street2": row['STREET2'],
            "city": row['CITY'],
            "county": formatted_county,
            "state": formatted_state,
            "zip_code": row['ZIP_CODE'],
            "region": get_region(row['REGION']),
            "last_action_date": convert_date(row['LAST_ACTION_DATE']),
            "cert_issue_date": convert_date(row['CERT_ISSUE_DATE']),
            "certification": get_certification_type(row['CERTIFICATION']),
            "status_code": get_status_description(row['STATUS_CODE']),
            "fract_owner": row['FRACT_OWNER'],
            "air_worth_date": convert_date(row['AIR_WORTH_DATE']),
            "other_names1": row['OTHER_NAMES1'],
            "other_names2": row['OTHER_NAMES2'],
            "other_names3": row['OTHER_NAMES3'],
            "other_names4": row['OTHER_NAMES4'],
            "other_names5": row['OTHER_NAMES5'],
            "expiration_date": convert_date(row['EXPIRATION_DATE']),
            "mode_s_code_oct": row['MODE_S_CODE'],  # Assuming it's the octal version
            "unique_id": row['UNIQUE_ID'],
            'last_updated': datetime.now().strftime('%m/%d/%Y %I:%M %p'),
            'timestamp': datetime.now(timezone.utc)
        }

    def update_or_insert_aircraft(aircraft, data):
        fields_changed = False  # Flag to track if any field has changed
        
        for field, value in data.items():
            if field in ['last_updated', 'timestamp']:
                continue  # Skip timestamp fields for now
            
            if getattr(aircraft, field) != value:
                print(f"Updating: {data['hex']} ({field})")
                setattr(aircraft, field, value)
                fields_changed = True
        
        if fields_changed:
            # Update timestamp fields only if any other field has changed
            setattr(aircraft, 'last_updated', datetime.now().strftime('%m/%d/%Y %I:%M %p'))
            setattr(aircraft, 'timestamp', datetime.now(timezone.utc))

    def sync_data():
        # Connect to the SQLite database
        sqlite_conn = sqlite3.connect(sqlite_file)
        sqlite_conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        sqlite_cursor = sqlite_conn.cursor()

        # SQL query to get the data from SQLite
        sqlite_query = '''
        SELECT 
            m."MODE_S_CODE_HEX", 
            m."N_NUMBER" AS "Registration",
            m."NAME",
            m."SERIAL_NUMBER",
            a."MFR" AS "Aircraft_Man", 
            a."MODEL" AS "Aircraft_Model",
            a."NO_SEATS",
            a."NO_ENG",
            e."MFR" AS "Eng_MFR", 
            e."MODEL" AS "Eng_Model", 
            m."YEAR_MFR",
            m."TYPE_AIRCRAFT",
            m."TYPE_ENGINE",
            m."KIT_MFR",
            m."_KIT_MODEL",
            m."MFR_MDL_CODE",
            m."ENG_MFR_MDL",
            m."TYPE_REGISTRANT",
            m."STREET",
            m."STREET2",
            m."CITY",
            m."STATE",
            m."ZIP_CODE",
            m."REGION",
            m."COUNTY",
            m."COUNTRY",
            m."LAST_ACTION_DATE",
            m."CERT_ISSUE_DATE",
            m."CERTIFICATION",
            m."STATUS_CODE",
            m."MODE_S_CODE",
            m."FRACT_OWNER",
            m."AIR_WORTH_DATE",
            m."OTHER_NAMES1",
            m."OTHER_NAMES2",
            m."OTHER_NAMES3",
            m."OTHER_NAMES4",
            m."OTHER_NAMES5",
            m."EXPIRATION_DATE",
            m."UNIQUE_ID"
        FROM 
            MASTER m 
        LEFT JOIN 
            ENGINE e ON m."ENG_MFR_MDL" = e."CODE"
        LEFT JOIN 
            ACFTREF a ON m."MFR_MDL_CODE" = a."CODE";

        '''
        
        sqlite_cursor.execute(sqlite_query)
        rows = sqlite_cursor.fetchmany(1000)  # Fetch in batches of 1000
        
        while rows:
            for row in rows:
                cleaned_row = clean_data(row)  # Clean data
                data = process_data(cleaned_row)  # Map cleaned data

                # Check if the aircraft already exists in PostgreSQL by hex (Mode S code)
                aircraft = pg_session.query(Aircraft).filter_by(hex=data['hex']).first()

                if aircraft:
                    # Update the existing record dynamically
                    update_or_insert_aircraft(aircraft, data)
                else:
                    # Insert a new record if it doesn't exist
                    print(f"Adding: {data['hex']}")
                    new_aircraft = Aircraft(**data)  # Unpack the dictionary to create a new record
                    pg_session.add(new_aircraft)

            # Commit the batch to PostgreSQL
            try:
                pg_session.commit()
            except IntegrityError:
                pg_session.rollback()

            # Fetch the next batch of rows
            rows = sqlite_cursor.fetchmany(1000)

        # Close SQLite connection
        sqlite_conn.close()

    # Run the sync function
    print("Starting DB Update")
    sync_data()

    # Close PostgreSQL session
    pg_session.close()
    print("All done!")


update_db()
