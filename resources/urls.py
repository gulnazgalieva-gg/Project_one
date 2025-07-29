from django.urls import path
from .views import materials_view

app_name = 'resources'

urlpatterns = [
    path('', materials_view, name='materials'),
]
