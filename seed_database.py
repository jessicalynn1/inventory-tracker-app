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

for city in CITIES:
    c = model.Warehouse(name=city)
    model.db.session.add(c)
    model.db.session.commit()
