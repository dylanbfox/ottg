from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to
		# submit an empty list item. She hits Enter on the emtpy input box

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank

		# She tries again with some text for the itme, which now works.

		# Perversely, she tries to submit a second blank list item

		# She receives a similar warning on the list page

		# And now she can correct it by filling some text in
		self.fail('write me!')	
