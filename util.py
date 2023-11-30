import numpy as np
import pandas as pd

def add_geospatial_data(df,df_fc,cols,year):

    for i, row in df.iterrows():
        if i % 1000 == 0:
            print('on row {}'.format(i))
        if row['start_date'].year == year:
            # find data for date
            df_temp = df_fc[df_fc.index.get_level_values('time').date == row['start_date'].date()]
            # see if data is available, if not append NaN
            try:
                # find closest latitude data
                lat = min(df_temp.latitude.unique(), key=lambda x:abs(x-row['lat']))
                df_temp = df_temp[df_temp.latitude == lat]
                # find closest longitude data
                lon = min(df_temp.longitude.unique(), key=lambda x:abs(x-(row['lon']+360)))
                df_temp = df_temp[df_temp.longitude == lon]
                # add datapoints
                for variable in cols:
                    df.at[i,variable] = df_temp.iloc[0][variable]
            except:
                pass



def add_geospatial_data_alt(df,df_fc,cols,year):

    for i, row in df.iterrows():
        if i % 1000 == 0:
            print('on row {}'.format(i))
        if row['start_date'].year == year:
            # find data for date
            df_temp = df_fc[df_fc.index.get_level_values('time').date == row['start_date'].date()]
            # see if data is available, if not append NaN
            try:
                # find closest latitude data
                lat = df_temp.iloc[abs((df_temp.index.get_level_values('latitude')-row['lat'])).argsort()[:1]].index.get_level_values('latitude').values[0]
                df_temp = df_temp[df_temp.index.get_level_values('latitude') == lat]
                # find closest longitude data
                lon = df_temp.iloc[abs((df_temp.index.get_level_values('longitude')-(row['lon']+360))).argsort()[:1]].index.get_level_values('longitude').values[0]
                df_temp = df_temp[df_temp.index.get_level_values('longitude') == lon]
                # add datapoints
                for variable in cols:
                    df.at[i,variable] = df_temp.iloc[0][variable]
            except:
                pass
