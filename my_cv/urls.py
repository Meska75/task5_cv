from django.urls import path
from my_cv.views import index_view , ai_chat_view

app_name = 'my_cv'

urlpatterns = [
    path('',index_view, name ='index'),
    path('ai_chat_view', ai_chat_view , name = 'ai_chat_view')
]
