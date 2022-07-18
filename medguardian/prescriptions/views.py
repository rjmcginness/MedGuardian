from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import PrescriptionCreateForm


class PrescriptionCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = PrescriptionCreateForm
    template_name = 'prescriptions/prescription-create.html'
    success_url = '/medications'

    def test_func(self) -> bool:
        return self.user.id == self.kwargs['pk']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
