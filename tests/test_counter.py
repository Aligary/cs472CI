"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        result = self.client.post('/counters/cou')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result.json['cou'], 0)

        put = self.client.put('/counters/cou')
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(put.json['cou'], 1)

        put = self.client.put('/counters/coo')
        self.assertEqual(put.status_code, status.HTTP_409_CONFLICT)

    def test_read_counter(self):
        """It should read a counter"""
        result = self.client.post('/counters/rea')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        get = self.client.get('/counters/rea')
        self.assertEqual(get.json["count"], "0")
        self.assertEqual(get.status_code, status.HTTP_200_OK)

        self.client.put('/counters/rea')
        get = self.client.get('/counters/rea')
        self.assertEqual(get.json["count"], "1")
        self.assertEqual(get.status_code, status.HTTP_200_OK)

        get = self.client.get('/counters/ree')
        self.assertEqual(get.status_code, status.HTTP_409_CONFLICT)

    def test_delete_counter(self):
        """It should delete a counter"""
        # Create a counter to delete
        result = self.client.post('/counters/del')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Delete the counter
        delete_result = self.client.delete('/counters/del')
        self.assertEqual(delete_result.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the counter has been deleted
        get_result = self.client.get('/counters/del')
        self.assertEqual(get_result.status_code, status.HTTP_409_CONFLICT)

