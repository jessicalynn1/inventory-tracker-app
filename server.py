from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, Inventory, Warehouse
import model

from jinja2 import StrictUndefined
import os
import webbrowser
import requests
import json 
from pprint import pprint

app = Flask(__name__, static_url_path='/static') 
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
api_key = os.environ["API_KEY"]
api_key_2 = os.environ["API_KEY_2"]


@app.route("/")
def homepage():
    """Asks what you'd like to do."""

    return render_template("homepage.html")


@app.route("/create_inventory")
def create_inventory():
    """Loads new inventory item form"""

    warehouse_table = Warehouse.query.all()
           
    return render_template("create_inventory.html", warehouse_table=warehouse_table)


@app.route("/commit_inventory", methods=["POST"])
def commit_inventory():
    """Allows user to create a new inventory item"""
    
    product_code = request.form.get("product-code")
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    warehouse_name = request.form.get("warehouse")
    warehouse_id = Warehouse.query.filter_by(name=warehouse_name).first()

    new_product = Inventory(product_code=product_code, name=name, description=description, quantity=quantity, warehouse_id=warehouse_id.id)
    db.session.add(new_product)
    db.session.commit()


    return redirect("/")


@app.route("/edit_inventory")
def edit_inventory():
    """Loads the edit inventory form"""

    inventory_table = Inventory.query.all()
    warehouse_table = Warehouse.query.all()

    return render_template("edit_inventory.html", inventory_table=inventory_table, warehouse_table=warehouse_table)


@app.route("/commit_edit", methods=["POST"])
def commit_edit():
    """Allows user to edit an existing inventory item"""
    
    deleted = request.form.get("deleted")
    item = Inventory.query.filter_by(name=deleted).first()
    db.session.delete(item)
    db.session.commit()

    product_code = request.form.get("product-code")
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    warehouse_name = request.form.get("warehouse")
    warehouse_id = Warehouse.query.filter_by(name=warehouse_name).first()

    new_product = Inventory(product_code=product_code, name=name, description=description, quantity=quantity, warehouse_id=warehouse_id.id)
    db.session.add(new_product)
    db.session.commit()

    return redirect("/")


@app.route("/delete_inventory")
def delete_inventory():
    """Allows user to delete an existing inventory item"""

    inventory_table = Inventory.query.all()
           
    return render_template("delete_inventory.html", inventory_table=inventory_table)


@app.route("/commit_delete", methods=["POST"])
def commit_delete():
    """Allows user to delete an existing inventory item"""
    
    deleted = request.form.get("deleted")
    item = Inventory.query.filter_by(name=deleted).first()
    db.session.delete(item)
    db.session.commit()
           
    return redirect("/")


@app.route("/create_warehouse")
def create_warehouse():
    """Allows user to create a new warehouse location"""
    
    warehouse_table = Warehouse.query.all()

    return render_template("create_warehouse.html", warehouse_table=warehouse_table)


@app.route("/commit_warehouse", methods=["POST"])
def commit_warehouse():
    """Allows user to create a new warehouse location"""
    
    location = request.form.get("location")
    db_location = Warehouse.query.filter_by(name=location).first()
    limit = 1

    city = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit={limit}&appid={api_key}')
    city = city.json()
    lat = city[0]["lat"]
    lon = city[0]["lon"]

    if not db_location:
        warehouse_location = Warehouse(name=location, lat=lat, lon=lon)
        db.session.add(warehouse_location)
        db.session.commit()
    else:
        flash("This warehouse location already exists.")

    return redirect("/")


@app.route("/view_inventory", methods=["GET"])
def view_inventory():
    """Allows user to search for inventory items"""
    

    inventory_table = Inventory.query.all()
    
    for obj in inventory_table:
        city_name = obj.warehouse.name
        lat = obj.warehouse.lat
        lon = obj.warehouse.lon

        weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key_2}')
        response = weather.json()
        description = response['weather'][0]['description']

        model.Warehouse.query.filter_by(name=city_name).update(dict(weather=description))
        model.db.session.commit()

           
    return render_template("view_inventory.html", inventory_table=inventory_table)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)




#Tried to use a class to connect the city with the inventory item and the weather
        
    # class FullInventory:
    #     """Creates an object that has information from both inventory table and warehouse table."""
    #     def __init__(self, product_name, city_name, description):

    #         self.pname = product_name
    #         self.cname = city_name
    #         self.desc = description
        
    #     def create_instance(self):
    #         """Puts all the info into one object"""