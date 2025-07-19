from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import AdForm, ExchangeProposalForm, ExchangeProposalUpdateForm
from .models import Ad, ExchangeProposal


class AdListView(ListView):
    """Класс-представление для отображения списка товаров."""

    model = Ad


class AdDetailView(LoginRequiredMixin, DetailView):
    """Класс-представление для отображения информации об одном товаре."""

    model = Ad
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, CreateView):
    """Класс-представление для создания товаров."""

    model = Ad
    form_class = AdForm
    success_url = reverse_lazy("ads:ad-list")

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.user = self.request.user
        ad.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ads:ad-detail", args=[self.object.pk])


class AdUpdateView(LoginRequiredMixin, UpdateView):
    """Класс-представление для изменения товаров."""

    model = Ad
    form_class = AdForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return AdForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("ads:ad-detail", args=[self.kwargs.get("pk")])


class AdDeleteView(LoginRequiredMixin, DeleteView):
    """Класс-представление для удаления товаров."""

    model = Ad
    success_url = reverse_lazy("ads:ad-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этого товара")
        return obj


class ExchangeProposalListView(LoginRequiredMixin, ListView):
    """Класс-представление для отображения списка предложений обмена."""

    model = ExchangeProposal

    def get_queryset(self):
        # Пользователь может видеть все отправленные и полученные предложения обмена
        sent_proposals = ExchangeProposal.objects.filter(ad_sender__user=self.request.user)
        received_proposals = ExchangeProposal.objects.filter(ad_receiver__user=self.request.user)
        return sent_proposals.union(received_proposals)


class ExchangeProposalDetailView(LoginRequiredMixin, DetailView):
    """Класс-представление для отображения информации об одном предложении обмена."""

    model = ExchangeProposal


class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    """Класс-представление для создания предложений обмена."""

    model = ExchangeProposal
    form_class = ExchangeProposalForm

    def get(self, request, *args, **kwargs):
        """Если у пользователя нет товара, то его перенаправит на страницу создания."""
        if not request.user.ads.exists():
            return redirect("ads:ad-create")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("ads:exchange-detail", args=[self.object.pk])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Добавляем пользователя
        return kwargs


class ExchangeProposalUpdateView(LoginRequiredMixin, UpdateView):
    """Класс-представление для изменения предложений обмена."""

    model = ExchangeProposal
    form_class = ExchangeProposalUpdateForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object.ad_sender.user:
            return ExchangeProposalUpdateForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("ads:exchange-detail", args=[self.kwargs.get("pk")])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Добавляем пользователя
        return kwargs


class ExchangeProposalDeleteView(LoginRequiredMixin, DeleteView):
    """Класс-представление для удаления предложений обмена."""

    model = ExchangeProposal
    success_url = reverse_lazy("ads:exchange-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.ad_sender.user != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этого предложения")
        return obj


class AcceptExchangeProposalView(LoginRequiredMixin, UpdateView):
    """Класс-представление для принятия предложения обмена."""

    model = ExchangeProposal
    fields = []

    def form_valid(self, form):
        self.object.status = "accepted"
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("ads:exchange-detail", args=[self.kwargs.get("pk")])


class DeclineExchangeProposalView(LoginRequiredMixin, UpdateView):
    """Класс-представление для отказа от предложения обмена."""

    model = ExchangeProposal
    fields = []

    def form_valid(self, form):
        self.object.status = "declined"
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("ads:exchange-detail", args=[self.kwargs.get("pk")])
