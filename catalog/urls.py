from django.urls import path
from catalog import views

# this is where patterns are added specific to this application 'catalog'
# this is accessed by the include in locallibrary/locallibrary/urls.py

urlpatterns = [
    path('', views.index, name='index'),
]