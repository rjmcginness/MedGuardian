from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import PrescriberCreateForm
from .forms import PrescriptionCreateForm


class PrescriberCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = PrescriberCreateForm
    template_name = 'prescriber-create.html'
    success_url = '/prescribers'

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PrescriptionCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = PrescriptionCreateForm
    template_name = 'prescriptions/prescription-create.html'
    success_url = '/medications'

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
