# Import Meteostat library and dependencies
import datetime
from meteostat import Point, Daily, Stations
import numpy as np
import pandas as pd
import sqlite3

conn = sqlite3.connect("C:\\Users\\scott\\Downloads\\FPA_FOD_20221014.sqlite")

c = conn.cursor()

# read data from SQL
query = 'SELECT * FROM Fires ORDER BY RANDOM() LIMIT 10000'
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

df_weather = pd.DataFrame(data=None,columns=['id','tavg','tmin','tmax','prcp','snow','wdir','wspd','wpgt','pres','tsun','prcp_30'])
df_weather = df_weather.astype('float64')
# pull in historical weather data
for i, row in df.iterrows():
    if i % 100 == 0:
        print('at row {}'.format(i))
    has_data = False
    n_stations = 1
    # make sure weather station has data
    while not has_data:
        start = row['start_date']
        start_prcp = start-datetime.timedelta(days=30) # last 30 day precipitation measure
        # get stations with data
        stations = Stations()
        stations = stations.nearby(row['lat'],row['lon'])
        stations = stations.inventory('daily',start)
        station = stations.fetch(n_stations)
        end = start
        data = Daily(station,start,end).fetch()
        prcp_30 = Daily(station,start_prcp,end).fetch()['prcp'] # get last 30 day prcp
        # if no data, add next nearest station
        if data.empty:
            n_stations+=1
        # append data
        else:
            data['id'] = row['id']
            data['prcp_30'] = np.sum(prcp_30) # add sum of last 30 day precipitation
            data['prcp'].replace(np.nan,0,inplace=True) # assume nan prec values are zero
            df_weather.loc[i] = data.iloc[0]
        has_data=True

# merge weather data to wildfire data
df = df.merge(df_weather,on='id')

df.to_csv('./data/sample_data.csv')
