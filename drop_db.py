# drop_db.py

import os
import shutil
import sys
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
from ts_modeling_db.models import Base


def drop_database(create_backup=True):
    # Load .env and get DATABASE_URL
    load_dotenv()
    db_url = os.getenv("DATABASE_URL", "sqlite:///data/ts_modeling.db")

    # Drop all tables
    engine = create_engine(db_url, echo=True, future=True)
    Base.metadata.drop_all(engine)
    print(f"Dropped all tables in database: {db_url}")

    # If SQLite: backup then delete
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")

        if os.path.exists(db_path):
            # 1. Create backup before disposing/deleting
            if create_backup:
                backup_name = f"{os.path.splitext(db_path)[0]}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(db_path, backup_name)
                abs_backup_path = os.path.abspath(backup_name)
                print(f"Backup created at: {abs_backup_path}")

            # 2. Dispose to release file lock
            engine.dispose()

            # 3. Try deleting
            try:
                os.remove(db_path)
                print(f"Deleted SQLite file: {db_path}")
            except PermissionError:
                print(f"\n[ERROR] Could not delete database file (possibly still in use): {db_path}")
                print("Please ensure no other process (Jupyter, VS Code, etc.) is accessing it.\n")
        else:
            print(f"No SQLite file found at: {db_path}")


if __name__ == "__main__":
    # CLI: python drop_db.py [nobackup]
    create_backup = "nobackup" not in [arg.lower() for arg in sys.argv[1:]]
    drop_database(create_backup=create_backup)
