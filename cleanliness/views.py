from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CleanlinessReport
from notifications.models import Notification

# Create your views here.
@login_required
def list_reports(request):
    status = request.GET.get('status')
    severity = request.GET.get('severity')
    
    reports = CleanlinessReport.objects.all()
    
    if status:
        reports = reports.filter(status=status)
    
    if severity:
        reports = reports.filter(severity=severity)
    
    context = {
        'reports': reports,
        'selected_status': status,
        'selected_severity': severity,
    }
    return render(request, 'cleanliness/list.html', context)


@login_required
def submit_report(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        issue_description = request.POST.get('issue_description')
        severity = request.POST.get('severity')
        image = request.FILES.get('image')
        
        report = CleanlinessReport.objects.create(
            reported_by=request.user,
            location=location,
            issue_description=issue_description,
            severity=severity,
            image=image,
            status='open'
        )
        
        maintenance_staff = User.objects.filter(userprofile__role='staff')
        for staff in maintenance_staff:
            Notification.objects.create(
                user=staff,
                title='New Cleanliness Report',
                message=f'Report #{report.id} - {location} ({severity.upper()})',
                notification_type='cleanliness',
                related_report=report
            )
        
        messages.success(request, 'Report submitted successfully!')
        return redirect('cleanliness:list')
    
    return render(request, 'cleanliness/submit.html')