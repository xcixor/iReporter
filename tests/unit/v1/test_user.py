"""Contains the tests for a user."""
import unittest

from app import create_app

from app.api_1_0.views import users, logged_in


class TestUser(unittest.TestCase):
    """Tests user's functionality."""

    def setUp(self):
        """Initialize objects for testing."""
        self.user = {
            "Email": "user@example.com",
            "Password": "pass1234",
            "Confirm Password": "pass1234"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client

    def tearDown(self):
        """Clean up after test."""
        users.clear()
        logged_in.clear()

    def test_signup_with_valid_credentials_success(self):
        """Test user can register."""
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = res.get_json()
        self.assertEqual(res['data']['message']['message'], 'You have successfuly signed up')

    def test_signup_with_invalid_email_false(self):
        """Test email is valid."""
        user = {
            "Email": "user.com",
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
        res = res.get_json()
        self.assertEqual(res['errors'][0], 'That email is already taken')

    def test_signup_with_blank_email_false(self):
        """Test email is present."""
        user = {
            "Email": "",
            "Password": "pass1234",
            "Confirm Password": "pass5678"
        }
        res = self.client().post('/api/v1/auth/signup', data=user)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Email should not be blank')

    def test_signup_with_blank_password_false(self):
        """Test password is present."""
        user = {
            "Email": "a@g.com",
            "Password": "",
            "Confirm Password": "pass5678"
        }
        res = self.client().post('/api/v1/auth/signup', data=user)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Password should not be blank')

    def test_signup_with_blank_confirm_password_false(self):
        """Test password is present."""
        user = {
            "Email": "a@g.com",
            "Password": "pass1234",
            "Confirm Password": "    "
        }
        res = self.client().post('/api/v1/auth/signup', data=user)
        self.assertEqual(res.status_code, 400)
        res = res.get_json()
        self.assertEqual(res['errors'][0],
                         'Password should not be blank')

    def test_user_login_with_correct_credentials_true(self):
        """Test user can login."""
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)
        logins = {
            "Email": "user@example.com",
            "Password": "pass1234"
        }
        resp = self.client().post('/api/v1/auth/login', data=logins)
        self.assertEqual(resp.status_code, 200)
        resp = resp.get_json()
        self.assertEqual(resp['data']['message'][0]['Email'], logins['Email'])

    def test_login_wrong_credentials_false(self):
        """Test user cannot login with false credentials."""
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)
        logins = {
            "Email": "user@example.com",
            "Password": "pass4567"
        }
        resp = self.client().post('/api/v1/auth/login', data=logins)
        self.assertEqual(resp.status_code, 400)
        resp = resp.get_json()
        self.assertEqual(resp['errors'],
                         'Invalid password/email combination')

    def test_login_login_inexisting_user_false(self):
        """Test user cannot login with false credentials."""
        logins = {
            "Email": "user@example.com",
            "Password": "pass1234"
        }
        resp = self.client().post('/api/v1/auth/login', data=logins)
        self.assertEqual(resp.status_code, 400)
        resp = resp.get_json()
        self.assertEqual(resp['errors'],
                         'User not found in our database')

    def test_logout_logged_in_user_true(self):
        """Test user can logout."""
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)
        logins = {
            "Email": "user@example.com",
            "Password": "pass1234"
        }
        resp = self.client().post('/api/v1/auth/login', data=logins)
        self.assertEqual(resp.status_code, 200)
        result = self.client().post('/api/v1/auth/logout/1')
        self.assertEqual(result.status_code, 200)
        result = result.get_json()
        self.assertEqual(result['data']['message'],
                         'Successfuly logged out')

    def test_logout_un_logged_in_user_false(self):
        """Test unlogged in user logout fails."""
        resp = self.client().post('/api/v1/auth/logout/1')
        self.assertEqual(resp.status_code, 400)
        resp = resp.get_json()
        self.assertEqual(resp['errors'],
                         'That user is not logged in')
