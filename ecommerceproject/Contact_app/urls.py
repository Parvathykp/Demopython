from . import views
from django.urls import path

app_name = 'Contact_app'

urlpatterns = [

    path('contact', views.contact, name='contact'),
]
