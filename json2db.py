import json
import sqlite3
import time
import datetime
import os
from datetime import timedelta
from datetime import date
import re

def conv_time(stamp):
    pass
    #'2020-09-21T01:22:18.428Z'
    result = re.split(r'[-T:.Z]', stamp)
    #print(result)
    return result


os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = "data.db"
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
try:
    c.execute('DROP TABLE IF EXISTS expart')
except:
    pass
c.execute('create table if not exists expart ("timestampMs","year","mon","day","hour","min","sec", "latitudeE7","longitudeE7")')
#c.execute('create table table_name (timestampMs,latitudeE7,longitudeE7)')

json_open=open("./input_data/Records.json","r",encoding="utf-8_sig")
json_load=json.load(json_open)
for i in json_load["locations"]:
    data = list()
    epoch_time = i["timestamp"]
    dt=conv_time(epoch_time)
    #dt = time.localtime(epoch_time)
    data.append(epoch_time)

    for j in range(6):
        data.append(int(dt[j]))

    data.append(i["latitudeE7"]/10000000)
    data.append(i["longitudeE7"]/10000000)
    
    c.execute('insert into expart values (?,?,?,?,?,?,?,?,?)', data)
    #print(i["timestampMs"])
    ###print("/")
    
#print(json_load)




conn.commit()
c.close()