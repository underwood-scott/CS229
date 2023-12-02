import datetime
import numpy as np
import pandas as pd
import sqlite3
from util import add_geospatial_data, add_geospatial_data_alt
import xarray as xr


df = pd.read_csv('data/compiled_dataset_scott.csv')
#######################################################################################################
############################## READ IN TEMPERATURE DATA ###############################################
#######################################################################################################
temp_data = 'C:/Users/scott/OneDrive/Documents/Stanford/Autumn23/CS229/cs229_project/data/temp_features'

# open temp grib data and add
first_year = True
for year in range(1992,2021,1):
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
    df.to_csv('data/compiled_dataset_scott.csv')

    print('Year {} of fire temp data complete'.format(year))

df.to_csv('data/compiled_dataset_scott.csv')
