"""Script to test Flask routes and server"""

from unittest import TestCase
from server import app
from model import Inventory, Warehouse, connect_to_db, db

import os 


class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///shopifytestdb")


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_homepage(self):
        """Test displaying homepage"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'What would you like to do?', result.data)



#------------------------------------------------------------------#

if __name__ == '__main__':
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')
    
    unittest.main(verbosity=2)