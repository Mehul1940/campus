from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from notifications.models import Notification, Announcement
from events.models import Event
from users.models import UserProfile
from core.models import ContactMessage
from canteen.models import FoodOrder
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    announcements = Announcement.objects.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
    ).order_by('-priority', '-created_at')[:5]
    
    context = {
        'announcements': announcements,
    }
    return render(request, 'core/index.html', context)


@login_required
def dashboard(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    recent_orders = FoodOrder.objects.filter(user=request.user)[:3]
    
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    upcoming_events = Event.objects.filter(
        event_date__gte=timezone.now()
    ).order_by('event_date')[:3]
    
    announcements = Announcement.objects.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
    ).order_by('-priority')[:3]
    
    context = {
        'user_profile': user_profile,
        'recent_orders': recent_orders,
        'unread_notifications': unread_notifications,
        'upcoming_events': upcoming_events,
        'announcements': announcements,
    }
    return render(request, 'core/dashboard.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        full_email_body = f"From: {name} <{email}>\n\n{message_text}"
        try:
            send_mail(
                subject,
                full_email_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Success! The admin team has received your message.")
        except:
            messages.warning(request, "Message saved, but email notification failed.")

        return redirect('core:contact')
    return render(request, 'core/contact.html')