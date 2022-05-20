import os
import json
import requests
from pprint import pprint

from model import connect_to_db, db, Inventory, Warehouse
import server
import model


os.system("createdb Inventory")
os.system("createdb Warehouse")
connect_to_db(server.app)
db.create_all()


CITIES = ["Denver", "San Jose", "Philadelphia", "Atlanta", "Chicago"]

for city in CITIES:
    c = model.Warehouse(name=city)
    model.db.session.add(c)
    model.db.session.commit()


# This is converting the city into lat and lon to use in the weather call
# get city, state and country from warehouse table, pass through api to get lat and lon
location = requests.get('http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={93b423527d6806d147c30e1558064431}')
location = location.json()

# This is the weather call using lat and lon above
res = requests.get('https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={93b423527d6806d147c30e1558064431}')
response = res.json()