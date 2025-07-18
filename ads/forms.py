from django import forms

from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["title", "description", "image_url", "category", "condition"]

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ["ad_sender", "ad_receiver", "comment"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ExchangeProposalForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        # Предложить можно только свой товар, а запросить - только чужой
        if user:
            self.fields["ad_sender"].queryset = Ad.objects.filter(user=user)
            self.fields["ad_receiver"].queryset = Ad.objects.filter(user != user)
