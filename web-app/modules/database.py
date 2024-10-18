# app/database.py
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os

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
engine = create_engine(engine_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
