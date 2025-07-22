from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreateForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text="Уникальное имя пользователя, до 150 символов")
    first_name = forms.CharField(max_length=50, required=False, help_text="Имя (необязательно)")
    last_name = forms.CharField(max_length=15, required=False, help_text="Фамилия (необязательно)")
    email = forms.EmailField(required=False, help_text="Email (необязательно)")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
