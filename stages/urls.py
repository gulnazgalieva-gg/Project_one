from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # только отображение
    path('add/', views.add_stage, name='add_stage'),  # добавление этапа
    path('stages/update/<int:stage_id>/', views.update_stage_status, name='update_stage_status'),
    path('stages/<int:stage_id>/upload/', views.upload_stage_image, name='upload_stage_image'),
    path('rate_stage/<int:stage_id>/', views.rate_stage, name='rate_stage'),
    path('stages/<int:stage_id>/', views.stage_detail, name='stage_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
