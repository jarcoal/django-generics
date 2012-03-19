from django.views.generic import UpdateView


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