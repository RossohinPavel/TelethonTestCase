from django.urls import path
from api import views
 
urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('qr/', views.get_qr)
]