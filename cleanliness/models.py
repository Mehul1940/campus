from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CleanlinessReport(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    issue_description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    image = models.ImageField(upload_to='cleanliness_reports/', null=True, blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_reports')
    feedback = models.TextField(blank=True)
    
    class Meta:
        app_label = 'cleanliness'
        ordering = ['-report_date']
        verbose_name = 'Cleanliness Report'
        verbose_name_plural = 'Cleanliness Reports'
    
    def __str__(self):
        return f"Report #{self.id} - {self.location} ({self.get_severity_display()})"
