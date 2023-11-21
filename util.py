import numpy as np
import pandas as pd

def add_geospatial_data(df,df_fc,variable):
    data = []
    for i, row in df.iterrows():
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
            # add datapoint 
            data.append(df_temp.iloc[0][variable])
        except:
            data.append(np.NaN)

    df[variable] = data
