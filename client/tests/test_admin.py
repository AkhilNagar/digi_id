import sys
import unittest
import pymongo
import certifi
from unittest.mock import patch, MagicMock
from io import StringIO
global conn
from admin import connect,view_event
global db
class TestConnect(unittest.TestCase):
    @patch('builtins.input', side_effect=["1"])
    def test_connect_client1(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            connect()
            self.assertIn("Connection Successful", fake_output.getvalue())
        self.assertIsInstance(conn, pymongo.MongoClient)
        self.assertEqual(conn.address, ("client.du8czbz.mongodb.net", 27017))

    @patch('builtins.input', side_effect=["2"])
    def test_connect_client2(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            connect()
            self.assertIn("Connection Successful", fake_output.getvalue())
        self.assertIsInstance(conn, pymongo.MongoClient)
        self.assertEqual(conn.address, ("client.nraxkyn.mongodb.net", 27017))

class TestViewEvent(unittest.TestCase):
    def setUp(self):
        # Set up mock data for the tests
        self.mock_event = {
            "name": "Birthday Party",
            "capacity": 50
        }
        self.mock_user_count = 10

    @patch('sys.stdout', new=StringIO())
    def test_view_event(self):
        # Mock the database queries
        mock_event_query = MagicMock(return_value=self.mock_event)
        mock_user_count_query = MagicMock(return_value=self.mock_user_count)
        db.details.find_one = mock_event_query
        db.users.count_documents = mock_user_count_query

        # Call the function
        view_event()

        # Check the output
        expected_output = "Event Name Birthday Party\nCapacity 50\nCount 10\n"
        self.assertEqual(expected_output, sys.stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
