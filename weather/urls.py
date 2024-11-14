from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('about', views.about, name='about'),
    # path('add_city', views.add_city, name='add_city'),
    # path('delete_city/<city_name>', views.delete_city, name='delete_city'),
]