"""Contains the tests for a record."""

import unittest

from app.v1.controller import Controller


class TestRecord(unittest.TestCase):
    """Test record's functionality."""

    def setUp(self):
        self.controller = Controller()
        self.incident = {
            "Id": 1,
            "created_on": "21/11/2018",
            "created_by": "ptah",
            "type": "red-flag",
            "location": "23.0, 45.02",
            "status": "pending",
            "images": [],
            "videos": [],
            "comment": "The county clerk is asking for bribes to award tenders"
        }

    def tearDown(self):
        """Remove instance variables."""
        del self.incident
        del self.controller

    def test_create_incident_success(self):
        """Test an incident can be created successfuly."""
        res = self.controller.create_incident(self.incident)
        self.assertTrue(res['status'])
        self.assertEqual(res['message'], 'Incident created successfuly')
