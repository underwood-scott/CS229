import datetime
import numpy as np
import pandas as pd
import sqlite3
from util import add_geospatial_data
import xarray as xr

conn = sqlite3.connect("C:\\Users\\scott\\Downloads\\FPA_FOD_20221014.sqlite")

c = conn.cursor()

# read data from SQL
query = "SELECT * FROM Fires ORDER BY RANDOM() LIMIT 1000"
df = pd.read_sql_query(query,conn)
df = df[['OBJECTID','FIRE_NAME','DISCOVERY_DATE','FIRE_SIZE_CLASS','NWCG_CAUSE_CLASSIFICATION','CONT_DATE','FIRE_SIZE',
         'LATITUDE','LONGITUDE','STATE']]
df = df.rename(columns={'OBJECTID':'id','FIRE_NAME':'name','DISCOVERY_DATE':'start_date','NWCG_CAUSE_CLASSIFICATION':'cause',
                        'CONT_DATE':'end_date','FIRE_SIZE':'size','LATITUDE':'lat','LONGITUDE':'lon','STATE':'state',
                        'FIRE_CLASS_SIZE':'fire_size_class'})

# format datetime columns
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])
df['start_year'] = df['start_date'].dt.year
df['start_month'] = df['start_date'].dt.month
df['start_day_of_year'] = df['start_date'].dt.dayofyear
df['end_year'] = df['end_date'].dt.year
df['end_month'] = df['end_date'].dt.month
df['end_day_of_year'] = df['end_date'].dt.dayofyear

# filter to year desired
df = df.loc[df['start_date'].dt.year == 1994]

# open grib data
ds = xr.open_dataset("data/1994_us_data.grib",engine='cfgrib')
df_fc = ds.to_dataframe()

# add all variables available
for variable in df_fc.columns:
    add_geospatial_data(df,df_fc,variable)

print(df)
