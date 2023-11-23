# Import Meteostat library and dependencies
import datetime
import numpy as np
import pandas as pd
import sqlite3

conn = sqlite3.connect("C:\\Users\\scott\\Downloads\\FPA_FOD_20221014.sqlite")

c = conn.cursor()

query = 'SELECT * FROM Fires ORDER BY RANDOM() LIMIT 10000'
df = pd.read_sql_query(query,conn)

df = df.rename(columns={'OBJECTID':'id','FIRE_NAME':'name','DISCOVERY_DATE':'start_date','NWCG_CAUSE_CLASSIFICATION':'cause',
                        'CONT_DATE':'end_date','FIRE_SIZE':'size','LATITUDE':'lat','LONGITUDE':'lon','STATE':'state',
                        'FIRE_CLASS_SIZE':'fire_size_class'})

print("Minimum lat: {}".format(np.min(df['lat'])))
print("Maximum lat: {}".format(np.max(df['lat'])))
print("Minimum lon: {}".format(np.min(df['lon'])))
print("Maximum lon: {}".format(np.max(df['lon'])))
print("Minimum start date: {}".format(np.min(df['start_date'])))
print("Maximum start date: {}".format(np.max(df['start_date'])))

