import base64
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
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


# Create your views here.

@login_required
def Property_list(request):
    if request.method == 'POST':
        # Extract property details from the POST request
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
        amenities_names = request.POST.getlist('amenities')
        other_amenities_names = request.POST.getlist('other_amenities')
        safety_items_names = request.POST.getlist('safety_items')
        extra_items_names = request.POST.getlist('extra_items')


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
            price=price
        )

        # Get the list of uploaded photos
        photos = request.FILES.getlist("PropertyPhoto")

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

    return render(request, 'property.html')



@login_required
def myProperty(request):
    user = User.objects.get(id=request.user.id)  
    # Get all properties owned by the user
    properties = PropertyInfo.objects.filter(user=user)
    
    # Get all pending reservation requests associated with the properties
    pending_requests = Booking.objects.filter(property__in=properties, status='pending')
    first_name = user.full_name.split()[0] if user.full_name else ''
    print(first_name)
    return render(request, 'myProperty.html', {'first_name': first_name, 'pending_requests': pending_requests})

def accept_reservation(request, booking_id):

    booking = Booking.objects.get(id=booking_id)
    booking.status = 'accepted'
    booking.save()

    property_obj = booking.property
    property_obj.reserved = True
    property_obj.save()

    messages.success(request, 'Reservation accepted successfully.')
    user_email = booking.user.email
    property_title = booking.property.title
    guest_name = booking.user.full_name
    send_reservation_notification_email(user_email, 'accepted', property_title, guest_name)
    return redirect('myProperty')

def decline_reservation(request, booking_id):

    booking = Booking.objects.get(id=booking_id)
    booking.status = 'declined'
    booking.save()

    messages.info(request, 'Reservation declined.')
    user_email = booking.user.email
    property_title = booking.property.title
    guest_name = booking.user.full_name
    send_reservation_notification_email(user_email, 'declined', property_title, guest_name)   
    return redirect('myProperty')

def send_reservation_notification_email(user_email, status, property_title, guest_name):
    subject = 'Reservation Notification'

    if status == 'accepted':
        message = f"Hello,\n\nYour reservation request for property '{property_title}' has been accepted.\n\nRegards,\nThe NepalNest Team"
    elif status == 'declined':
        message = f"Hello,\n\nYour reservation request for property '{property_title}' has been declined.\n\nRegards,\nThe NepalNest Team"

    send_mail(subject, message, "info.NepalNest@gmail.com", [user_email])

def stays_type(request, property_type):
    if property_type == 'All':
        filtered_properties = PropertyInfo.objects(reserved=False)
    else:
        filtered_properties = PropertyInfo.objects.filter(property_type=property_type, reserved=False)
    
    return render(request, 'stays.html', {'filtered_properties': filtered_properties})

def stays(request):
    data = PropertyInfo.objects.filter(reserved=False)
    return render(request, 'stays.html', {'data': data})

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
            reserved=False
            ).distinct()    
    else:
        Search_properties = PropertyInfo.objects.none()
    return render(request, 'stays.html', {'Search_properties': Search_properties, 'search_performed': search_performed})


def property_detail(request, property_id):
    property_obj = get_object_or_404(PropertyInfo, id=property_id)
    today = date.today()
    return render(request, 'property-details.html', {'property': property_obj, 'today': today})

def submit_review(request, property_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(user__id=request.user.id, property__id=property_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your Review has been updated.")
            return redirect(url)

        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.property_id = property_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your Review has been submitted.")
                return redirect(url)
def property_detail(request, property_id):
    property_obj = get_object_or_404(PropertyInfo, id=property_id)

    
    # Handle booking submission
    if request.method == 'POST' and 'arrival' in request.POST:
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
    
    today = date.today()

    return render(request, 'property-details.html', {'property': property_obj,'today': today})

def book(request, booking_id):
    # Retrieve the booking object
    booking = get_object_or_404(Booking, pk=booking_id)
    
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
            return redirect('payment')  # Replace 'reservation_success' with your URL name
        else:
            # Handle direct payment scenario (not implemented yet)
            # Redirect to a page for direct payment
            return redirect('payment')  # Replace 'direct_payment' with your URL name

    return render(request, 'book-reserve.html', {'booking': booking})

def notify_host(host_email, property_title,guest_name):
    subject = f"New Reservation for "
    message = f"Hello,\n\nYou have a new reservation request for your property '{property_title}' from {guest_name} .\n\nPlease login to your account to accept or decline the reservation.\n\nRegards,\nThe NepalNest Team"
    sender_email = "info.NepalNest@gmail.com"
    recipient_email = host_email
    send_mail(subject, message, sender_email, [recipient_email])



# def confirm_reservation(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)

#     if request.method == 'POST':
#         action = request.POST.get('action')

#         if action == 'accept':
#             # Handle accepting reservation
#             booking.status = 'accepted'
#             booking.save()
#             messages.success(request, 'Reservation accepted successfully.')
#             return redirect('myProperty')  # Redirect to the dashboard or any other page
            
#         elif action == 'decline':
#             # Handle declining reservation
#             booking.status = 'declined'
#             booking.save()
#             messages.success(request, 'Reservation declined successfully.')
#             return redirect('myProperty')  # Redirect to the dashboard or any other page

#     # Filter bookings based on the properties owned by the current user
#     user_bookings = Booking.objects.filter(property__user=request.user)

#     return render(request, 'myProperty.html', {'user_bookings': user_bookings})


def payment(request):
    # booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment.html')




def about(request):
    # booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'about.html')








    # def genSha256(key, message):
    #     # Convert the key and message to bytes if they're not already
    #     key_bytes = bytes(key, 'utf-8')
    #     message_bytes = bytes(message, 'utf-8')

    #     # Calculate the HMAC using SHA256
    #     hmac_digest = hmac.new(key_bytes, message_bytes, hashlib.sha256).digest()

    #     # Encode the result in base64
    #     signature = base64.b64encode(hmac_digest).decode('utf-8')

    #     return signature

    # print(booking.total_price)
    # uuid_val = uuid.uuid4()
    # # Example usage:
    # secret_key = "8gBm/:&EnhH.1/q"
    # data_to_sign = f"{booking.total_price},{uuid_val},EPAYTEST"
    # print(data_to_sign)
    # print({booking.total_price})

    # result = genSha256(secret_key, data_to_sign)
    # print(result)

#     def generate_signature(total_amount, transaction_uuid, product_code, secret_key):
#         # Concatenate input parameters in the specified order
#         data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    
#         # Convert the secret key to bytes
#         key_bytes = bytes(secret_key, 'utf-8')
    
#         # Convert the data to sign to bytes
#         data_bytes = bytes(data_to_sign, 'utf-8')
    
#         # Generate HMAC using SHA-256
#         hmac_digest = hmac.new(key_bytes, data_bytes, hashlib.sha256).digest()
    
#         # Encode the result in base64
#         signature = base64.b64encode(hmac_digest).decode('utf-8')
    
#         return signature

# # Example usage
#     total_amount = "100"
#     transaction_uuid = "11-201-13"
#     product_code = "EPAYTEST"
#     secret_key = "8gBm/:&EnhH.1/q"

#     result = generate_signature(total_amount, transaction_uuid, product_code, secret_key)
#     print("Result:", result)



def filter_property(request):
    # Retrieve all properties
    properties = PropertyInfo.objects.all()

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
    # Map the guest room value to its corresponding choice in the model
            guest_room_choice = dict(PropertyInfo.GUEST_ROOM_CHOICES).get(guest_room)
    # Filter properties based on the mapped choice
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
