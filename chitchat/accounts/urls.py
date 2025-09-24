from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.registration,name='regpage'),

  
    path('login/',views.loginuser,name='log'),
    path('send/', views.bodymessage, name='bodymessage'),
]
