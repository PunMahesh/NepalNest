from django.db import models

# Create your models here.

class Ammenities(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name
    
class Other_Ammenities(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name

class Safety_Items(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name
    
class Extra_Items(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name



class PropertyInfo(models.Model):
    PROPERTY_TYPES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Hotel', 'Hotel'),
        ('Tent', 'Tent'),
        ('Guest_House', 'Guest House'),
        ('Bed_and_Breakfast', 'Beds and Breakfast'),
        ('HomeStay', 'HomeStay'),
        ('Cabin', 'Cabin'),
    ]
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=True, blank=True, default=None)
    GUEST_ROOM_CHOICES = [
        ('entire_place', 'Entire Place'),
        ('a_room', 'A Room'),
        ('shared_room', 'Shared Room'),
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
    PropertyPhoto = models.ImageField(upload_to="Photo", blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0, null=True)
    extra_items = models.ManyToManyField(Extra_Items)













