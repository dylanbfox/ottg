from selenium import webdriver
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