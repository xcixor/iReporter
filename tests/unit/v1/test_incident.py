"""Contains the tests for a record."""
import json

import unittest

from app import create_app


class TestRecord(unittest.TestCase):
    """Test record's functionality."""

    def setUp(self):
        """Initialize objects for testing."""
        self.incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "23.0, 34.5",
            "Comment": "Thieves thieves thieves"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client

    def tearDown(self):
        """Remove instance variables."""
        del self.incident

    def test_create_incident_with_valid_data_true(self):
        """Test an incident can be created successfuly."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        res = res.get_json()
        self.assertEqual(res['data']['message'],
                         'Successfuly created incident')

    def test_incident_with_one_coordinate_false(self):
        """Test coordinate should have longitude and latitude."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "34.5",
            "Comment": "Thieves thieves thieves"
        }
        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0], 'Two coordinates required')

    def test_create_incident_with_non_floating_point_values_false(self):
        """Test incident coordinates are floating point values."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "34.5, string",
            "Comment": "Thieves thieves thieves"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Coordinates should be floating point values')

    def test_create_incident_without_created_by_false(self):
        """Test incident coordinates are floating point values."""
        incident = {
            "Created By": "",
            "Type": "red-flag",
            "Location": "34.5, 45.6",
            "Comment": "Thieves thieves thieves"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Incident owner should not be blank')

    def test_create_incident_without_location_false(self):
        """Test incident coordinates are floating point values."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "",
            "Comment": "Thieves thieves thieves"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Location should not be empty')

    def test_create_incident_without_type_false(self):
        """Test incident coordinates are floating point values."""
        incident = {
            "Created By": 1,
            "Type": "",
            "Location": "23.5, 34.6",
            "Comment": "Thieves thieves thieves"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Incident type should not be empty')

    def test_create_incident_without_comment_false(self):
        """Test incident coordinates are floating point values."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "23.5, 34.6",
            "Comment": "      "
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Comments cannot be empty')

    def test_create_incident_with_wrong_type_false(self):
        """Test incident coordinates are floating point values."""
        incident = {
            "Created By": 1,
            "Type": "a report",
            "Location": "23.5, 34.6",
            "Comment": "This clerks are corrupt"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        err_msg = 'Incident type should either be a \'red-flag\' or {0}'.\
                  format("\'intervention\'")
        self.assertEqual(res['errors'][0], err_msg)

    def test_create_incident_with_non_integer_created_by_id_false(self):
        """Test created by Id is an integer."""
        incident = {
            "Created By": "ptah",
            "Type": "red-flag",
            "Location": "23.5, 34.6",
            "Comment": "This clerks are corrupt"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0], "Created by should be an Integer")

    def test_get_existing_incident_true(self):
        """Test can get existing record."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/api/v1/incidents/1')
        self.assertEqual(result.status_code, 200)
        result = result.get_json()
        self.assertDictContainsSubset(self.incident, result['data'])

    def test_get_non_existing_incident_false(self):
        """Test cannot get non existing incident."""
        res = self.client().get('/api/v1/incidents/5')
        print(res.get_json())
        self.assertEqual(res.status_code, 404)
        res = res.get_json()
        self.assertEqual(res['error'], "That resource cannot be found")

    def test_get_all_incidences_true(self):
        """Test user can get all incidences."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        incident = {
            "Created By": 2,
            "Type": "intervention",
            "Location": "23.0, 34.5",
            "Comment": "Clerks are take a bribe"
        }
        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/api/v1/incidents')
        self.assertEqual(result.status_code, 200)
        result = result.get_json()
        self.assertEqual(len(result['data']), 2)

    def test_get_non_existing_incidences_false(self):
        """Test app doesn't crash if there are no incidences."""
        result = self.client().get('/api/v1/incidents')
        self.assertEqual(result.status_code, 404)
        result = result.get_json()
        self.assertEqual(len(result['data']),
                         "There are no incidences at the moment")
