"""Contains the tests for a user."""
import unittest

from app import create_app

from app.api_1_0 import users


class TestUser(unittest.TestCase):
    """Tests user's functionality."""

    def setUp(self):
        self.user = {
            "Email": "user@example.com",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client

    def test_signup_with_valid_credentials_success(self):
        """Test user can register."""
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = res.get_json()
        self.assertEqual(res['data']['message'], 'You have successfuly signed up')

    def test_signup_with_invalid_email_false(self):
        """Test email is valid."""
        user = {
            "Email": "user@example.com",
            "Password": "pass1234",
            "Confirm Password": "pass1234"
        }
        res = self.client().post('/api/v1/auth/signup', data=user)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Invalid Email Address')

    def test_signup_user_with_short_password_false(self):
        """Test password is long enough."""
        user = {
            "Email": "user@example.com",
            "Password": "pass",
            "Confirm Password": "pass"
        }
        res = self.client().post('/api/v1/auth/signup', data=user)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Password should be atleast eight characters')

    def test_signup_user_with_mistmatching_passwords_false(self):
        """Test passwords match."""
        user = {
            "Email": "user@example.com",
            "Password": "pass1234",
            "Confirm Password": "pass5678"
        }
        res = self.client().post('/api/v1/auth/signup', data=user)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Passwords should match')

    def test_multiple_signup_false(self):
        """Test user cannot register more than once."""
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res['errors'][0],
                         'That emails password is already taken')
