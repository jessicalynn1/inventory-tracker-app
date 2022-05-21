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
    api_key = "b61401ee0365e42673899dda2db91f00"
    limit = 5

    new_product = Inventory(product_code=product_code, name=name, description=description, quantity=quantity, warehouse_id=warehouse_id.id)
    db.session.add(new_product)
    db.session.commit()

    location = requests.get('http://api.openweathermap.org/geo/1.0/direct?q={warehouse_name}&limit={limit}&appid={api_key}')
    location = location.json()
    pprint(location)
    # this saves the weather data in the warehouse database
    # city = Warehouse(name=warehouse_name, weather=weather)
    # db.session.add(city)
    # db.session.commit()
           
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
    item = Inventory.query.filter_by(product_code=deleted).first()
    print(item)
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

    if not db_location:
        warehouse_location = Warehouse(name=location)
        db.session.add(warehouse_location)
        db.session.commit()
    else:
        flash("This warehouse location already exists.")

    return redirect("/")


@app.route("/view_inventory", methods=["GET"])
def view_inventory():
    """Allows user to search for inventory items"""
    
    inventory_table = Inventory.query.all()
    warehouse_table = Warehouse.query.all()
    # api_key = "b61401ee0365e42673899dda2db91f00"
    # limit = 5

    #this will get me a list of all the warehouse city locations
    for item in warehouse_table:
        name = item.name
        warehouse_name = Warehouse.query.filter_by(name=name).all()
    
        return warehouse_name

    # location = requests.get('http://api.openweathermap.org/geo/1.0/direct?q={warehouse_name}&limit={limit}&appid={api_key}')
    # location = location.json()
    # pprint(location)
    # lat = location["lat"]
    # lon = location["lon"]

    # weather = requests.get('https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={93b423527d6806d147c30e1558064431}')
    # response = weather.json()
    # desc = response[weather]    #this is a list of dictionaries
    # desc = desc["description"] 


    # this saves the weather data in the warehouse database
    # city = Warehouse(name=warehouse_name, weather=weather)
    # db.session.add(city)
    # db.session.commit()
           
    return render_template("view_inventory.html", inventory_table=inventory_table, warehouse_table=warehouse_table)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)