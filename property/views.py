from django.shortcuts import render

# Create your views here.
def Property_list(request):
    return render(request, 'property.html')