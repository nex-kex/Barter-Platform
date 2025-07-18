from django import forms

from .models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["title", "description", "image_url", "category", "condition"]

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
