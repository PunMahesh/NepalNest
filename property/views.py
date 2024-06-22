import base64
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect, reverse
import googlemaps
from .models import PropertyInfo
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import PropertyInfo, Ammenities, Other_Ammenities, Safety_Items,Extra_Items,PropertyPhoto,Review,Booking
from django.db.models import Q
from datetime import date, datetime
import hmac
import hashlib
import uuid
from .forms import ReviewForm
from django.core.mail import send_mail
from django.http import JsonResponse
import requests




# Create your views here.

@login_required
def Property_list(request, property_id=None):
    # If property_id is provided, it means we are editing an existing property
    if property_id:
        property_obj = get_object_or_404(PropertyInfo, pk=property_id)
    else:
        property_obj = None

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

        # Extract location details from the POST request
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')
        street_address = request.POST.get('street_address')

        # Handling many-to-many fields
        amenities_names = request.POST.getlist('amenities')
        other_amenities_names = request.POST.getlist('other_amenities')
        safety_items_names = request.POST.getlist('safety_items')
        extra_items_names = request.POST.getlist('extra_items')

        # Get the list of uploaded photos
        photos = request.FILES.getlist("PropertyPhoto")

        # Handle the scenario where property_id is provided
        if property_id:
            # Update the existing property with new data
            property_obj.property_type = property_type
            property_obj.guest_room = guest_room
            property_obj.Guest_number = guest_number
            property_obj.bedrooms = bedrooms
            property_obj.bed = bed
            property_obj.guest_bathroom = guest_bathroom
            property_obj.title = title
            property_obj.description = description
            property_obj.price = price
            property_obj.latitude = latitude
            property_obj.longitude = longitude
            property_obj.city = city
            property_obj.province = province
            property_obj.postal_code = postal_code
            property_obj.street_address = street_address

            # Save the updated property
            property_obj.save()

            return redirect('Property_list')

        else:
            # Create PropertyInfo object with property details
            property_info = PropertyInfo.objects.create(
                user=request.user,
                property_type=property_type,
                guest_room=guest_room,
                Guest_number=guest_number,
                bedrooms=bedrooms,
                bed=bed,
                guest_bathroom=guest_bathroom,
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                street_address=street_address,
                city=city,
                province=province,
                postal_code=postal_code
            )


            # Check if at least 5 photos are uploaded
            if len(photos) < 5:
                return render(request, "property.html", {"error_message": "Please upload at least 5 images"})

            # Create PropertyPhoto objects for each uploaded photo
            for photo in photos:
                PropertyPhoto.objects.create(property_info=property_info, photo=photo)

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
        
    return render(request, 'property.html', {'property_obj': property_obj})




def search_map(request):
    return render(request, 'maps.html')
@login_required
def search_properties(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        if location:
            try:
                # Query properties based on location
                properties_near_location = PropertyInfo.objects.filter(
                    Q(street_address__icontains=location) | Q(city__icontains=location),
                    Status="Verified",
                    Booking_Status="Listing"
                )
                if properties_near_location.exists():
                    # Serialize property data with additional information
                    property_data = []
                    for prop in properties_near_location:
                        # Get the URL of the property's photo if available
                        photo_url = prop.property_photo.first().photo.url if prop.property_photo.first() else None
                        
                        property_data.append({
                            'id': prop.id,
                            'name': prop.title,
                            'latitude': float(prop.latitude),
                            'longitude': float(prop.longitude),
                            'price': prop.price,
                            'property_type': prop.property_type,
                            'photo_url': photo_url,  # Add photo URL
                            # Add other property information as needed
                        })

                    return JsonResponse(property_data, safe=False)
                else:
                    # Return a message indicating no properties were found
                    return JsonResponse({'message': 'No properties found for the specified location.'})
            except ValueError as e:
                # Handle invalid latitude or longitude values
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                # Handle other exceptions
                return JsonResponse({'error': 'An error occurred while processing the request.'}, status=500)

    # Return a message indicating no location provided or other method than GET
    return JsonResponse({'message': 'No location provided or invalid request method.'}, status=400)


@login_required
def myProperty(request, info_type=None):
    user = User.objects.get(id=request.user.id)  
    properties = PropertyInfo.objects.filter(user=user)
    user_properties = PropertyInfo.objects.filter(user=request.user)

    # Initialize pending_requests to an empty queryset
    pending_requests = Booking.objects.none()
    
    # Get all pending reservation requests associated with the properties
    if info_type == 'pending_requests':
        pending_requests = Booking.objects.filter(property__in=properties, status='pending')
    
    first_name = user.full_name.split()[0] if user.full_name else ''

    # Prepare the context based on the info_type parameter
    if info_type == 'pending_requests':
        context = {'first_name': first_name, 'pending_requests': pending_requests, 'user_properties': user_properties}
    elif info_type == 'upcoming_reservations':
        # Logic to retrieve upcoming reservations
        context = {'first_name': first_name, 'user_properties': user_properties}  # Add your logic here
    elif info_type == 'currently_hosting':
        # Logic to retrieve currently hosting properties
        context = {'first_name': first_name, 'user_properties': user_properties}  # Add your logic here
    elif info_type == 'checked_out':
        # Logic to retrieve checked out properties
        context = {'first_name': first_name, 'user_properties': user_properties}  # Add your logic here
    else:
        # Default context
        context = {'first_name': first_name, 'pending_requests': pending_requests, 'user_properties': user_properties}
    
    return render(request, 'myProperty.html', context)

@login_required
def Hosting(request, info_type=None):
    user = get_object_or_404(User, id=request.user.id)  

    properties = PropertyInfo.objects.filter(user=user)
    user_properties = PropertyInfo.objects.filter(user=request.user)

    # Initialize pending_requests to an empty queryset
    pending_requests = Booking.objects.none()

    first_name = user.full_name.split()[0] if user.full_name else ''

    if info_type == 'my_listings':
        my_listings = PropertyInfo.objects.filter(user=user)
        context = {'first_name': first_name, 'my_listings': my_listings}  
    elif info_type == 'pending_requests':
        pending_requests = Booking.objects.filter(property__in=properties, status='pending')
        context = {'first_name': first_name, 'pending_requests': pending_requests, 'user_properties': user_properties}
    elif info_type == 'currently_hosting':
        currently_hosting = Booking.objects.filter(status="accepted", check_in_date__lte=date.today(), check_out_date__gte=date.today())
        context = {'first_name': first_name, 'user_properties': user_properties, 'currently_hosting':currently_hosting}  
    elif info_type == 'upcoming_reservation':
        upcoming_reservation = Booking.objects.filter(status="accepted", check_in_date__gt=date.today())
        context = {'first_name': first_name, 'user_properties': user_properties,'upcoming_reservation':upcoming_reservation} 
    elif info_type == 'checked_out':
        context = {'first_name': first_name, 'user_properties': user_properties}  
    else:
        context = {'first_name': first_name}
    
    return render(request, 'Hosting.html', context)

def delete_listing(request, listing_id):
    listing = get_object_or_404(PropertyInfo, id=listing_id)
    
    if request.method == 'POST':
        listing.delete()
        return redirect(reverse('Hosting', kwargs={'info_type': 'my_listings'}))
    
    return render(request, 'Hosting.html', {'listing': listing})

def accept_reservation(request, booking_id):

    booking = Booking.objects.get(id=booking_id)
    booking.status = 'accepted'
    booking.save()

    property_obj = booking.property
    property_obj.Booking_Status = 'Reserved'
    property_obj.save()

    messages.success(request, 'Reservation accepted successfully.')
    user_email = booking.user.email
    property_title = booking.property.title
    guest_name = booking.user.full_name
    send_reservation_notification_email(user_email, 'accepted', property_title, guest_name)
    url = reverse('Hosting', kwargs={'info_type': 'my_listings'})
    return redirect(url)
def decline_reservation(request, booking_id):

    booking = Booking.objects.get(id=booking_id)
    booking.status = 'declined'
    booking.save()

    messages.info(request, 'Reservation declined.')
    user_email = booking.user.email
    property_title = booking.property.title
    guest_name = booking.user.full_name
    send_reservation_notification_email(user_email, 'declined', property_title, guest_name)   
    url = reverse('Hosting', kwargs={'info_type': 'my_listings'})
    return redirect(url)
def send_reservation_notification_email(user_email, status, property_title, guest_name):
    subject = 'Reservation Notification'

    if status == 'accepted':
        message = f"Hello,\n\nYour reservation request for property '{property_title}' has been accepted.\n\nRegards,\nThe NepalNest Team"
    elif status == 'declined':
        message = f"Hello,\n\nYour reservation request for property '{property_title}' has been declined.\n\nRegards,\nThe NepalNest Team"

    send_mail(subject, message, "info.NepalNest@gmail.com", [user_email])

def stays_type(request, property_type):
    if property_type == 'All':
        filtered_properties = PropertyInfo.objects.filter(Status="Verified", Booking_Status="Listing")
    else:
        filtered_properties = PropertyInfo.objects.filter(property_type=property_type,Status="Verified", Booking_Status="Listing")
    
    return render(request, 'stays.html', {'filtered_properties': filtered_properties})

def stays(request):
    data = PropertyInfo.objects.filter(Status="Verified", Booking_Status="Listing")
    return render(request, 'stays.html', {'data': data})

def staysByCity(request,city_name):
    city = PropertyInfo.objects.filter(Status="Verified", Booking_Status="Listing", city=city_name)
    return render(request, 'stays.html', {'city': city})

def search(request):
    query = request.GET.get('search')
    search_performed = bool(query) 
    if query:
        Search_properties = PropertyInfo.objects.filter(
            Q(title__icontains=query) |
            Q(property_type__icontains=query) |
            Q(ammenities__name__icontains=query) |     
            Q(other_ammenities__name__icontains=query) |
            Q(safety_items__name__icontains=query) |
            Q(extra_items__name__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query),
            Q(Status="Verified") | Q(Booking_Status="Listing")
            ).distinct()    
    else:
        Search_properties = PropertyInfo.objects.none()
    return render(request, 'stays.html', {'Search_properties': Search_properties, 'search_performed': search_performed})


# def property_detail(request, property_id):
#     property_obj = get_object_or_404(PropertyInfo, id=property_id)
#     today = date.today()

#     icons = {
#         "Smoke Alarm": "fa-smoke",
#         "First Aid": "fa-first-aid",
#         "Fire Extinguisher": "fa-extinguisher",
#         "Carbon Monoxide Alarm": "fa-alarm",
#     }
#     return render(request, 'property-details.html', {'property': property_obj, 'today': today,'icons': icons})

# def submit_review(request, property_id):
#     url = request.META.get("HTTP_REFERER")
#     if request.method == 'POST':
#         try:
#             reviews = Review.objects.get(user__id=request.user.id, property__id=property_id)
#             form = ReviewForm(request.POST, instance=reviews)
#             form.save()
#             messages.success(request, "Thank you! Your Review has been updated.")
#             return redirect(url)

#         except Review.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = form.save(commit=False)
#                 data.property_id = property_id
#                 data.user_id = request.user.id
#                 data.save()
#                 messages.success(request, "Thank you! Your Review has been submitted.")
#                 return redirect(url)
            
def submit_review(request, property_id):
    url = request.META.get("HTTP_REFERER")
    property_obj = get_object_or_404(PropertyInfo, id=property_id)
    review = None

    if request.method == 'POST':
        try:
            review = Review.objects.get(user=request.user, property=property_obj)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you! Your Review has been updated.")
                return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.property = property_obj
                data.user = request.user
                data.save()
                messages.success(request, "Thank you! Your Review has been submitted.")
                return redirect(url)
    else:
        try:
            review = Review.objects.get(user=request.user, property=property_obj)
            form = ReviewForm(instance=review)
        except Review.DoesNotExist:
            form = ReviewForm()
    all_reviews = Review.objects.filter(property=property_obj).exclude(user=request.user)

    return render(request, 'property-details.html', {
        'property': property_obj,
        'form': form,
        'review': review,
        'all_reviews':all_reviews,
    })
def property_detail(request, property_id):
    property_obj = get_object_or_404(PropertyInfo, id=property_id)
    today = date.today()
    icons = {
    "House": "fas fa-home",
    "Apartment": "fas fa-building",
    "Hotel": "fas fa-hotel",
    "Tent": "fas fa-campground",
    "Guest House": "fas fa-home",
    "Bed and Breakfast": "fas fa-bed",
    "Homestay": "fas fa-home-alt",
    "Cabin": "fas fa-home",

    "wifi": "fa fa-wifi",
    "TV": "fa fa-television",
    "Kitchen": "fa fa-cutlery",
    "Washer": "fa fa-bath",
    "Free Parking": "fa fa-parking",
    "Paid Parking": "fa fa-parking",
    "A/C": "fa fa-snowflake",
    "Workspace": "fa fa-laptop",


    "Pool": "fa fa-swimming-pool",
    "Hottub": "fa fa-hot-tub",
    "Patio": "fa fa-umbrella-beach",
    "BBQGrill": "fa fa-fire-alt",
    "Outdoor Dining Area": "fa fa-utensils",
    "Fire Pit": "fa fa-fire",
    "Pool Table": "fa fa-gamepad",
    "Indoor Fire Place": "fa fa-fire",
    "Excersie Equiment": "fa fa-dumbbell",
    "Lake Access": "fa fa-water",
    "Ski": "fa fa-skiing",
    "Outdoor Shower": "fa fa-shower",
    "Smoke Alarm": "fa fa-exclamation-triangle",

    "First Aid": "fa fa-medkit",
    "Fire Ext": "fa fa-fire-extinguisher",
    "CO Alarm": "fa fa-biohazard",

    "Camera": "fa fa-camera",
    "Firearms": "fa fa-gun",
    "Pet": "fa fa-paw",
    }

    
    # Handle booking submission
    if request.method == 'POST':
        # Retrieve form data
        check_in_date = request.POST.get('arrival')
        check_out_date = request.POST.get('departure')
        num_guests = request.POST.get('num_guests')
        number_of_days = request.POST.get('num_of_days')
        before_service_fee = request.POST.get('before_service_fee')
        service_fee = request.POST.get('service_price')
        total_price = request.POST.get('total_price')

        # Create booking record
        booking = Booking.objects.create(
            user=request.user,
            property=property_obj,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            num_guests=num_guests,
            number_of_days=number_of_days,
            before_service_fee=before_service_fee,
            service_fee=service_fee,
            total_price=total_price
        )

        # Redirect to a confirmation page or display a success message
        return redirect('book', booking_id=booking.id)
    
    return render(request, 'property-details.html', {'property': property_obj, 'today': today, 'icons': icons})

def genSha256(key, message):
    key = key.encode('utf-8')
    message = message.encode('utf-8')

    hmac_sha256 = hmac.new(key, message, hashlib.sha256)
    digest = hmac_sha256.digest()

    # Convert the digest to a Base64-encoded string
    signature = base64.b64encode(digest).decode('utf-8')

    return signature


def book(request, booking_id):
    # Retrieve the booking object
    booking = get_object_or_404(Booking, pk=booking_id)
        # Generate UUID
    uuid_value = uuid.uuid4() 

    # Example usage:
    secret_key = "8gBm/:&EnhH.1/q"
    data_to_sign = f"total_amount={booking.total_price},transaction_uuid={uuid_value},product_code=EPAYTEST"

    # Generate signature
    signature = genSha256(secret_key, data_to_sign)
    print("Signature",signature)
    print("data_to_sign",data_to_sign)
    print('transaction_uuid',uuid_value)
    print('total_price',booking.total_price)
    
    if request.method == 'POST':
        # Extract new check-in and check-out dates from the request data
        new_check_in_date_str = request.POST.get('new_check_in_date')
        new_check_out_date_str = request.POST.get('new_check_out_date')

        # Convert the existing check-in and check-out dates to datetime objects
        existing_check_in_date = booking.check_in_date
        existing_check_out_date = booking.check_out_date

        # Use existing dates if new dates are not provided
        if not new_check_in_date_str:
            new_check_in_date = existing_check_in_date
        else:
            new_check_in_date = datetime.strptime(new_check_in_date_str, '%Y-%m-%d')

        if not new_check_out_date_str:
            new_check_out_date = existing_check_out_date
        else:
            new_check_out_date = datetime.strptime(new_check_out_date_str, '%Y-%m-%d')

        # Validate the form data
        if new_check_out_date <= new_check_in_date:
            return HttpResponse("Invalid date range. Check-out date must be after check-in date.")

        # Calculate the number of days between the new check-in and check-out dates
        new_num_days = (new_check_out_date - new_check_in_date).days

        # Update the booking object with the new dates and number of days
        booking.check_in_date = new_check_in_date
        booking.check_out_date = new_check_out_date
        booking.number_of_days = new_num_days

        # Calculate the total price of the booking
        booking.before_service_fee = new_num_days * booking.property.price
        booking.service_fee = (new_num_days * booking.property.price) * 0.1
        booking.total_price = (new_num_days * booking.property.price) + booking.service_fee

        # Save the updated booking object
        booking.save()


        if request.POST.get('action') == 'reservation':
            # Handle reservation scenario
            booking.status = 'pending'
            notify_host(booking.property.user.email, booking.property.title,booking.user.full_name)
            booking.save()
            # Redirect to a success page or display a message
            return redirect('stays')  # Replace 'reservation_success' with your URL nam

    return render(request, 'book-reserve.html',{'booking_id':booking_id,'booking':booking,'signature': signature, 'transaction_uuid': uuid_value, 'total_amount': booking.total_price})

def notify_host(host_email, property_title,guest_name):
    subject = f"New Reservation for "
    message = f"Hello,\n\nYou have a new reservation request for your property '{property_title}' from {guest_name} .\n\nPlease login to your account to accept or decline the reservation.\n\nRegards,\nThe NepalNest Team"
    sender_email = "info.NepalNest@gmail.com"
    recipient_email = host_email
    send_mail(subject, message, sender_email, [recipient_email])

def about(request):
    # booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'about.html')


def filter_property(request):
    # Retrieve all properties
    properties = PropertyInfo.objects.filter(Status="Verified", Booking_Status="Listing")
    print(properties)

    # Filter properties based on user input
    if request.method == 'GET':
        property_type = request.GET.get('property_type')
        guest_room = request.GET.get('guest_room')
        Guest_number = request.GET.get('guest_number')
        bedrooms = request.GET.get('bedrooms')
        bed = request.GET.get('bed')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if property_type:
            properties = properties.filter(property_type=property_type)
        if guest_room:
            guest_room_choice = dict(PropertyInfo.GUEST_ROOM_CHOICES).get(guest_room)
            properties = properties.filter(guest_room=guest_room_choice)
            print(properties)
        if Guest_number:
            properties = properties.filter(Guest_number=Guest_number)
        if bedrooms:
            properties = properties.filter(bedrooms=bedrooms)
        if bed:
            properties = properties.filter(bed=bed)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)

    context = {
        'properties': properties
    }

    return render(request, 'stays.html', context)

@login_required
def edit_property(request, property_id):
    # Retrieve the property object to edit or return 404 if not found
    property_obj = get_object_or_404(PropertyInfo, pk=property_id)

    # Retrieve selected amenities for the property object
    selected_amenities = property_obj.ammenities.all()
    selected_other_amenities = property_obj.other_ammenities.all()
    selected_safety_items = property_obj.safety_items.all()
    selected_extra_items = property_obj.extra_items.all()

    print(property_obj.bedrooms)

    # Extract names of selected amenities into lists using list comprehension
    selected_amenities_names = [amenity.name for amenity in selected_amenities]
    selected_other_amenities_names = [other_amenity.name for other_amenity in selected_other_amenities]
    selected_safety_items_names = [safety_item.name for safety_item in selected_safety_items]
    selected_extra_items_names = [extra_item.name for extra_item in selected_extra_items]

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

        # Extract location details from the POST request
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')
        street_address = request.POST.get('street_address')

        # Handling many-to-many fields
        amenities_names = request.POST.getlist('amenities')
        other_amenities_names = request.POST.getlist('other_amenities')
        safety_items_names = request.POST.getlist('safety_items')
        extra_items_names = request.POST.getlist('extra_items')

        # Get the list of uploaded photos
        photos = request.FILES.getlist("PropertyPhoto")

        # Handle the scenario where property_id is provided
        if property_id:
            # Update the existing property with new data
            property_obj.property_type = property_type
            property_obj.guest_room = guest_room
            property_obj.Guest_number = guest_number
            property_obj.bedrooms = bedrooms
            property_obj.bed = bed
            property_obj.guest_bathroom = guest_bathroom
            property_obj.title = title
            property_obj.description = description
            property_obj.price = price
            property_obj.latitude = latitude
            property_obj.longitude = longitude
            property_obj.city = city
            property_obj.province = province
            property_obj.postal_code = postal_code
            property_obj.street_address = street_address

            property_obj.ammenities.set(Ammenities.objects.filter(name__in=amenities_names))
            property_obj.other_ammenities.set(Other_Ammenities.objects.filter(name__in=other_amenities_names))
            property_obj.safety_items.set(Safety_Items.objects.filter(name__in=safety_items_names))
            property_obj.extra_items.set(Extra_Items.objects.filter(name__in=extra_items_names))

            property_obj.save()
            # Handle file uploads
            # Remove existing photos associated with the property
            PropertyPhoto.objects.filter(property_info=property_obj).delete()

            # Check if at least 5 photos are uploaded
            if len(photos) < 5:
                return render(request, "property.html", {"error_message": "Please upload at least 5 images"})

            # Create PropertyPhoto objects for each uploaded photo
            for photo in photos:
                PropertyPhoto.objects.create(property_info=property_obj, photo=photo)

        return redirect('edit_property', property_id=property_id)


    # Define context dictionary with all required data
    context = {
        'property_obj': property_obj,
        'selected_amenities_names': selected_amenities_names,
        'selected_other_amenities_names': selected_other_amenities_names,
        'selected_safety_items_names': selected_safety_items_names,
        'selected_extra_items_names': selected_extra_items_names,
    }

    # Render the edit property form with pre-filled data
    return render(request, 'edit_listing.html', context)





def my_booking(request):
    user = get_object_or_404(User, id=request.user.id)  

    properties = PropertyInfo.objects.filter(user=user)
    user_properties = PropertyInfo.objects.filter(user=request.user)

    # Initialize pending_requests to an empty queryset
    pending_requests = Booking.objects.none()

    bookings = Booking.objects.filter(user=request.user)
    
    # Get all pending reservation requests associated with the properties
    # if info_type == 'my_listings':
    #     my_listings = PropertyInfo.objects.filter(user=user)
    # elif info_type == 'pending_requests':
    #     pending_requests = Booking.objects.filter(property__in=properties, status='pending')
    

    first_name = user.full_name.split()[0] if user.full_name else ''
    return render(request, 'my_booking.html',{'first_name':first_name,'bookings': bookings})

def booking_page(request):
    # Retrieve bookings associated with the current user
    user_bookings = Booking.objects.filter(user=request.user)

    # Pass bookings to the template for rendering
    return render(request, 'booking_page.html', {'bookings': user_bookings})