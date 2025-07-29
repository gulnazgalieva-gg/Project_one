import plotly.figure_factory as ff
from django.utils import timezone
from datetime import datetime
import plotly.graph_objs as go
from .models import StageRating
from django.contrib.auth.decorators import login_required
from .forms import StageImageForm
from resources.models import StageMaterial
from message.models import Feedback
from times.models import Task
@login_required
def rate_stage(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)

    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        if not rating_value:
            messages.error(request, 'Пожалуйста, выберите оценку перед отправкой!')
            return redirect('stage_detail', stage_id=stage.id)

        try:
            rating_value = int(rating_value)
        except ValueError:
            messages.error(request, 'Оценка должна быть числом от 1 до 5.')
            return redirect('stage_detail', stage_id=stage.id)

        # Только теперь создаём StageRating
        rating, created = StageRating.objects.get_or_create(
            stage=stage,
            user=request.user,
            defaults={'rating': rating_value, 'comment': comment}
        )

        # Если объект уже был (не создан), обновляем
        if not created:
            rating.rating = rating_value
            rating.comment = comment
            rating.save()

        messages.success(request, 'Ваша оценка успешно сохранена!')
        return redirect('index')
    return redirect('index')
def stage_detail(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    return render(request, 'stages/index.html', {'stage': stage})
def create_status_bar_chart(status_counts):
    statuses = list(status_counts.keys())
    counts = list(status_counts.values())
    fig = go.Figure(data=[go.Bar(x=statuses, y=counts)])

    fig.update_layout(
        xaxis_title='Статус',
        yaxis_title='Количество этапов',
        width=450,
        height=450,

    )


    fig.add_annotation(
        text='Количество этапов по статусам',
        xref='paper', yref='paper',
        x=0.5, y=1.2,
        showarrow=False,
        bgcolor='#f0f0f0',
        borderwidth=1,
        font=dict(size=16)
    )

    return fig.to_html(full_html=False)

def stage_view(request):
    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES)  # Обработка файлов
        if form.is_valid():
            form.save()
            return redirect('index')  # Укажите URL для перенаправления после успешной загрузки
    else:
        form = StageForm()

    stages = Stage.objects.all()  # Получение всех этапов для отображения
    return render(request, 'stages/index.html', {'form': form, 'stages': stages})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Stage
from .forms import StageForm
from django.contrib import messages

def create_stage_rating_chart():
    from django.db.models import Avg

    stages = Stage.objects.all()
    stage_ratings = []

    for stage in stages:
        ratings = stage.ratings.all()
        avg_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        stage_ratings.append({
            'stage_name': stage.name,
            'avg_rating': round(avg_rating, 2)
        })

    # Создание столбчатой диаграммы с Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=[stage['stage_name'] for stage in stage_ratings],
            y=[stage['avg_rating'] for stage in stage_ratings],
            marker_color='rgba(255, 165, 0, 0.7)'
        )
    ])

    fig.update_layout(
        xaxis_title='Этап',
        yaxis_title='Средний рейтинг',
        yaxis=dict(range=[0, 5]),  # Оценки от 0 до 5
        width=900,
        height=450,
        title='Средний рейтинг этапов строительства'
    )

    return fig.to_html(full_html=False)

def upload_stage_image(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)

    if request.method == 'POST':
        form = StageImageForm(request.POST, request.FILES, instance=stage)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StageImageForm(instance=stage)

    return render(request, 'stages/upload_image.html', {
        'stage': stage,
        'form': form,
    })
def update_stage_status(request, stage_id):
    if request.method == 'POST':
        stage = get_object_or_404(Stage, id=stage_id)
        new_status = request.POST.get('status')
        if new_status in ['not_started', 'in_progress', 'completed']:
            stage.status = new_status
            stage.save()
    return redirect('index')
def create_gantt_chart(stages):
    data = []

    for stage in stages:
        planned_start_date = timezone.make_aware(datetime.combine(stage.start_date, datetime.min.time()))
        planned_end_date = timezone.make_aware(datetime.combine(stage.end_date, datetime.min.time()))

        data.append(dict(Task=stage.name, Start=planned_start_date, Finish=planned_end_date,
                         Resource=stage.get_status_display()))

    num_stages = len(stages)
    colors = [f'rgba({i * 255 // num_stages}, {100 + (i * 100) // num_stages}, {150}, 0.6)' for i in range(num_stages)]

    fig = ff.create_gantt(data, colors=colors,
                          show_colorbar=True, bar_width=0.2, showgrid_x=True, showgrid_y=True,
                          title='')

    fig.update_layout(yaxis=dict(autorange="reversed"))

    fig.update_traces(
        text=[stage['Task'] for stage in data],
        textposition='middle center',  # Положение текста
        textfont=dict(color='black', size=12, family='Arial', weight='bold')  # Жирный шрифт
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 месяц", step="month", stepmode="backward"),
                    dict(count=6, label="6 месяцев", step="month", stepmode="backward"),
                    dict(label="Все", step="all")
                ])
            ),
            type='date'
        ),
        width=900,
        height=450
    )

    return fig.to_html(full_html=False)


def calculate_average_durations(stages):
    status_durations = {}

    for stage in stages:
        if stage.end_date and stage.start_date:
            duration = (stage.end_date - stage.start_date).days
            status = stage.status

            if status not in status_durations:
                status_durations[status] = []
            status_durations[status].append(duration)

    average_durations = {status: sum(durations) / len(durations) for status, durations in status_durations.items() if
                         durations}

    return average_durations

def index(request):
    status_filter = request.GET.get('status')
    stages = Stage.objects.all()

    if status_filter:
        stages = stages.filter(status=status_filter)

    no_deferred_stages = not stages.filter(status='deferred').exists()

    gantt_chart_html = create_gantt_chart(stages) if stages.exists() else "<p>Нет данных для отображения.</p>"

    status_counts = {
        'Не начато': stages.filter(status='not_started').count(),
        'В процессе': stages.filter(status='in_progress').count(),
        'Завершено': stages.filter(status='completed').count(),
    }

    status_bar_chart_html = create_status_bar_chart(status_counts)
    stage_rating_chart_html = create_stage_rating_chart()

    materials = StageMaterial.objects.filter(stage__in=stages)
    feedbacks = Feedback.objects.all()
    tasks = Task.objects.all()
    return render(request, 'stages/index.html', {
        'stages': stages,
        'gantt_chart_html': gantt_chart_html,
        'no_deferred_stages': no_deferred_stages,
        'status_counts': status_counts,
        'status_bar_chart_html': status_bar_chart_html,
        'stage_rating_chart_html': stage_rating_chart_html,
        'materials': materials,  # ✔ правильно передаём материалы
        'feedbacks': feedbacks,
        'tasks': tasks,
    })


def add_stage(request):
    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StageForm()

    return render(request, 'stages/add_stage.html', {'form': form})

