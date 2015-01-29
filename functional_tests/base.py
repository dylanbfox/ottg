from selenium.webdriver.support.ui import WebDriverWait

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys

class FunctionalTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super(FunctionalTest, cls).setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super(FunctionalTest, cls).tearDownClass()

	# special method; gets called before each test
	def setUp(self):
		self.browser = webdriver.Firefox()
		# browser will wait 3 seconds before trying anything
		# to help guarantee everything has loaded before
		# continuing to test
		self.browser.implicitly_wait(3)

	# special method; gets called after each test
	# even if there is an error in the test
	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	def wait_for_element_with_id(self, element_id):
		WebDriverWait(self.browser, timeout=30).until(
			lambda b: b.find_element_by_id(element_id),
			'Could not find element with id {}. Page text was {}'.format(
				element_id, self.browser.find_element_by_tag_name('body').text
			)
		)

	def wait_to_be_logged_in(self, email):
		self.wait_for_element_with_id('id_logout')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	def wait_to_be_logged_out(self, email):
		self.wait_for_element_with_id('id_login')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)