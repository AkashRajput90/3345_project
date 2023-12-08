# test_app.py

import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):

    @patch('app.posts_collection.find')
    def test_index_route(self, mock_find):
        # Mock the find method and set the return value
        mock_find.return_value = [
            {'_id': 1, 'title': 'Post 1', 'content': 'Content 1'},
            {'_id': 2, 'title': 'Post 2', 'content': 'Content 2'}
        ]
        
        # Create a test client
        with app.test_client() as client:
            # Make a GET request to '/'
            response = client.get('/')
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            # Additional assertions based on the rendered template or data
            
            # For example, you can check if 'Post 1' exists in the rendered HTML
            self.assertIn(b'Post 1', response.data)


