from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Ваш Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Сообщение", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.isalpha():
            raise forms.ValidationError("Имя должно содержать только буквы.")
        return name