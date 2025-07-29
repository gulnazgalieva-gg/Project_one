from django.shortcuts import render, redirect
from .models import Budget
from .forms import BudgetForm

def budget_view(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    else:
        form = BudgetForm()

    budgets = Budget.objects.all()
    return render(request, 'costs/budget.html', {'form': form, 'budgets': budgets})