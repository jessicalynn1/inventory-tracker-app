from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)


class Inventory(db.Model):
    """Table to keep track of inventory items"""

    __tablename__ = 'inventory'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    product_code = db.Column(db.String, unique=True)
    name = db.Column(db.String, unique=False)
    description = db.Column(db.String, unique=False)
    quantity = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.id"))

    warehouse = db.relationship("Warehouse", backref="inventory")

    def __repr__(self):
        return f'<Inventory product_code={self.product_code} name={self.name} quantity={self.quantity}>'


class Warehouse(db.Model):
    """Table to keep track of warehouses"""

    __tablename__ = 'warehouse'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)
    weather = db.Column(db.String, unique=False, Nullable=False) 


    def __repr__(self):
        return f'<Warehouse id={self.id} name={self.name}>'




def connect_to_db(app, db_uri="postgresql://popkjngt:VvqKa5kCap5HUaVA0DapnqqOVf6RHSxV@heffalump.db.elephantsql.com/popkjngt", echo=False):
    """Connect the database to the Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = echo
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
