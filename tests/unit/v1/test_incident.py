"""Contains the tests for a record."""
import unittest

from app import create_app

from app.api_1_0.views import db


class TestRecord(unittest.TestCase):
    """Test record's functionality."""

    def setUp(self):
        """Initialize objects for testing."""
        self.incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "23.0, 34.5",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client

    def tearDown(self):
        """Remove instance variables."""
        del self.incident
        db.clear()

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
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
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
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Coordinates should be floating point values')

    def test_create_incident_without_created_by_false(self):
        """Test user cannot create incident without incidence owner."""
        incident = {
            "Created By": "",
            "Type": "red-flag",
            "Location": "34.5, 45.6",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Incident owner should not be blank')

    def test_create_incident_without_location_false(self):
        """Test user cannot create incidence without location."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Location should not be empty')

    def test_create_incident_without_type_false(self):
        """Test user cannot create incident without Type."""
        incident = {
            "Created By": 1,
            "Type": "",
            "Location": "23.5, 34.6",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Incident type should not be empty')

    def test_create_incident_without_comment_false(self):
        """Test cannot create incident without comments."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "23.5, 34.6",
            "Comment": "      ",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Comments cannot be empty')

    def test_create_incident_without_title_false(self):
        """Test user cannot create incident without title."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "23.5, 34.6",
            "Comment": "Officers in this office are taking....",
            "Title": ""
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Title cannot be empty')

    def test_create_incident_without_special_characters_title_false(self):
        """Test cannot create incident with special characters title."""
        incident = {
            "Created By": 1,
            "Type": "red-flag",
            "Location": "23.5, 34.6",
            "Comment": "Officers in this office are taking....",
            "Title": "***&&&&"
        }

        res = self.client().post('/api/v1/incidents', data=incident)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Title cannot contain special characters')

    def test_create_incident_with_wrong_type_false(self):
        """Test cannot create incident with the wrong type."""
        incident = {
            "Created By": 1,
            "Type": "a report",
            "Location": "23.5, 34.6",
            "Comment": "This clerks are corrupt",
            "Title": "Corruption of the highest order"
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
            "Comment": "This clerks are corrupt",
            "Title": "Corruption of the highest order"
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
            "Comment": "Clerks are take a bribe",
            "Title": "Corruption of the highest order"
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
        self.assertEqual(result['data'],
                         "There are no incidences at the moment")

    def test_edit_existing_record_true(self):
        """Test user can edit an incidences."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Created By": 2,
            "Type": "intervention",
            "Location": "22.0, 34.5",
            "Comment": "Clerks are take a bribe",
        }
        res = self.client().put('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 201)

    def test_edit_non_existing_record_false(self):
        """Test user cannot edit a non exisitng incident."""
        edit_data = {
            "Created By": 2,
            "Type": "red-flag",
            "Location": "22.0, 34.5",
            "Comment": "Clerks are take a bribe"
        }
        res = self.client().put('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 404)
        res = res.get_json()
        self.assertEqual(
            res['error'], "That resource cannot be found")

    def test_delete_existing_incident_true(self):
        """Test user can delete an incident successfuly."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        result = self.client().delete('/api/v1/incidents/1')
        self.assertEqual(result.status_code, 200)
        result = result.get_json()
        self.assertEqual(
            result['data'], "Incident successfuly deleted")

    def test_delete_non_existing_incident_false(self):
        """Test user can delete an incident successfuly."""
        result = self.client().delete('/api/v1/incidents/1')
        self.assertEqual(result.status_code, 404)
        result = result.get_json()
        self.assertEqual(
            result['error'], "That resource cannot be found")

    def test_edit_existing_record_comment_true(self):
        """Test user can edit an incidences."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Comment": "Clerks are taking bribes"
        }
        res = self.client().patch('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 200)
        res = res.get_json()
        self.assertEqual(res['data']['message'], "Updated red-flag record’s comment")

    def test_edit_non_existing_record_comment_false(self):
        """Test user cannot edit a non exisitng incident."""
        edit_data = {
            "Comment": "Clerks are taking bribes"
        }
        res = self.client().patch('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 404)
        res = res.get_json()
        self.assertEqual(
            res['error'], "That resource cannot be found")

    def test_edit_existing_record_comment_true(self):
        """Test user can edit an incidences."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Location": "23.4, 23.6"
        }
        res = self.client().patch('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 200)
        res = res.get_json()
        self.assertEqual(res['data']['message'],
                         "Updated incident location")

    def test_edit_non_existing_record_comment_false(self):
        """Test user cannot edit a non exisitng incident."""
        edit_data = {
            "Location": "23.4, 23.6"
        }
        res = self.client().patch('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 404)
        res = res.get_json()
        self.assertEqual(
            res['error'], "That resource cannot be found")

    def test_edit_record_with_invalid_location_false(self):
        """Test user cannot edit location with invalid location."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Location": "23.io, lat"
        }
        res = self.client().patch('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['error'],
                         "Coordinates should be floating point values")

    def test_edit_record_with_only_one_location_false(self):
        """Test user cannot edit location with invalid location."""
        res = self.client().post('/api/v1/incidents', data=self.incident)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Location": "23.7"
        }
        res = self.client().patch('/api/v1/incidents/1', data=edit_data)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['error'],
                         "Two coordinates required")
