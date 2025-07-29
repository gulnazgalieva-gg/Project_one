from django import forms
from .models import StageMaterial, Material


class StageMaterialForm(forms.ModelForm):
    class Meta:
        model = StageMaterial
        fields = ['stage', 'material', 'planned_quantity', 'actual_quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если экземпляр формы уже существует (это редактирование)
        if self.instance and self.instance.pk:
            if self.instance.material:
                self.fields['material'].queryset = Material.objects.all()
            else:
                self.fields[
                    'material'].queryset = Material.objects.none()  # Если нет материала, очищаем доступные материалы
        else:
            # Если объект не сохранен (создание), то показываем все материалы
            self.fields['material'].queryset = Material.objects.all()
