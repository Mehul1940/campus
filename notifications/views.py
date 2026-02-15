from django.shortcuts import render , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification, Announcement
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)
    
    if request.GET.get('mark_read'):
        user_notifications.update(is_read=True)
    
    context = {
        'notifications': user_notifications,
    }
    return render(request, 'notifications/list.html', context)

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, "Notification deleted.")
    return redirect('notifications:list')

def announcements(request):
    announcements_list = Announcement.objects.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
    ).order_by('-priority', '-created_at')
    
    context = {
        'announcements': announcements_list,
    }
    return render(request, 'notifications/announcements.html', context)
