from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order', 'Order Update'),
        ('event', 'Event Notification'),
        ('cleanliness', 'Cleanliness Report'),
        ('lost_found', 'Lost & Found'),
        ('general', 'General Announcement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_order = models.ForeignKey('canteen.FoodOrder', on_delete=models.SET_NULL, null=True, blank=True)
    related_event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True)
    related_report = models.ForeignKey('cleanliness.CleanlinessReport', on_delete=models.SET_NULL, null=True, blank=True)
    related_item = models.ForeignKey('lostandfound.LostAndFound', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        app_label = 'notifications'
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Announcement(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        app_label = 'notifications'
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
    
    def __str__(self):
        return self.title