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

# open us grib data and add
ds = xr.open_dataset("data/1994_us_data.grib",engine='cfgrib')
df_us = ds.to_dataframe()
for year in range(1995,2020,1):
    ds_temp = xr.open_dataset("data/{}us_data.grib".format(year),engine='cfgrib')
    df_temp = ds_temp.to_dataframe
    df_us = pd.concat([df_us,df_temp])

# add all variables available
for variable in df_us.columns:
    add_geospatial_data(df,df_us,variable)

# open canada grib data and add
ds = xr.open_dataset("data/1994_ca1_data.grib",engine='cfgrib')
df_ca1 = ds.to_dataframe()
ds = xr.open_dataset("data/1994_ca2_data.grib",engine='cfgrib')
df_ca2 = ds.to_dataframe()
for year in range(1995,2020,1):
    # add first canadian dataset
    ds_temp = xr.open_dataset("data/{}ca1_data.grib".format(year),engine='cfgrib')
    df_temp = ds_temp.to_dataframe
    df_ca1 = pd.concat([df_ca1,df_temp])
    # add second canadian dataset
    ds_temp = xr.open_dataset("data/{}ca2_data.grib".format(year),engine='cfgrib')
    df_temp = ds_temp.to_dataframe
    df_ca2 = pd.concat([df_ca2,df_temp])

# add all variables available
for variable in df_us.columns:
    add_geospatial_data(df,df_us,variable)

# add all variables available
for variable in df_ca1.columns:
    add_geospatial_data(df,df_ca1,variable)

# add all variables available
for variable in df_ca2.columns:
    add_geospatial_data(df,df_ca2,variable)
