from django.urls import path
from api import views
 
urlpatterns = [
    path('check/login', views.CheckAPIView.as_view()),
    path('login', views.LoginAPIView.as_view()),
    path('logout', views.LogoutAPIView.as_view()),
    path('messages', views.MessagesAPIView.as_view()),
    path('qr', views.get_qr),
    path('', views.WildberrysParserAPIView.as_view())
]