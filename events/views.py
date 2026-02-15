from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Event, EventRegistration
from notifications.models import Notification

# Create your views here.

@login_required
def list_events(request):
    upcoming = request.GET.get('filter', 'upcoming')
    
    if upcoming == 'past':
        events_list = Event.objects.filter(event_date__lt=timezone.now()).order_by('-event_date')
    else:
        events_list = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')
    
    user_registrations = EventRegistration.objects.filter(user=request.user).values_list('event_id', flat=True) if request.user.is_authenticated else []
    
    for event in events_list:
        event.is_registered = event.id in user_registrations
    
    context = {
        'events': events_list,
        'filter_type': upcoming,
    }
    return render(request, 'events/list.html', context)

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists() if request.user.is_authenticated else False
    registrations = EventRegistration.objects.filter(event=event).count()
    
    context = {
        'event': event,
        'is_registered': is_registered,
        'registrations': registrations,
    }
    return render(request, 'events/detail.html', context)


@login_required
@require_POST
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.event_date < timezone.now():
        return JsonResponse({'success': False, 'message': 'Cannot register for past events'}, status=400)
    
    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({'success': False, 'message': 'Already registered'}, status=400)
    
    if event.registered_count >= event.capacity:
        return JsonResponse({'success': False, 'message': 'Event is full'}, status=400)
    
    EventRegistration.objects.create(user=request.user, event=event)
    event.registered_count += 1
    event.save()
    
    Notification.objects.create(
        user=request.user,
        title='Event Registration Confirmed',
        message=f'You are registered for {event.title}',
        notification_type='event',
        related_event=event
    )
    
    return JsonResponse({'success': True, 'message': 'Registered successfully!'})


@login_required
@require_POST
def unregister_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    if registration:
        registration.delete()
        event.registered_count = max(0, event.registered_count - 1)
        event.save()
    
    return JsonResponse({'success': True, 'message': 'Unregistered successfully!'})
