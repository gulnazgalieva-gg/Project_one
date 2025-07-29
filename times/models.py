from django.db import models
from datetime import date

class Task(models.Model):
    planned_start_date = models.DateField('Запланированное начало работ')
    actual_start_date = models.DateField('Фактическое начало работ', null=True, blank=True)
    planned_end_date = models.DateField('Запланированный конец работ')
    actual_end_date = models.DateField('Фактический конец работ', null=True, blank=True)

    def start_deviation(self):
        if self.actual_start_date and self.planned_start_date:
            return (self.actual_start_date - self.planned_start_date).days
        return None

    def end_deviation(self):
        if self.actual_end_date and self.planned_end_date:
            return (self.actual_end_date - self.planned_end_date).days
        return None

    def completion_percentage(self):
        """Возвращает процент отклонения от запланированных сроков."""
        if self.planned_start_date and self.planned_end_date:
            total_days = (self.planned_end_date - self.planned_start_date).days
            if total_days > 0:
                if self.actual_end_date:
                    # Если задача завершена, считаем разницу между фактической датой окончания и запланированной
                    completed_days = (self.actual_end_date - self.planned_start_date).days
                    deviation = (completed_days - total_days) / total_days * 100
                    return min(max(deviation, -100), 100)  # Ограничиваем до -100% и 100%
                else:
                    # Если задача еще не завершена, можно рассчитать отклонение на основе текущей даты
                    today = date.today()
                    if today < self.planned_start_date:
                        return -100  # Если сегодня раньше запланированной даты начала
                    elif today > self.planned_end_date:
                        return 100  # Если сегодня позже запланированной даты окончания
                    else:
                        elapsed_days = (today - self.planned_start_date).days
                        deviation = (elapsed_days - total_days) / total_days * 100
                        return min(max(deviation, -100), 100)
        return None

    def execution_percentage(self):
        """Возвращает процент выполнения задачи на основе фактической даты окончания."""
        if self.planned_end_date and self.planned_start_date:
            total_days = (self.planned_end_date - self.planned_start_date).days
            if total_days > 0:
                if self.actual_end_date:
                    completed_days = (self.actual_end_date - self.planned_start_date).days
                    return min((completed_days / total_days) * 100, 100)  # Ограничиваем до 100%
                elif self.actual_start_date:  # Если работа начата, но не завершена
                    ongoing_days = (date.today() - self.planned_start_date).days
                    return min((ongoing_days / total_days) * 100, 100)
                else:
                    return 0
        return None

    def __str__(self):
        return f"Task from {self.planned_start_date} to {self.planned_end_date}"

    class Meta:
        verbose_name = 'Срок'
        verbose_name_plural = 'Сроки'


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo {self.id}'