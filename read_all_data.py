import datetime
import numpy as np
import pandas as pd
import sqlite3
from util import add_geospatial_data, add_geospatial_data_alt
import xarray as xr

conn = sqlite3.connect("C:\\Users\\scott\\Downloads\\FPA_FOD_20221014.sqlite")

c = conn.cursor()

# read data from SQL
#query = "SELECT * FROM Fires"
query = "SELECT * FROM Fires ORDER BY RANDOM() LIMIT 10000"
df = pd.read_sql_query(query,conn)
df = df[['DISCOVERY_DATE','FIRE_SIZE_CLASS','NWCG_CAUSE_CLASSIFICATION','NWCG_GENERAL_CAUSE','FIRE_SIZE',
         'LATITUDE','LONGITUDE']]
df = df.rename(columns={'DISCOVERY_DATE':'start_date','NWCG_CAUSE_CLASSIFICATION':'category', 'NWCG_GENERAL_CAUSE': 'cause',
                        'FIRE_SIZE':'size','LATITUDE':'lat','LONGITUDE':'lon','FIRE_CLASS_SIZE':'fire_size_class'})

# format datetime columns
df['start_date'] = pd.to_datetime(df['start_date'])

print('done reading in sql')

#######################################################################################################
############################## READ IN INDEX DATA ###############################################
#######################################################################################################
# find path to fire index data
index_data = 'C:/Users/scott/OneDrive/Documents/Stanford/Autumn23/CS229/cs229_project/data/fire_indices'

# open fire index grib data and add
first_year = True
for year in range(2010,2021,1):
    ds_temp = xr.open_dataset(index_data+"/{}_us_data.grib".format(str(year)),engine='cfgrib')
    df_temp = ds_temp.to_dataframe()
    # get list of columns
    cols = list(df_temp.columns)
    cols.remove('surface')
    cols.remove('latitude')
    cols.remove('longitude')

    # initialize columns
    if first_year:
        first_year = False
        for variable in cols:
            df[variable] = np.nan

    # add all column data
    add_geospatial_data(df,df_temp,cols,year)
    df.to_csv('data/compiled_dataset.csv')

    print('Year {} of fire index data complete'.format(year))


df.to_csv('data/compiled_dataset.csv')
print('finished fire index data')


#######################################################################################################
############################## READ IN TEMPERATURE DATA ###############################################
#######################################################################################################
temp_data = 'C:/Users/scott/OneDrive/Documents/Stanford/Autumn23/CS229/cs229_project/data/temp_features'

# open temp grib data and add
first_year = True
for year in range(2010,2021,1):
    ds_temp = xr.open_dataset(temp_data+"/{}_us_data.grib".format(year),engine='cfgrib')
    df_temp = ds_temp.to_dataframe()
    # get list of columns
    cols = list(df_temp.columns)
    cols.remove('number')
    cols.remove('step')
    cols.remove('surface')
    cols.remove('valid_time')

    # for first year, initialize columns
    if first_year:
        first_year = False
        # add each columns' data
        for variable in cols:
            df[variable] = np.nan

    add_geospatial_data_alt(df,df_temp,cols,year)
    df.to_csv('data/compiled_dataset.csv')

    print('Year {} of fire temp data complete'.format(year))

df.to_csv('data/compiled_dataset.csv')
