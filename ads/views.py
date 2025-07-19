from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AdForm, ExchangeProposalForm, ExchangeProposalUpdateForm
from .models import Ad, ExchangeProposal


class AdSearchView(ListView):
    model = Ad
    template_name = "ads/search_results.html"
    paginate_by = 15
    context_object_name = "ads"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search")
        category = self.request.GET.get("category")
        condition = self.request.GET.get("condition")

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        if category:
            queryset = queryset.filter(category__iexact=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["unique_categories"] = Ad.objects.order_by().values_list("category", flat=True).distinct()
        context["condition_choices"] = Ad.CONDITION_CHOICES

        return context


class AdListView(ListView):
    """Класс-представление для отображения списка всех товаров."""

    model = Ad
    paginate_by = 15


class NotUserAdListView(LoginRequiredMixin, ListView):
    """Класс-представление для отображения списка товаров, не опубликованных пользователем."""

    model = Ad
    paginate_by = 15

    def get_queryset(self):
        return Ad.objects.exclude(user=self.request.user)


class UserAdListView(LoginRequiredMixin, ListView):
    """Класс-представление для отображения списка товаров, опубликованных пользователем."""

    model = Ad
    paginate_by = 15

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)


class AdDetailView(LoginRequiredMixin, DetailView):
    """Класс-представление для отображения информации об одном товаре."""

    model = Ad
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, CreateView):
    """Класс-представление для создания товаров."""

    model = Ad
    form_class = AdForm

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
    success_url = reverse_lazy("ads:user-ad-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этого товара")
        return obj


class SentExchangeProposalListView(LoginRequiredMixin, ListView):
    """Класс-представление для отображения списка отправленных предложений обмена."""

    model = ExchangeProposal
    ordering = ["-status"]
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(ad_sender__user=self.request.user)


class ReceivedExchangeProposalListView(LoginRequiredMixin, ListView):
    """Класс-представление для отображения списка полученных предложений обмена."""

    model = ExchangeProposal
    ordering = ["-status"]
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(ad_receiver__user=self.request.user)


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
