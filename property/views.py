from django.shortcuts import render,redirect
from .models import PropertyInfo
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import PropertyInfo, Ammenities, Other_Ammenities, Safety_Items,Extra_Items



# Create your views here.

@login_required
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
        PropertyPhoto = request.FILES.get("PropertyPhoto")
        price = request.POST.get('price')
        
        # Handling many-to-many fields
        amenities_names = request.POST.getlist('amenities')
        other_amenities_names = request.POST.getlist('other_amenities')
        safety_items_names = request.POST.getlist('safety_items')
        extra_items_names = request.POST.getlist('extra_items')

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
            PropertyPhoto=PropertyPhoto,
            price=price
        )
        # Handling many-to-many relationship for amenities
        amenities = []
        for amenity_name in amenities_names:
            amenity, created = Ammenities.objects.get_or_create(name=amenity_name)
            amenities.append(amenity)

        # Handling many-to-many relationship for other amenities
        other_amenities = []
        for other_amenity_name in other_amenities_names:
            other_amenity, created = Other_Ammenities.objects.get_or_create(name=other_amenity_name)
            other_amenities.append(other_amenity)

        # Handling many-to-many relationship for safety items
        safety_items = []
        for safety_item_name in safety_items_names:
            safety_item, created = Safety_Items.objects.get_or_create(name=safety_item_name)
            safety_items.append(safety_item)

        # Handling many-to-many relationship for extra items
        extra_items = []
        for extra_item_name in extra_items_names:
            extra_item, created = Extra_Items.objects.get_or_create(name=extra_item_name)
            extra_items.append(extra_item)

        # Adding many-to-many relationships
        property_info.ammenities.set(amenities)
        property_info.other_ammenities.set(other_amenities)
        property_info.safety_items.set(safety_items)
        property_info.extra_items.set(extra_items)
        
        # Save the property_info object
        property_info.save()
        return redirect('Property_list')
    return render(request, 'property.html')

@login_required
def myProperty(request):
    # Assuming you have a user object retrieved from your database
    user = User.objects.get(id=request.user.id)  # Adjust this according to your user retrieval logic
    
    # Splitting the full name to extract the first name
    first_name = user.full_name.split()[0] if user.full_name else ''
    print(first_name)
    return render(request, 'myProperty.html', {'first_name': first_name})