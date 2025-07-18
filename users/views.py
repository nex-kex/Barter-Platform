from django.urls import reverse_lazy
from django.views.generic import FormView, View, DetailView, UpdateView
from django.contrib.auth import login
from django.db.utils import IntegrityError

from .models import User
from .forms import UserCreationForm, UserForm


class UserRegisterView(FormView):
    """Класс для регистрации пользователя."""
    form_class = UserCreationForm
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


class LoginView(View):
    """Класс для входа в систему."""
    template_name = "users/login.html"


class LogoutView(View):
    """Класс для выхода из системы."""
    template_name = "users/logged_out.html"
    next_page = reverse_lazy("users:login")


class UserDetailView(DetailView):
    """Класс для получения информации об определённом пользователе."""
    model = User
    template_name = "users/user_detail.html"


class UserUpdateView(UpdateView):
    """Класс для обновления пользователя."""
    model = User
    template_name = "users/user_form.html"
    form_class = UserForm
    # success_url = reverse_lazy("catalog:product_list")
