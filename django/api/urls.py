from django.urls import path
from api import views
 
urlpatterns = [
    path('login', views.LoginAPIView.as_view()),
    path('logout', views.LogoutAPIView.as_view()),
    path('check/login', views.CheckAPIView.as_view()),
    path('messages', views.MessagesAPIView.as_view()),
    path('qr', views.get_qr)
]