from django import forms
from .models import Stage
from .models import StageRating,StagePhoto

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StageImageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['image']

class StageRatingForm(forms.ModelForm):
    class Meta:
        model = StageRating
        fields = ['rating', 'comment']

from django import forms

