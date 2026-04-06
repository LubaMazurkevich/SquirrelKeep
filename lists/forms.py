from django import forms
from dal import autocomplete

from .models import List


class ListCreateForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ("title", "category")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": autocomplete.ModelSelect2(
                url="category-autocomplete",
                attrs={
                    "data-placeholder": "Выберите или создайте категорию",
                    "data-minimum-input-length": 0,
                },
            ),
        }
