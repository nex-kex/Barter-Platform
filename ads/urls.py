from django.urls import path

from ads.apps import AdsConfig

from . import views

app_name = AdsConfig.name

urlpatterns = [
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("", views.AdListView.as_view(), name="ad-list"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("create", views.AdCreateView.as_view(), name="ad-create"),
    path("<int:pk>/update/", views.AdUpdateView.as_view(), name="ad-update"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad-delete"),
]
