from django.db import models
from stages.models import Stage  # Импортируем модель Stage
from decimal import Decimal

class Material(models.Model):
    name = models.CharField("Название материала", max_length=100)
    price = models.DecimalField("Цена материала", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
class StageMaterial(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name="Этап")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Материал", null=False, blank=False)
    planned_quantity = models.FloatField("План (кол-во)")
    actual_quantity = models.FloatField("Факт (кол-во)", default=0)
    unit_price = models.DecimalField("Цена за единицу", max_digits=10, decimal_places=2, blank=True, null=True)

    @property
    def total_planned_cost(self):
        return Decimal(self.planned_quantity) * self.unit_price

    @property
    def total_actual_cost(self):
        return Decimal(self.actual_quantity) * self.unit_price

    @property
    def shortage(self):
        # Проверка на дефицит материала
        if self.actual_quantity > self.planned_quantity:
            return self.actual_quantity - self.planned_quantity  # Возвращаем излишек
        return 0  # Если фактическое количество меньше или равно запланированному, недостачи нет

    def save(self, *args, **kwargs):
        # Автозаполнение цены за единицу, если она не была введена
        if not self.unit_price and self.material:
            self.unit_price = self.material.price  # Получаем цену из модели Material
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stage.name} - {self.material.name}"

