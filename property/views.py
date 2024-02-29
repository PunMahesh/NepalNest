from django.shortcuts import render,redirect
from .models import PropertyInfo
from django.contrib.auth.decorators import login_required


# Create your views here.

# @login_required
def Property_list(request):
    if request.method == 'POST':
        property_type = request.POST.get('property__type')
        guest_room = request.POST.get('guest__room')
        guest_number = request.POST.get('guest__number')
        bedrooms = request.POST.get('bedroom__number')
        bed = request.POST.get('bed__number')
        guest_bathroom = request.POST.get('guest__bathroom')
        title = request.POST.get('title')  
        description = request.POST.get('description')
        price = request.POST.get('price')
        
        # Handling many-to-many fields
        amenities = request.POST.getlist('amenities')
        other_amenities = request.POST.getlist('other_amenities')
        safety_items = request.POST.getlist('safety_items')
        extra_items = request.POST.getlist('extra_items')

        if guest_number == "":
            guest_number = 1
        if bedrooms == "":
            bedrooms = 1
        if bed == "":
            bed = 1
        if price == "":
            price = 0

        # Saving data to PropertyInfo model
        property_info = PropertyInfo.objects.create(
            property_type=property_type,
            guest_room=guest_room,
            Guest_number=guest_number,
            bedrooms=bedrooms,
            bed=bed,
            guest_bathroom=guest_bathroom,
            title=title,
            description=description,
            price=price
        )
        
        # Adding many-to-many relationships
        property_info.ammenities.add(*amenities)
        property_info.other_ammenities.add(*other_amenities)
        property_info.safety_items.add(*safety_items)
        property_info.extra_items.add(*extra_items)
        
        # Save the property_info object
        property_info.save()
        
        # Redirect to a success page or wherever appropriate
        # return redirect('property_list')
        # return redirect('success_page')
    
    return render(request, 'property.html')