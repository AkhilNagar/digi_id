import unittest
from app import app

class TestApp(unittest.TestCase):

    def test_index(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome to container no.:', response.data)
            print(response.data)
