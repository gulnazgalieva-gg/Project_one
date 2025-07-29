from django.contrib import admin
from .models import Stage
from .models import StageRating

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'status')

@admin.register(StageRating)
class StageRatingAdmin(admin.ModelAdmin):
     list_display = ('stage', 'user', 'rating', 'comment','created_at')  # Поля, которые будут отображаться в списке

