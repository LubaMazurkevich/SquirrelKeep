from django import forms
from django.forms import inlineformset_factory
from dal import autocomplete

from .models import List, ListItem


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


ItemFormSet = inlineformset_factory(
    List,
    ListItem,
    fields=['text'],
    extra=0,
    can_delete=True,
    widgets={
        'text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пункт списка',
        })
    }
)
