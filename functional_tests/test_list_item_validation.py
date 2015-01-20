from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to
		# submit an empty list item. She hits Enter on the emtpy input box
		self.browser.get(self.server_url) # go to the site
		self.get_item_input_box().send_keys('\n') # find the input box and hit enter

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't have an empty list item")

		# She tries again with some text for the itme, which now works.
		self.get_item_input_box().send_keys('Buy milk\n')
		self.check_for_row_in_list_table('1: Buy milk')

		# Perversely, she tries to submit a second blank list item
		self.get_item_input_box().send_keys('\n')

		# She receives a similar warning on the list page
		self.check_for_row_in_list_table('1: Buy milk')		
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't have an empty list item")		

		# And now she can correct it by filling some text in
		self.get_item_input_box().send_keys('Make tea\n')
		self.check_for_row_in_list_table('1: Buy milk')
		self.check_for_row_in_list_table('2: Make tea')
