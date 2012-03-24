from django.views.generic import UpdateView, FormView
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory


class UpsertView(UpdateView):
	"""
	UpsertView allows you to handle an insert or update of a given model in the same view.
	This is useful for forms that use the same template for updating or creating a model object.
	"""

	def post(self, *a, **k):
		"""
		If a POST variable "delete" is submitted, the model object will be deleted.
		If you have a delete button in your form somewhere, just give it `name="delete"`.
		"""
	
		#Not marked for deletion
		if 'delete' not in self.request.POST:
			return super(UpsertView, self).post(*a, **k)
		
		#Delete the object
		self.object = self.get_object()
		self.object.delete()
		
		#Redirect to Delete URL
		return HttpResponseRedirect(self.get_delete_url())

	
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


	def get_formset_class(self, form_class):
		"""
		Converts a form class into a formset.
		"""
		return formset_factory(form_class, **self.get_formset_kwargs())


	def get_form(self, form_class):
		"""
		Returns a formset.
		"""
		
		#convert the form into a formset class
		formset_class = self.get_formset_class(form_class)
		
		#instatiate the formset with form parameters
		return formset_class(**self.get_form_kwargs())
		


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



class InlineFormsetView(FormsetView):
	"""
	Handles a view that needs to operate on an inline formset.
	"""

	parent_model = None
	model = None
	
	fields = None
	exclude = None
	fk_name = None


	def get(self, *a, **k):
		"""
		Creates a formset and adds it to the context to be rendered.
		"""
		formset_class = self.get_formset_class()
		form = self.get_form(formset_class)
		return self.render_to_response(self.get_context_data(form=form))


	def post(self, *a, **k):
		"""
		Validates a formset, and calls the appropriate handler.
		"""
		formset_class = self.get_formset_class()
		form = self.get_form(formset_class)
		return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

	
	def get_formset_class(self):
		"""
		Returns an inline formset.
		"""
		return inlineformset_factory(self.parent_model, self.model, **self.get_formset_kwargs())


	def get_form(self, form_class):
		return form_class(**self.get_form_kwargs())


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
	
	
	def get_form_kwargs(self, *a, **k):
		"""
		Injects the instance variable into the form kwargs
		"""
		kwargs = super(InlineFormsetView, self).get_form_kwargs(*a, **k)
		kwargs['instance'] = self.get_object()
		return kwargs