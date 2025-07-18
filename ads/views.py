from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import AdForm, ExchangeProposalForm
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
        return ExchangeProposal.objects.filter(ad_sender__user=self.request.user) + ExchangeProposal.objects.filter(
            ad_receiver__user=self.request.user
        )


class ExchangeProposalDetailView(LoginRequiredMixin, DetailView):
    """Класс-представление для отображения информации об одном предложении обмена."""

    model = ExchangeProposal


class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    """Класс-представление для создания предложений обмена."""

    model = ExchangeProposal
    form_class = ExchangeProposalForm

    def get_success_url(self):
        return reverse_lazy("ads:exchange-detail", args=[self.object.pk])


class ExchangeProposalUpdateView(LoginRequiredMixin, UpdateView):
    """Класс-представление для изменения предложений обмена."""

    model = ExchangeProposal
    form_class = ExchangeProposalForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object["ad_sender"]["user"]:
            return ExchangeProposalForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("ads:exchange-detail", args=[self.kwargs.get("pk")])


class ExchangeProposalDeleteView(LoginRequiredMixin, DeleteView):
    """Класс-представление для удаления предложений обмена."""

    model = ExchangeProposal
    success_url = reverse_lazy("exchange:ad-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj["ad_sender"]["user"] != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этого предложения")
        return obj


class AcceptExchangeProposalView(LoginRequiredMixin, UpdateView):
    """Класс-представление для принятия предложения обмена."""

    model = ExchangeProposal
    form_class = ExchangeProposalForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object["ad_receiver"]["user"]:
            return ExchangeProposalForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("ads:exchange-detail", args=[self.kwargs.get("pk")])

    def post(self, request, *args, **kwargs):
        self.object["status"] = "accepted"
        self.object.save()
        return super().post(request, *args, **kwargs)


class DeclineExchangeProposalView(LoginRequiredMixin, UpdateView):
    """Класс-представление для отказа от предложения обмена."""

    model = ExchangeProposal
    form_class = ExchangeProposalForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object["ad_receiver"]["user"]:
            return ExchangeProposalForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("ads:exchange-detail", args=[self.kwargs.get("pk")])

    def post(self, request, *args, **kwargs):
        self.object["status"] = "declined"
        self.object.save()
        return super().post(request, *args, **kwargs)
