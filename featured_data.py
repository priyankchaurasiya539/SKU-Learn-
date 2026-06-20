import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import joblib

# 1. Load hidden password credentials
load_dotenv()

DB_USER = "root"
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "skustream_db"

# 2. Variable engine ko define karein (Isse error door ho jayega)
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 3. Load the dataset using the defined engine connection bridge
df = pd.read_sql("SELECT * FROM inventory_metrics", con=engine)

# 4. Print the first 5 rows to verify data loading
print(df.head(20))
print("-"*100)

#Drop unncessary columns 
df_new = df.copy()
df_new = df.drop(columns=['SKU_ID' , 'Origin_City' , 'Destination_City'])

#Standardization 
scaler = StandardScaler()
scale_data = scaler.fit_transform(df_new)

#Now apply PCA
pca = PCA(n_components=4)
data_pca = pca.fit_transform(scale_data)

print(df_new)
print("-"*100)
print(data_pca)
print("-"*100)
print("All done.")



#Save the pca file to joblib
joblib.dump(data_pca , "models/data_pca.pkl")
joblib.dump(scale_data , "models/scale_data.pkl")
joblib.dump(pca , "models/pca.pkl")
joblib.dump(list(df_new.columns) , "models/feature_names.pkl")
print("Files saved in models.")