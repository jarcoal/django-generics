from django.views.generic import UpdateView, FormView
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.views.generic.detail import SingleObjectMixin


class UpsertView(UpdateView):
	"""
	UpsertView allows you to handle an insert or update of a given model in the same view.
	This is useful for forms that use the same template for updating or creating a model object.
	"""

	def get_object(self):
		"""
		Attempts to get a model object.  If one is found, we are updating an existing model object, otherwise, we are creating one.
		"""
	
		try:
			return super(UpsertView, self).get_object(queryset=self.get_queryset())
		except AttributeError:
			return None
	
	
	def get_context_data(self, **k):
		"""
		Injects an 'is_update' variable into the context scope.  This will be true if the request intends to update a model object.
		"""
	
		#Parent
		context = super(UpsertView, self).get_context_data(**k)
	
		#Add our update variable
		context['is_update'] = True if self.object else False
	
		#Gone
		return context
	
	
	def form_valid(self, form):
		"""
		Calls the appropriate form_valid method, if it exists.
		If one of those methods returns a response, use it, else generate a redirect.
		"""
	
		self.is_update = True if self.object else False
	
		#Call the appropriate handler.
		try:
			response = self.form_valid_update(form) if self.object else self.form_valid_insert(form)
		except:
			pass
		
		#Return the response
		return response if response else HttpResponseRedirect(self.get_success_url())
		
			

class FormsetView(FormView):
	"""
	Handles a view that needs to operate on a formset.
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
		form_class = super(FormsetView, self).get_form_class()
		return formset_factory(form_class, **self.get_formset_kwargs())


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



class InlineFormsetView(SingleObjectMixin, FormsetView):
	"""
	Handles a view that needs to operate on an inline formset.
	"""

	related_model = None
	
	fields = None
	exclude = None
	fk_name = None


	def get(self, *a, **k):
		self.object = self.get_object()
		return super(InlineFormsetView, self).get(*a, **k)
	
	
	def post(self, *a, **k):
		self.object = self.get_object()
		return super(InlineFormsetView, self).post(*a, **k)

	
	def form_valid(self, form):
		self.object = form.save()
		return super(InlineFormsetView, self).form_valid(form)


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
		kwargs = super(InlineFormsetView, self).get_formset_kwargs()
		
		kwargs.update({
			'fields': self.fields,
			'exclude': self.exclude,
			'fk_name': self.fk_name,
		})
		
		return kwargs
	
	
	def get_form_kwargs(self):
		"""
		Injects the instance variable into the form kwargs
		"""
		kwargs = super(InlineFormsetView, self).get_form_kwargs()
		kwargs['instance'] = self.object
		return kwargs