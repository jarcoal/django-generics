from django.views.generic.edit import FormMixin
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory


class FormsetMixin(FormMixin):
	"""
	Provides functionality to operate on a formset.
	"""

	extra = 3
	can_order = False
	can_delete = False
	max_num = None
	
	initial = []

	def get_initial(self):
		"""
		Returns the initial data to input into the formset.
		"""
		return self.initial


	def get_form_class(self):
		"""
		Converts a form class into a formset class.
		"""
		return formset_factory(super(FormsetMixin, self).get_form_class(), **self.get_formset_kwargs())


	def get_formset_kwargs(self):
		"""
		Returns the kwargs used to create the formset class.
		"""
		return {
			'extra': self.extra,
			'can_order': self.can_order,
			'can_delete': self.can_delete,
			'max_num': self.max_num,		
		}


class InlineFormsetMixin(FormsetMixin):
	"""
	Handles a view that needs to operate on an inline formset.
	"""

	related_model = None
	
	fields = None
	exclude = None
	fk_name = None


	def get_model(self):
		"""
		Returns the Parent Model
		"""
		return self.object.__class__


	def get_related_model(self):
		"""
		Returns the model that is related (child) of the Parent
		"""
		return self.related_model

	
	def get_form_class(self):
		"""
		Returns an inline formset.
		"""
		return inlineformset_factory(self.get_model(), self.get_related_model(), **self.get_formset_kwargs())


	def get_formset_kwargs(self):
		"""
		Returns the kwargs used to instatiate the formset.
		"""
		kwargs = super(InlineFormsetMixin, self).get_formset_kwargs()
		
		kwargs.update({
			'fields': self.fields,
			'exclude': self.exclude,
			'fk_name': self.fk_name,
		})
		
		return kwargs
	
	def get_form_kwargs(self):
		kwargs = super(InlineFormsetMixin, self).get_form_kwargs()
		del kwargs['initial']		
		return kwargs
