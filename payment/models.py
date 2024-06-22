from accounts.models import User
from django.db import models

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pidx = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    refunded = models.BooleanField()
    booking_id = models.IntegerField(blank=True,null=True)
    property_title = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status} - Booking ID: {self.booking_id} - Property Title: {self.property_title}"
