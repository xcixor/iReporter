"""Contains the tests for an redflag."""
import unittest

from app import create_app

from app.api_1_0.views import db


class TestRecord(unittest.TestCase):
    """Test record's functionality."""

    def setUp(self):
        """Initialize objects for testing."""
        self.redflag = {
            "Created By": 1,
            "Location": "23.0, 34.5",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client

    def tearDown(self):
        """Remove instance variables."""
        del self.redflag
        db.clear()

    def test_create_redflag_with_valid_data_true(self):
        """Test an redflag can be created successfuly."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        res = res.get_json()
        self.assertEqual(res['data']['message'],
                         'Successfuly created redflag')

    def test_redflag_with_one_coordinate_false(self):
        """Test coordinate should have longitude and latitude."""
        redflag = {
            "Created By": 1,
            "Location": "34.5",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }
        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0], 'Two coordinates required')

    def test_create_redflag_with_non_floating_point_values_false(self):
        """Test redflag coordinates are floating point values."""
        redflag = {
            "Created By": 1,
            "Location": "34.5, string",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Coordinates should be floating point values')

    def test_create_redflag_without_created_by_false(self):
        """Test user cannot create redflag without redflag owner."""
        redflag = {
            "Created By": "",
            "Location": "34.5, 45.6",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'redflag owner should not be blank')

    def test_create_redflag_without_location_false(self):
        """Test user cannot create redflag without location."""
        redflag = {
            "Created By": 1,
            "Location": "",
            "Comment": "Thieves thieves thieves",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Location should not be empty')


    def test_create_redflag_without_comment_false(self):
        """Test cannot create redflag without comments."""
        redflag = {
            "Created By": 1,
            "Location": "23.5, 34.6",
            "Comment": "      ",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Comments cannot be empty')

    def test_create_redflag_without_title_false(self):
        """Test user cannot create redflag without title."""
        redflag = {
            "Created By": 1,
            "Location": "23.5, 34.6",
            "Comment": "Officers in this office are taking....",
            "Title": ""
        }

        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Title cannot be empty')

    def test_create_redflag_without_special_characters_title_false(self):
        """Test cannot create redflag with special characters title."""
        redflag = {
            "Created By": 1,
            "Location": "23.5, 34.6",
            "Comment": "Officers in this office are taking....",
            "Title": "***&&&&"
        }

        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Title cannot contain special characters')

    def test_create_redflag_with_non_integer_created_by_id_false(self):
        """Test created by Id is an integer."""
        redflag = {
            "Created By": "ptah",
            "Location": "23.5, 34.6",
            "Comment": "This clerks are corrupt",
            "Title": "Corruption of the highest order"
        }

        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0], "Created by should be an Integer")

    def test_get_existing_redflag_true(self):
        """Test can get existing record."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/api/v1/redflags/1')
        self.assertEqual(result.status_code, 200)
        result = result.get_json()
        self.assertDictContainsSubset(self.redflag, result['data'])

    def test_get_non_existing_redflag_false(self):
        """Test cannot get non existing redflag."""
        res = self.client().get('/api/v1/redflags/5')
        print(res.get_json())
        self.assertEqual(res.status_code, 404)
        res = res.get_json()
        self.assertEqual(res['error'], "That resource cannot be found")

    def test_get_all_redflags_true(self):
        """Test user can get all redflags."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        redflag = {
            "Created By": 2,
            "Location": "23.0, 34.5",
            "Comment": "Clerks are take a bribe",
            "Title": "Corruption of the highest order"
        }
        res = self.client().post('/api/v1/redflags', data=redflag)
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/api/v1/redflags')
        self.assertEqual(result.status_code, 200)
        result = result.get_json()
        self.assertEqual(len(result['data']), 2)

    def test_get_non_existing_redflags_false(self):
        """Test app doesn't crash if there are no redflags."""
        result = self.client().get('/api/v1/redflags')
        self.assertEqual(result.status_code, 404)
        result = result.get_json()
        self.assertEqual(result['data'],
                         "There are no redflags at the moment")

    def test_delete_existing_redflag_true(self):
        """Test user can delete an redflag successfuly."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        result = self.client().delete('/api/v1/redflags/1')
        self.assertEqual(result.status_code, 200)
        result = result.get_json()
        self.assertEqual(
            result['data'], "redflag successfuly deleted")

    def test_delete_non_existing_redflag_false(self):
        """Test user can delete an redflag successfuly."""
        result = self.client().delete('/api/v1/redflags/1')
        self.assertEqual(result.status_code, 404)
        result = result.get_json()
        self.assertEqual(
            result['error'], "That resource cannot be found")

    def test_edit_existing_record_comment_true(self):
        """Test user can edit an redflags."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Comment": "Clerks are taking bribes"
        }
        res = self.client().patch('/api/v1/redflags/1/comments', data=edit_data)
        self.assertEqual(res.status_code, 200)
        res = res.get_json()
        self.assertEqual(res['data']['message'], "Updated red-flag record’s comment")

    def test_edit_existing_record_with_blank_comment_false(self):
        """Test user cannot edit an redflag comment without a comment."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Comment": ""
        }
        res = self.client().patch('/api/v1/redflags/1/comments', data=edit_data)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['error'][0], "Comments cannot be empty")

    def test_edit_non_existing_record_comment_false(self):
        """Test user cannot edit a non exisitng redflag."""
        edit_data = {
            "Comment": "Clerks are taking bribes"
        }
        res = self.client().patch('/api/v1/redflags/1/comments', data=edit_data)
        self.assertEqual(res.status_code, 404)
        res = res.get_json()
        self.assertEqual(
            res['error'], "That resource cannot be found")

    def test_edit_existing_record_location_true(self):
        """Test user can edit an redflags."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Location": "23.4, 23.6"
        }
        res = self.client().patch('/api/v1/redflags/1/location', data=edit_data)
        self.assertEqual(res.status_code, 200)
        res = res.get_json()
        self.assertEqual(res['data']['message'],
                         "Updated redflag location")

    def test_edit_non_existing_record_location_false(self):
        """Test user cannot edit a non exisitng redflag."""
        edit_data = {
            "Location": "23.4, 23.6"
        }
        res = self.client().patch('/api/v1/redflags/1/location', data=edit_data)
        self.assertEqual(res.status_code, 404)
        res = res.get_json()
        self.assertEqual(
            res['error'], "That resource cannot be found")

    def test_edit_record_with_invalid_location_false(self):
        """Test user cannot edit location with invalid location."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Location": "23.io, lat"
        }
        res = self.client().patch('/api/v1/redflags/1/location', data=edit_data)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['error'][0],
                         "Coordinates should be floating point values")

    def test_edit_record_with_only_one_location_false(self):
        """Test user cannot edit location with invalid location."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Location": "23.7"
        }
        res = self.client().patch('/api/v1/redflags/1/location', data=edit_data)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['error'][0],
                         "Two coordinates required")

    def test_edit_record_with_missing_location_false(self):
        """Test user cannot edit location with empty location."""
        res = self.client().post('/api/v1/redflags', data=self.redflag)
        self.assertEqual(res.status_code, 201)
        edit_data = {
            "Location": ""
        }
        res = self.client().patch('/api/v1/redflags/1/location', data=edit_data)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['error'][0],
                         "Location should not be empty")