from django.shortcuts import render, redirect
from django.db.models import F, Sum, ExpressionWrapper, FloatField, Case, When
from .models import StageMaterial, Stage, Material
from .forms import StageMaterialForm
import json

def materials_view(request):
    materials = StageMaterial.objects.select_related('stage', 'material').filter(material__isnull=False)

    if request.method == 'POST' and request.user.is_staff:
        form = StageMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resources:materials')
    else:
        form = StageMaterialForm()

    # Общая плановая стоимость
    total_required_cost = materials.annotate(
        planned_cost=ExpressionWrapper(F('planned_quantity') * F('unit_price'), output_field=FloatField())
    ).aggregate(total=Sum('planned_cost'))['total'] or 0

    shortage_total = materials.annotate(
        overuse_value=ExpressionWrapper(
            Case(
                When(actual_quantity__gt=F('planned_quantity'),
                     then=(F('actual_quantity') - F('planned_quantity')) * F('unit_price')),
                default=0,
                output_field=FloatField()
            ),
            output_field=FloatField()
        )
    ).aggregate(total=Sum('overuse_value'))['total'] or 0

    # Данные для графика по материалам
    chart_labels = [m.material.name for m in materials]
    chart_planned = [float(m.planned_quantity) for m in materials]
    chart_actual = [float(m.actual_quantity) for m in materials]

    # Данные для графика по этапам
    stages = materials.values('stage__name').annotate(
        planned_sum=Sum('planned_quantity'),
        actual_sum=Sum('actual_quantity')
    ).order_by('stage__name')

    stage_chart_labels = [s['stage__name'] for s in stages]
    stage_chart_planned = [float(s['planned_sum']) for s in stages]
    stage_chart_actual = [float(s['actual_sum']) for s in stages]

    return render(request, 'resources/materials.html', {
        'form': form,
        'materials': materials,
        'total_required_cost': total_required_cost,
        'shortage_total': shortage_total,
        'stages': Stage.objects.all(),
        'materials_list': Material.objects.all(),
        'selected_stage': request.GET.get('stage', ''),
        'selected_material': request.GET.get('material', ''),
        'chart_labels': json.dumps(chart_labels),
        'chart_planned': json.dumps(chart_planned),
        'chart_actual': json.dumps(chart_actual),
        'stage_chart_labels': json.dumps(stage_chart_labels),
        'stage_chart_planned': json.dumps(stage_chart_planned),
        'stage_chart_actual': json.dumps(stage_chart_actual),
    })
