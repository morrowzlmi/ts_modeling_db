import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env
dotenv_file = find_dotenv(usecwd=True)
print("Working directory:", os.getcwd())
print("Found .env file at:", dotenv_file)
load_dotenv(dotenv_file)
print("Loaded DATABASE_URL:", os.getenv("DATABASE_URL"))
# Default to an absolute SQLite path if DATABASE_URL is not specified
DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "ts_modeling.db"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Create engine and sessionmaker
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    """Returns a new SQLAlchemy session."""
    return SessionLocal()

def get_engine():
    """Returns the configured SQLAlchemy engine."""
    return engine
