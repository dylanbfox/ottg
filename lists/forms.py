from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item

EMPTY_LIST_ERROR = "You can't have an empty list item"

class ItemForm(forms.models.ModelForm):

	def save(self, for_list):
		self.instance.list = for_list
		return super(ItemForm, self).save()

	class Meta:
		model = Item
		fields = ('text',)
		widgets = {
			'text': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a to-do item',
				'class': 'form-control input-lg',
			}),
		}
		error_messages = {
			'text': {'required': EMPTY_LIST_ERROR},
		}

class ExistingListItemForm(ItemForm):

	def __init__(self, for_list, *args, **kwargs):
		super(ExistingListItemForm, self).__init__(*args, **kwargs)
		self.instance.list = for_list

	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_TEXT]}
			self._update_errors(e)
