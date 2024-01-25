from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def customer_dashboard(request):
    return render(request, 'dashboard/customer_dashboard.html')

@login_required
def engineer_dashboard(request):
    return render(request, 'dashboard/engineer_dashboard.html')