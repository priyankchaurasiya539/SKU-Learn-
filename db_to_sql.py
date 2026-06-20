import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Environment variables set up
load_dotenv()

DB_USER = "root"
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "skustream_db"

# 2. Connection path engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("Reading data...")
# 3. Read whole table instantly into a dataframe
df = pd.read_sql("SELECT * FROM inventory_metrics", con=engine)

print("Writing direct sql statements...")
# 4. Pure structured matrix ko binary local SQL script backup file mein transfer karein
df.to_pickle("inventory_backup.sql")

print("Done! Check your folder.")