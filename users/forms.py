from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False, help_text="Имя (необязательно)")
    last_name = forms.CharField(max_length=15, required=False, help_text="Фамилия (необязательно)")
    email = forms.EmailField(required=False, help_text="Email (необязательно)")
    usable_password = None

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
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