from .base import FunctionalTest

from selenium.webdriver.support.ui import WebDriverWait

class LoginTest(FunctionalTest):

	def switch_to_new_window(self, text_in_title):
		retries = 60
		while retries > 0:
			for handle in self.browser.window_handles:
				self.browser.switch_to_window(handle)
				if text_in_title in self.browser.title:
					return
			retries -= 1
			time.sleep(0.5)
		self.fail('could not find window')

	def wait_for_element_with_id(self, element_id):
		WebDriverWait(self.browser, timeout=30).until(
			lambda b: b.find_element_by_id(element_id)
		)

	def test_login_with_persona(self):
		# Edith clicks the sign in link
		self.browser.get(self.server_url)
		self.browser.find_element_by_id('login').click()

		# A persona login box appears
		self.switch_to_new_window('Mozilla Persona')

		# Edith logs in with her email address
		self.browser.find_element_by_id(
			'authentication_email'
		).send_keys('edith@mockmyid.com')
		self.browser.find_element_by_tag_name('button').click()

		# The persona window closes
		self.switch_to_new_window('To-Do')

		# She can now see that she is logged in
		self.wait_for_element_with_id('logout')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn('edith@mockmyid.com', navbar.text)