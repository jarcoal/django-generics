from django.views.generic.edit import ProcessFormView, BaseCreateView, BaseUpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from generics.mixins import FormsetMixin, InlineFormsetMixin


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


class InlineFormsetUpdateView(SingleObjectTemplateResponseMixin, BaseInlineFormsetUpdateView):
	"""
	View for updating related instances to a given model.
	"""