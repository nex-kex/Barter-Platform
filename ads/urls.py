from django.urls import path

from ads.apps import AdsConfig

from . import views

app_name = AdsConfig.name

urlpatterns = [
    # Список товаров пользователя/не пользователя
    path("not_my/", views.NotUserAdListView.as_view(), name="not-user-ad-list"),
    path("my/", views.UserAdListView.as_view(), name="user-ad-list"),
    # CRUD для товаров
    path("", views.AdListView.as_view(), name="ad-list"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("create", views.AdCreateView.as_view(), name="ad-create"),
    path("<int:pk>/update/", views.AdUpdateView.as_view(), name="ad-update"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad-delete"),
    # CRUD для предложений обмена
    path("exchange/sent/", views.SentExchangeProposalListView.as_view(), name="sent-exchange-list"),
    path("exchange/received/", views.ReceivedExchangeProposalListView.as_view(), name="received-exchange-list"),
    path("exchange/<int:pk>/", views.ExchangeProposalDetailView.as_view(), name="exchange-detail"),
    path("exchange/create", views.ExchangeProposalCreateView.as_view(), name="exchange-create"),
    path("exchange/<int:pk>/update/", views.ExchangeProposalUpdateView.as_view(), name="exchange-update"),
    path("exchange/<int:pk>/delete/", views.ExchangeProposalDeleteView.as_view(), name="exchange-delete"),
    # Смена статуса предложения обмена
    path("exchange/<int:pk>/accept/", views.AcceptExchangeProposalView.as_view(), name="exchange-accept"),
    path("exchange/<int:pk>/decline/", views.DeclineExchangeProposalView.as_view(), name="exchange-decline"),
]
