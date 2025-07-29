from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.shortcuts import render, redirect

User = get_user_model()


class CustomUserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")  # Добавьте password1 и password2


def base(request):
    return render(request, 'users/base.html')


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('base')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)