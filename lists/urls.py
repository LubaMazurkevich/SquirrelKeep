from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view, name='list_index'),
    path('list/<int:list_id>/', views.list_view, name='list_detail'),
    path('item/<int:item_id>/toggle/', views.toggle_item, name='toggle_item'),
    path('list/<int:list_id>/toggle_all/', views.toggle_all, name='toggle_all'),
]
