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
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Remove instance variables."""
        del self.incident
        self.app_context.pop()

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
