from django.contrib import admin
from .models import PropertyInfo,Ammenities,Other_Ammenities,Safety_Items,Extra_Items,Review,Booking
# Register your models here.

admin.site.register(PropertyInfo)
# admin.site.register(Ammenities)
# admin.site.register(Other_Ammenities)
# admin.site.register(Safety_Items)
# admin.site.register(Extra_Items)
admin.site.register(Review)
admin.site.register(Booking)


