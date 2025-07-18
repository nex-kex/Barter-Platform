from django.contrib.auth import login
from django.db.utils import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from .forms import UserCreateForm


class UserRegisterView(FormView):
    """Класс для регистрации пользователя."""

    form_class = UserCreateForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:logout")

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            return super().form_valid(form)

        except IntegrityError:
            form.add_error("username", "Пользователь с таким username уже существует")
            return self.form_invalid(form)
