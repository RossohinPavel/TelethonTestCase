from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import tclient


# Create your views here.
class LoginAPIView(APIView):
    """Авторизация пользователя."""
    def post(self, request):
        try:
            phone = str(request.data['phone'])
            if len(phone) != 11 or not phone.isdigit():
                raise ValueError('Incorrect number')

            return Response({'qr_link_url': request.build_absolute_uri(f'/qr/?phone={phone}')})

        except Exception as e:
            return Response({'error': str(e)})
