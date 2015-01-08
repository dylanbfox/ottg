from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# Tests are organized into classes, which inherit 
# from unittest.TestCase 
class NewVisitorTest(unittest.TestCase):

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

	# any method whos name starts with test_ is a test
	# method and will be run by the test runner

	# you can have more than one test_ method per class

	# nice descriptive names are a good idea
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')
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

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy peacock feathers' for row in rows)
		)

		# fails no matter what, producing the error message given.
		# using it as a reminder here to finish the tests!
		self.fail('Finish the test!')

# This is how a Python script checks if it's been
# executed from the command line, rather than just imported
# by another script
if __name__ == '__main__':
	# launches the unittest test runner, which will
	# automatically find test classes and methods in the file
	# and run them
	unittest.main()