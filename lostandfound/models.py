from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LostAndFound(models.Model):
    ITEM_STATUS = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('claimed', 'Claimed'),
        ('returned', 'Returned'),
    ]
    
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=100)
    item_status = models.CharField(max_length=10, choices=ITEM_STATUS)
    description = models.TextField()
    location = models.CharField(max_length=200, help_text="Where the item was found/lost")
    date_found_lost = models.DateField()
    image = models.ImageField(upload_to='lost_found/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    report_date = models.DateTimeField(auto_now_add=True)
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_items')
    claim_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        app_label = 'lostandfound'
        ordering = ['-report_date']
        verbose_name = 'Lost & Found Item'
        verbose_name_plural = 'Lost & Found Items'
    
    def __str__(self):
        return f"{self.item_type} - {self.get_item_status_display()}"