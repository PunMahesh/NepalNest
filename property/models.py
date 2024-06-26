from django.db import models
from accounts.models import User

# Create your models here.

class Ammenities(models.Model):
    name = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return self.name
    
class Other_Ammenities(models.Model):
    name = models.CharField(max_length=225, unique=True )

    def __str__(self):
        return self.name

class Safety_Items(models.Model):
    name = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return self.name
    
class Extra_Items(models.Model):
    name = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return self.name



class PropertyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    PROPERTY_TYPES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Hotel', 'Hotel'),
        ('Tent', 'Tent'),
        ('Guest House', 'Guest House'),
        ('Bed and Breakfast', 'Beds and Breakfast'),
        ('Homestay', 'HomeStay'),
        ('Cabin', 'Cabin'),
    ]
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=True, blank=True, default=None)
    GUEST_ROOM_CHOICES = [
        ('Entire Place', 'Entire Place'),
        ('Single Room', 'A Room'),
        ('Shared Room', 'Shared Room'),
    ]
    guest_room = models.CharField(max_length=20, choices=GUEST_ROOM_CHOICES, null=True, blank=True, default=None)
    Guest_number = models.IntegerField(default=None, null=True)
    bedrooms = models.IntegerField(default=1)
    bed = models.IntegerField(default=1)
    GUEST_BATHROOM_CHOICES = [
        ('private_bathroom', 'Private and Attached'),
        ('dedicated_bathroom', 'Dedicated'),
        ('shared_bathroom', 'Shared'),
    ]
    guest_bathroom = models.CharField(max_length=20, choices=GUEST_BATHROOM_CHOICES, null=True, blank=True, default=None)
    ammenities = models.ManyToManyField(Ammenities)
    other_ammenities = models.ManyToManyField(Other_Ammenities)
    safety_items = models.ManyToManyField(Safety_Items)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0, null=True)
    extra_items = models.ManyToManyField(Extra_Items)
    Status_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
    ]
    Status = models.CharField(max_length=20, choices=Status_CHOICES,default="Pending")
    Booking_Status_CHOICES = [
        ('Listing', 'Listing'),
        ('Booked', 'Booked'),
        ('Reserved', 'Reserved'),
    ]
    Booking_Status = models.CharField(max_length=20, choices=Booking_Status_CHOICES,default="Listing")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title

class PropertyPhoto(models.Model):
    property_info = models.ForeignKey(PropertyInfo, related_name="property_photo", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to = "Property_Photos")


class Review(models.Model):
    property = models.ForeignKey('PropertyInfo', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=255, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.property} by {self.user.full_name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(PropertyInfo, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_days = models.IntegerField()
    num_guests = models.IntegerField()
    before_service_fee = models.FloatField()
    service_fee = models.FloatField()
    total_price = models.FloatField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):  
        return f"{self.property.title} - {self.check_in_date} to {self.check_out_date}"






