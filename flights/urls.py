from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:flight_id>', views.flight, name='flight'),
    path('login/', views.login_in, name='login'),
    path('logout/', views.login_out, name='logout')
]