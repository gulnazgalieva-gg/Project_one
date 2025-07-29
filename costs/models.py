from django.db import models
class Budget(models.Model):
    planned_cost = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def deviation_amount(self):
        return self.actual_cost - self.planned_cost

    def deviation_percentage(self):
        if self.planned_cost == 0:
            return 0
        return (self.deviation_amount() / self.planned_cost) * 100

    def __str__(self):
        return f"Planned: {self.planned_cost}, Actual: {self.actual_cost}"