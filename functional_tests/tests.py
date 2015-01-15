from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# Tests are organized into classes, which inherit 
# from unittest.TestCase 
class NewVisitorTest(StaticLiveServerTestCase):

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

	def test_layout_and_styling(self):
		# Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# She notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=15,
		)

		# she starts a new list and sees the input is nicely centered
		# there too
		inputbox.send_keys('testing\n') # \n == ENTER; submits POST
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=15,
		)

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

		# when she hits enter, she is taken to a new URL
		# and now the page lists "1: Buy peacock feathers" as an item in a
		# to- do list table
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegexpMatches(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		# There is still an input box inviting user to add another item.
		# User enters "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("Use peacock feathers to make a fly")
		inputbox.send_keys(Keys.ENTER)

		# the page updates again, and now shows both items on her list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# Now a new user, Francis, comes along to the site

		## we use a new browser session to make sure that no information
		## of Edith's is coming through from cookies, etc.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visit the home page. There is no sign of Edith's list
		self.browser.get(self.live_server_url) # go to server URL (now that we're using LiveServerTestCase)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text) 

		# Francis starts a new list by entering a new item. He is less
		# interesting than Edith...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegexpMatches(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# fails no matter what, producing the error message given.
		# using it as a reminder here to finish the tests!
		self.fail('Finish the test!')