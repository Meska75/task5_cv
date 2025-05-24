from django.urls import path
from my_cv.views import index_view


app_name = 'my_cv'

urlpatterns = [
    path('',index_view),
]
