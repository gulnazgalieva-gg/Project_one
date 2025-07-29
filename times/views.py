from django.shortcuts import render, redirect
from .models import Task, Photo
from .forms import TaskForm, PhotoUploadForm
import plotly.offline as pyo
import plotly.figure_factory as ff
from django.utils import timezone
from datetime import datetime


def create_gantt_chart(task):
    planned_start = timezone.make_aware(datetime.combine(task.planned_start_date, datetime.min.time()))
    planned_end = timezone.make_aware(datetime.combine(task.planned_end_date, datetime.min.time()))

    data = [
        dict(Task="План", Start=planned_start, Finish=planned_end, Resource="План")
    ]

    if task.actual_start_date:
        actual_start = timezone.make_aware(datetime.combine(task.actual_start_date, datetime.min.time()))

        if task.actual_end_date:
            actual_end = timezone.make_aware(datetime.combine(task.actual_end_date, datetime.min.time()))
        else:
            actual_end = timezone.now()  # Текущая дата, если строительство ещё идёт

        data.append(dict(Task="Факт", Start=actual_start, Finish=actual_end, Resource="Факт"))

    fig = ff.create_gantt(
        data,
        index_col="Resource",  # <--- вот это важно
        colors={"План": "#ADD8E6", "Факт": "#FFA07A"},
        show_colorbar=True,
        bar_width=0.4,
        showgrid_x=True,
        showgrid_y=True
    )

    fig.update_layout(
        title="График выполнения строительства",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 мес", step="month", stepmode="backward"),
                    dict(count=6, label="6 мес", step="month", stepmode="backward"),
                    dict(label="Все", step="all")
                ])
            ),
            type="date"
        ),
        width=850,
        height=400
    )

    return pyo.plot(fig, output_type="div", config={"displayModeBar": False})

def times_home(request):
    tasks = Task.objects.all()
    photos = Photo.objects.all()
    task_form = TaskForm()
    photo_form = PhotoUploadForm()
    if request.method == 'POST':
        if request.user.is_superuser and 'planned_start_date' in request.POST:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task_form.save()
                return redirect('times_home')
        if 'image' in request.FILES:
            photo_form = PhotoUploadForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo_form.save()
                return redirect('times_home')


    if tasks.exists():
        task = tasks.first()
        gantt_chart_html = create_gantt_chart(task)
    else:
        gantt_chart_html = "<p>Нет задач для отображения диаграммы Ганта.</p>"

    return render(request, 'times/times_home.html', {
        'tasks': tasks,
        'form': task_form,
        'form_photo': photo_form,
        'photos': photos,
        'gantt_chart_html': gantt_chart_html,
    })
