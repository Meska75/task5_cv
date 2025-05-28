from django.shortcuts import render

# Create your views here.
def index_view (request):
    return render(request , 'website/index.html')

def contact_view (request):
    contact_info = {'name': 'محمد اسکندرلو' , 'phone_number' : '+989337315709' , 'email': 'mohammad.eska34@gmail.com'}
    return render(request , 'website/contact.html',contact_info)