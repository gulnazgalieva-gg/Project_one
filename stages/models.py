from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Stage(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='stage_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

class StageRating(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('stage', 'user')

    def __str__(self):
        return f'{self.user.username} оценил {self.stage.name}'

class StagePhoto(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='stage_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)