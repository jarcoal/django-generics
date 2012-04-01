from django.views.generic.edit import ProcessFormView, BaseCreateView, BaseUpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from generics.mixins import FormsetMixin, InlineFormsetMixin

from django.http import HttpResponseRedirect

class BaseFormsetView(FormsetMixin, ProcessFormView):
	"""
	A base view for displaying a formset.
	"""


class FormsetView(TemplateResponseMixin, BaseFormsetView):
	"""
	A view for displaying a formset, and rendering a template response.
	"""


class BaseInlineFormsetUpdateView(InlineFormsetMixin, BaseUpdateView):
	"""
	A base view for updating a model's related objects.
	"""
	
	def form_valid(self, form):
		self.formset = form.save()
		self.object = self.get_object()
		return HttpResponseRedirect(self.get_success_url())


class InlineFormsetUpdateView(SingleObjectTemplateResponseMixin, BaseInlineFormsetUpdateView):
	"""
	View for updating related instances to a given model.
	"""