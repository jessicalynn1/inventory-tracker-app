import server
import os
import json
import requests
from pprint import pprint

from model import connect_to_db, db, Inventory, Warehouse
import model


os.system("createdb Inventory")
os.system("createdb Warehouse")
connect_to_db(server.app)
db.create_all()


CITIES = ["Denver", "San Jose", "Philadelphia", "Atlanta", "Chicago"]
api_key = "b61401ee0365e42673899dda2db91f00"
limit = 1


for city in CITIES:

    location = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}')
    location = location.json()
    lat = location[0]["lat"]
    lon = location[0]["lon"]

    c = model.Warehouse(name=city, lat=lat, lon=lon)
    model.db.session.add(c)
    model.db.session.commit()
