from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import FoodOrder
from notifications.models import Notification

@receiver(pre_save, sender=FoodOrder)
def send_order_status_notification(sender, instance, **kwargs):
    if not instance.pk:
        return

    previous_order = FoodOrder.objects.get(pk=instance.pk)
    
    if previous_order.status != instance.status:
        Notification.objects.create(
            user=instance.user,
            title=f"Your order #{instance.id} status updated",
            message=f"Your order status has changed from '{previous_order.status}' to '{instance.status}'.",
            notification_type='order',
            related_order=instance
        )
