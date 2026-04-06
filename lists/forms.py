from django import forms
from dal import autocomplete

from .models import List


class ListCreateForm(forms.ModelForm):
    # Select widgets with autocomplete for category and tags
    class Meta:
        model = List
        fields = ("title", "category", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": autocomplete.ModelSelect2(
                url="category-autocomplete",
                attrs={
                    "data-placeholder": "Выберите или создайте категорию",
                    "data-minimum-input-length": 0,
                },
            ),
            "tags": autocomplete.ModelSelect2Multiple(
                url="tag-autocomplete",
                attrs={
                    "data-placeholder": "Выберите или создайте теги",
                    "data-minimum-input-length": 0,
                },
            ),
        }
