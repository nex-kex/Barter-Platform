from django.views.generic import TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)

from .forms import AdForm
from .models import Ad, ExchangeProposal

class ContactsView(TemplateView):
    template_name = "ads/contacts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class AdListView(ListView):
    model = Ad


class AdDetailView(LoginRequiredMixin, DetailView):
    model = Ad


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy("ads:ad-list")

    def form_valid(self, form):
        ad = form.save()
        user = self.request.user
        ad.user = user
        ad.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ads:ad-detail", args=[self.object.pk])


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy("ads:ad-list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return AdForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("ads:ad-detail", args=[self.kwargs.get("pk")])


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy("ads:ad-list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return AdForm
        raise PermissionDenied
