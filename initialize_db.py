# initialize_db.py

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from ts_modeling_db.models import Base

# Load environment variables from .env
load_dotenv()

# Default to an absolute SQLite path if DATABASE_URL not specified
DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "ts_modeling.db"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

def initialize_database():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    print("Database schema created at:", DATABASE_URL)

if __name__ == "__main__":
    initialize_database()
