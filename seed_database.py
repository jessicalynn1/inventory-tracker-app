import server
import model
import os
import json
import requests
from pprint import pprint
from model import connect_to_db, db, Inventory, Warehouse

connect_to_db(server.app)
db.drop_all()
db.create_all()

api_key = "b61401ee0365e42673899dda2db91f00"
api_key_2 = "93b423527d6806d147c30e1558064431"

CITIES = ["Denver", "San Jose", "Philadelphia", "Atlanta", "Chicago"]
limit = 1

for city in CITIES:

    location = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}')
    location = location.json()
    lat = location[0]["lat"]
    lon = location[0]["lon"]

    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key_2}')
    response = weather.json()
    description = response['weather'][0]['description']

    c = Warehouse(name=city, lat=lat, lon=lon, weather=description)
    db.session.add(c)
    db.session.commit()
