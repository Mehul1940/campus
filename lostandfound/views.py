from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import LostAndFound
from notifications.models import Notification
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.

@login_required
def list_items(request):
    item_status = request.GET.get('status')
    status = request.GET.get('filter_status')
    
    items = LostAndFound.objects.all()
    
    if item_status:
        items = items.filter(item_status=item_status)
    
    if status:
        items = items.filter(status=status)
    
    context = {
        'items': items,
        'selected_item_status': item_status,
        'selected_status': status,
    }
    return render(request, 'lostandfound/list.html', context)


@login_required
def report_item(request):
    if request.method == 'POST':
        item_type = request.POST.get('item_type')
        item_status = request.POST.get('item_status')
        description = request.POST.get('description')
        location = request.POST.get('location')
        date_found_lost = request.POST.get('date_found_lost')
        image = request.FILES.get('image')
        
        report = LostAndFound.objects.create(
            reported_by=request.user,
            item_type=item_type,
            item_status=item_status,
            description=description,
            location=location,
            date_found_lost=date_found_lost,
            image=image,
            status='open'
        )
        
        users_to_notify = User.objects.filter(userprofile__role__in=['admin', 'staff'])
        for user in users_to_notify:
            Notification.objects.create(
                user=user,
                title=f'New {item_status.title()} Item Report',
                message=f'{request.user.get_full_name()} reported a {item_status} {item_type}',
                notification_type='lost_found',
                related_item=report
            )
        
        messages.success(request, 'Report submitted successfully!')
        return redirect('lostandfound:list')
    
    return render(request, 'lostandfound/report.html')

def claim_item(request, item_id):
    item = get_object_or_404(LostAndFound, id=item_id)
    
    if item.status == 'open':
        item.status = 'claimed'
        item.claimed_by = request.user
        item.claim_date = timezone.now()
        item.save()

        Notification.objects.create(
            user=item.reported_by,
            title="Item Claimed",
            message=f"Someone has claimed the {item.item_type} you reported. Please coordinate with the campus office.",
            notification_type='lost_found',
            related_item=item
        )
        
        messages.success(request, "Item marked as claimed. Please visit the office to collect/verify.")
    
    return redirect('core:dashboard') 

def return_item(request, item_id):
    item = get_object_or_404(LostAndFound, id=item_id)
    
    if request.user.is_staff:
        item.status = 'returned'
        item.save()

        if item.claimed_by:
            Notification.objects.create(
                user=item.claimed_by,
                title="Item Returned",
                message=f"Your claim for {item.item_type} is complete. The item has been officially returned.",
                notification_type='lost_found',
                related_item=item
            )
            
    return redirect('lostandfound:list')