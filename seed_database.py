import server
import os
import json
import requests
from pprint import pprint
from model import connect_to_db, db, Inventory, Warehouse


# os.system("dropdb Warehouse  --if-exists")
# os.system("createdb Warehouse")
connect_to_db(server.app)
db.drop_all()
db.create_all()

server.app.secret_key = "dev"
api_key = os.environ["API_KEY"]
api_key_2 = os.environ["API_KEY_2"]

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
