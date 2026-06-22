from django.shortcuts import render
from datetime import date

# Create your views here.
def index_view (request):
    my_info = {
        'birth_date': date(1996, 10, 24),
        'name': 'محمد اسکندرلو',
        'email': 'Mohammad.eska34@gmail.com',
        'location': 'تهران'
    }
    return render(request , 'website/index.html', my_info )

def ai_chat_view (request):
    ai_chat_view = {'name': 'محمد اسکندرلو' , 'phone_number' : '+989337315709' , 'email': 'mohammad.eska34@gmail.com'}
    return render(request , 'website/ai_chat_view.html',ai_chat_view)