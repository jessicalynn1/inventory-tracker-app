import os
import json
import requests
from pprint import pprint

from model import connect_to_db, db, Inventory, Warehouse
import server


os.system("createdb Inventory")
os.system("createdb Warehouse")
connect_to_db(server.app)
db.create_all()



