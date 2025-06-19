import os
import shutil
import sys
from dotenv import load_dotenv

# Load database path from .env
load_dotenv()
db_url = os.getenv("DATABASE_URL", "sqlite:///data/ts_modeling.db")

if not db_url.startswith("sqlite:///"):
    print("Restore is only supported for SQLite databases.")
    sys.exit(1)

# Extract path to SQLite file
db_path = db_url.replace("sqlite:///", "")

# Get backup filename from CLI
if len(sys.argv) < 2:
    print("Usage: python restore_db.py <backup_file_path>")
    sys.exit(1)

backup_path = sys.argv[1]

if not os.path.exists(backup_path):
    print(f"Backup file not found: {backup_path}")
    sys.exit(1)

# Ensure the target directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Build new restored file path
restored_path = os.path.splitext(db_path)[0] + "_restored.db"

# Copy backup to new restored file
shutil.copy2(backup_path, restored_path)
print(f"Restored database from {backup_path} to {restored_path}")
