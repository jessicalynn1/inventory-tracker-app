# Chris's Custom Designs
## Overview
Chris's Custom Designs is the backend of an online retailer with warehouse locations and inventory stored across the US.

Chris's Custom Designs is built with Python Flask on the backend with a PostgreSQL database, and HTML on the frontend. 


## Features 
#### View all inventory  
Users can view all inventory, including their warehouse locations and current weather.



#### Create new inventory item
Users can create a new inventory item.



#### Create new warehouse location
Users can create a new warehouse item.



#### Edit inventory items
Users can edit an inventory item.



#### Delete inventory items
Users can delete an inventory item.



## Technologies
Languages:
- Python 3
- HTML


Frameworks & Libraries:
- Flask
- Jinja


Database:
 - PostgreSQL / SQLAlchemy


## Getting Started  
Please read through and follow the steps below to get the app running.
To download and use Chris's Custom Designs please follow these instructions:
1. Clone repository: 
    https://github.com/jessicalynn1/inventory-tracker-app
2. Create a virtual environment: 
    $ virtualenv env
3. Install dependencies: 
    $ pip3 install -r requirements.txt
4. Build database tables and fill database with seed file: 
    $ python3 model.py
    $ python3 seed_database.py


## View on Replit
You can find this app on Replit here: https://replit.com/@JessicaF1/inventory-tracker-app-2#main.py


## Coming Soon...
A few ideas of features to add in the future: 
- Adding an API that shows the weather of each warehouse location
- Adding some front end design to "make it look pretty"
- Add ability for users to delete a warehouse location 