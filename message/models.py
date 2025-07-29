from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Дата и время")

    def __str__(self):
        return f"Сообщение от {self.name}"

    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
        ordering = ['-timestamp']