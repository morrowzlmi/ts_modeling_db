import os
import pandas as pd
from ts_modeling_db.db import engine, DATABASE_URL
from sqlalchemy import inspect
from pathlib import Path
from datetime import datetime

db_filename = Path(DATABASE_URL).stem

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
outdir = "C:\\Users\\zachary.morrow\\LMI\\11616.001 DOS Passport Study III- T - Project_Execution\\Working_Files_\\Miscellaneous\\Zach\\testing\\"
outfilename = f"{db_filename}_export_{timestamp}.xlsx"
outpath = os.path.join(outdir,outfilename)

inspector = inspect(engine)
table_names = inspector.get_table_names()

with engine.connect() as conn, pd.ExcelWriter(outpath, engine='openpyxl') as writer:
    for table_name in table_names:
        df = pd.read_sql_table(table_name, con=conn)
        df.to_excel(writer, sheet_name=table_name[:31], index=False)  # Excel max sheet name length = 31
        print(f"Added table '{table_name}' to workbook.")

print(f"\n✅ Export complete: {outpath}")