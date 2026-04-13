from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view, name='list_index'),
    path(
        'category-autocomplete/',
        views.CategoryAutocomplete.as_view(create_field='name', validate_create=True),
        name='category-autocomplete',
    ),
    path(
        'tag-autocomplete/',
        views.TagAutocomplete.as_view(create_field='name', validate_create=True),
        name='tag-autocomplete',
    ),
    path('list/<int:list_id>/', views.list_detail_view, name='list_detail'),
    path('list/<int:list_id>/edit/', views.edit_list, name='edit_list'),
    path('item/<int:item_id>/toggle/', views.toggle_item, name='toggle_item'),
    path('list/<int:list_id>/toggle_all/', views.toggle_all, name='toggle_all'),
]
