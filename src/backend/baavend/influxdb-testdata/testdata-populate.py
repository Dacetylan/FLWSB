from datetime import datetime
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb import DataFrameClient
import pandas as pd
import numpy as np

token = os.environ.get('DB_TOKEN')
org = os.environ.get('DB_ORG')
url = os.environ.get('DB_URL')
bucket = os.environ.get('DB_BUCKET')

data = pd.read_feather("./testdata-RL18.feather")
data.station = pd.to_numeric(data.station, downcast='integer')

# drop soil moisture predictions due to missing values
# Note that self is a minor change compared to the paper, but does not have a significant effect
data = data.drop(['sm_mean', 'sm_var'], axis=1)

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
columns = list(data.columns)
columns.remove("date")
write_api = client.write_api(write_options=SYNCHRONOUS)


data_frame = data
data_frame = data_frame[(data_frame['date'].dt.year==2015)&(data_frame['station']==10)]

data_frame.index = data_frame['date']
# DataFrame must have the timestamp column as an index for the client. 
write_api.write(bucket=bucket, record=data_frame, data_frame_measurement_name='obs', data_frame_tag_columns=columns)


my_token = os.environ.get('DB_TOKEN')
my_org = os.environ.get('DB_ORG')
url = os.environ.get('DB_URL')
bucket = os.environ.get('DB_BUCKET')
query = '''
from(bucket: "flwsb")
|> range(start:-15y, stop: now())
|> filter(fn: (r) => r._measurement == "obs")
|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
'''


client = InfluxDBClient(url=url, token=my_token, org=my_org, debug=False)
system_stats = client.query_api().query_data_frame(org=my_org, query=query)
print(system_stats.head())
