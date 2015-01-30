from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

class MyListsTest(FunctionalTest):

	def create_pre_authenticated_session(self, email):
		if self.against_staging:
			session_key = create_session_on_server(self.server_host, email)
		else:
			session_key = create_pre_authenticated_session(email)

		self.browser.get(self.server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/',
		))

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		email = 'edith@example.com'

		# arrive at page, shouldn't be logged in
		self.browser.get(self.server_url)
		self.wait_to_be_logged_out(email)

		# create session for user; goes to 404 page
		self.create_pre_authenticated_session(email)

		# go back to home page, now should be logged in
		self.browser.get(self.server_url)
		self.wait_to_be_logged_in(email)