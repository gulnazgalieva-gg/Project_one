from django.urls import path
from . import views

urlpatterns = [

    path('', views.times_home, name='times_home'),  # если есть главная

]
