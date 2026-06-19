import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
# 1. Simple Connection Setup (Apna MySQL password yahan check kar lena)
DB_USER = "root"
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "skustream_db"

print("Starting simple data generation...")

# 2. Database engine initialization
engine_base = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}")

# Default base database create karne ke liye basic command
with engine_base.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    conn.commit()

# Actual database schema se link
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 3. Generating Simple Sequential Data Array for 10,000 Rows
total_rows = 10000

# Simple lists creation
sku_list = []
origin_list = []
dest_list = []
dist_list = []
stock_list = []
sales_list = []
cost_list = []
lead_list = []
safety_list = []
storage_list = []
traffic_list = []
expiry_list = []

cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Kochi", "Lucknow"]

# Plain basic loop for generation
for i in range(1, total_rows + 1):
    sku_list.append(f"SKU-{i}")
    
    # Selecting distinct simple cities
    o_city = cities[i % 10]
    d_city = cities[(i + 3) % 10]
    origin_list.append(o_city)
    dest_list.append(d_city)
    
    # Baseline simple numerical numbers
    dist_list.append(500 + (i % 2000))        # Route Distance
    stock_list.append(50 + (i % 1500))        # Inventory On Hand
    sales_list.append(10 + (i % 400))         # Sales Velocity
    cost_list.append(1000 + (i % 50000))      # Unit Cost
    lead_list.append(2 + (i % 14))            # Lead Time
    safety_list.append(20 + (i % 100))        # Safety Stock
    storage_list.append(50 + (i % 500))        # Storage Cost
    traffic_list.append(1 + (i % 5))          # Traffic Index
    expiry_list.append(0.1 + ((i % 10) / 10.0)) # Expiry Risk

# 4. Merging lists cleanly inside standard DataFrame
df_simple = pd.DataFrame({
    'SKU_ID': sku_list,
    'Origin_City': origin_list,
    'Destination_City': dest_list,
    'Route_Distance_KM': dist_list,
    'Inventory_On_Hand': stock_list,
    'Sales_Velocity_30Days': sales_list,
    'Unit_Cost_INR': cost_list,
    'Lead_Time_Days': lead_list,
    'Safety_Stock_Level': safety_list,
    'Storage_Cost_Per_Unit': storage_list,
    'Route_Congestion_Index': traffic_list,
    'Expiry_Risk_Factor': expiry_list
})

# 5. Direct clean save to MySQL server database
print("Writing 10,000 rows to MySQL database client...")
df_simple.to_sql(name="inventory_metrics", con=engine, if_exists="replace", index=False)

print("Done! Check your database now.")