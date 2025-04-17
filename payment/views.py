import base64
from django.shortcuts import redirect, render
import requests
import json
from property.models import Booking
from payment.models import Transaction
import hmac
import hashlib
import uuid
from django.contrib import messages

# Create your views here.

def update_booking_and_property_status(booking):
    booking.status = 'accepted'
    booking.save()

    property_obj = booking.property
    property_obj.booking_status = 'Booked'
    property_obj.save()


def return_url(request,booking_id):
    if request.method == 'GET':
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        headers = {
            'Authorization': f'key {config("KHALTI_SECRET_KEY")}',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        data = json.dumps({
            'booking_id': booking_id,
            'pidx': pidx
            })
        
        # Make a POST request to the Khalti API to verify payment
        res = requests.post(url, headers=headers, data=data)
        print(res.text)

        new_res = json.loads(res.text)
        print("new_res hai: ",new_res)
        if new_res.get('status') == 'Completed':
            booking = Booking.objects.get(id=booking_id)
        
            # Create a new Transaction instance and save it to the database
            transaction = Transaction.objects.create(
                user=booking.user,
                pidx=new_res.get('pidx'),
                total_amount=booking.total_price,
                status=new_res.get('status'),
                transaction_id=new_res.get('transaction_id'),
                fee=new_res.get('fee'),
                refunded=new_res.get('refunded'),
                booking_id=booking.id,
                property_title=booking.property.title
            )
        
            # Additional logic for updating booking and property status
            booking.status = 'accepted'
            booking.save()
        
            property_obj = booking.property
            property_obj.Booking_Status = 'Booked'
            property_obj.save()
        
            messages.success(request, 'Payment Successful!')
        
            return render(request, "index.html")


        return redirect('/')


def initiate_khalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    user = request.user


    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = request.POST.get('amount')

    print(purchase_order_id)
    print(amount)
    print(return_url)


    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000/",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "NepalNest",
        "customer_info": {
        "name": user.full_name,
        "email": user.email,
        "phone": user.contact
        }
    })
    headers = {
        'Authorization': f'key {config("KHALTI_SECRET_KEY")}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    new_response = json.loads(response.text)
    print(new_response)

    return redirect(new_response['payment_url'])
    #return render(request, 'book-reserve.html', {'uuid_value': uuid_value, 'booking': booking})





# def initiate_esewa(request):
#     def genSha256(key, message):
#         key = key.encode('utf-8')
#         message = message.encode('utf-8')

#         hmac_sha256 = hmac.new(key, message, hashlib.sha256)
#         digest = hmac_sha256.digest()

#     # Convert the digest to a Base64-encoded string
#         signature = base64.b64encode(digest).decode('utf-8')

#         return signature

#     total_amount = 100
#     uuid_val = uuid.uuid4()
#     # Example usage:
#     secret_key = "8gBm/:&EnhH.1/q"
#     data_to_sign = f"{total_amount},{uuid_val},EPAYTEST"

#     result = genSha256(secret_key, data_to_sign)

#     print(uuid_val)
#     print(result)
#     print(total_amount)

#     return render(request,'book-reserve.html',{'signature':result, 'uuid_val':uuid_val})
