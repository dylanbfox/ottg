from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# Tests are organized into classes, which inherit 
# from unittest.TestCase 
class NewVisitorTest(LiveServerTestCase):

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
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	# any method whos name starts with test_ is a test
	# method and will be run by the test runner

	# you can have more than one test_ method per class

	# nice descriptive names are a good idea
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)
		# special assert function provided by unittest
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		# There is still an input box inviting user to add another item.
		# User enters "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("Use peacock feathers to make a fly")
		inputbox.send_keys(Keys.ENTER)

		# the page updates again, and now shows both items on her list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# fails no matter what, producing the error message given.
		# using it as a reminder here to finish the tests!
		self.fail('Finish the test!')