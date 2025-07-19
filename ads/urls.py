from django.urls import path

from ads.apps import AdsConfig

from . import views

app_name = AdsConfig.name

urlpatterns = [
    # CRUD для товаров
    path("", views.AdListView.as_view(), name="ad-list"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("create", views.AdCreateView.as_view(), name="ad-create"),
    path("<int:pk>/update/", views.AdUpdateView.as_view(), name="ad-update"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad-delete"),
    # CRUD для предложений обмена
    path("exchange/", views.ExchangeProposalListView.as_view(), name="exchange-list"),
    path("exchange/<int:pk>/", views.ExchangeProposalDetailView.as_view(), name="exchange-detail"),
    path("exchange/create", views.ExchangeProposalCreateView.as_view(), name="exchange-create"),
    path("exchange/<int:pk>/update/", views.ExchangeProposalUpdateView.as_view(), name="exchange-update"),
    path("exchange/<int:pk>/delete/", views.ExchangeProposalDeleteView.as_view(), name="exchange-delete"),
    # Смена статуса предложения обмена
    path("exchange/<int:pk>/accept/", views.AcceptExchangeProposalView.as_view(), name="exchange-accept"),
    path("exchange/<int:pk>/decline/", views.DeclineExchangeProposalView.as_view(), name="exchange-decline"),
]
