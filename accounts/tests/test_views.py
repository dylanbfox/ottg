from django.test import TestCase
from django.contrib.auth import get_user_model, SESSION_KEY

from mock import patch

User = get_user_model()

class LoginViewTestCase(TestCase):

	@patch('accounts.views.authenticate')
	def test_gets_logged_in_session_if_authenticate_returns_a_user(self, mock_authenticate):
		user = User.objects.create(email='a@b.com')
		user.backend = ''

		mock_authenticate.return_value = user

		self.client.post('/accounts/login', {'assertion': 'a'})
		self.assertEqual(self.client.session[SESSION_KEY], user.pk)

	@patch('accounts.views.authenticate')
	def test_does_not_get_logged_in_if_authenticate_returns_None(self, mock_authenticate):
		mock_authenticate.return_value = None
		self.client.post('/accounts/login', {'assertion': 'a'})
		self.assertNotIn(SESSION_KEY, self.client.session)

	@patch('accounts.views.authenticate')
	def test_returns_OK_when_user_found(self, mock_authenticate):
		# create a user
		user = User.objects.create(email='a@b.com')
		user.backend = '' # required for auth_login to work

		# configure the Mocked method (authenticate) to return this User
		# as if the authenticate method actually did find a User
		mock_authenticate.return_value = user

		# check that, now the method is returning a User, the view
		# sends back an "OK" string to tell us, well, things are OK!
		response = self.client.post('/accounts/login', {'assertion': 'a'})
		self.assertEqual(response.content.decode(), 'OK')

	@patch('accounts.views.authenticate')
	def test_calls_authenticate_with_assertion_from_post(self, mock_authenticate):
		mock_authenticate.return_value = None
		self.client.post('/accounts/login', {'assertion': 'assert this'})
		mock_authenticate.assert_called_once_with(assertion='assert this')
