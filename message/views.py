from django.shortcuts import render, redirect
from .models import Feedback
from .forms import FeedbackForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test  # Import the decorator

def is_superuser(user): # or is_staff if is_staff is enough
    return user.is_superuser

@user_passes_test(is_superuser)
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение успешно отправлено!')
            return redirect('feedback')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = FeedbackForm()

    # Only get feedbacks if the user is a superuser.  If not, feedbacks will be None
    if request.user.is_superuser: # or is_staff
        feedbacks = Feedback.objects.all().order_by('-timestamp')
    else:
        feedbacks = None

    return render(request, 'feedback/feedback.html', {'form': form, 'feedbacks': feedbacks})
def message(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            feedback.save()
            messages.success(request, 'Спасибо за ваше сообщение!')

            # Отправка email администратору (необязательно, но полезно)
            subject = f"Новое сообщение с сайта"
            message = f"Имя: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\nСообщение:\n{form.cleaned_data['message']}\n\n"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.ADMIN_EMAIL]
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                messages.error(request, f"Ошибка отправки email: {e}")

            return redirect('message')  # Перезагружаем страницу с сообщениями
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'feedbacks': Feedback.objects.all().order_by('-timestamp') # Получаем все сообщения для отображения
    }
    return render(request, 'message/message.html', context)