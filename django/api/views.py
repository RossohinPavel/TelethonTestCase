from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from api import tclient


# Create your views here.
class PhoneCheckMixin(APIView):
    """Логика обработки ошибок"""
    def initial(self, request, *args, **kwargs):
        """Проверка корректности номера телефона в запросе"""
        if 'phone' in request.data:
            phone = request.data['phone'] = str(request.data['phone'])
            if len(phone) != 11 or not phone.isdigit():
                raise ValueError('Incorrect number')

        return super().initial(request, *args, **kwargs)
    
    def handle_exception(self, exc):
        """Обработка всех исключений"""
        return Response({'error': str(exc)})


class LoginAPIView(PhoneCheckMixin):
    """Авторизация пользователя."""
    def post(self, request):
        phone = request.data['phone']
        tclient.login(phone)
        return Response({'qr_link_url': request.build_absolute_uri(f'/qr/?phone={phone}')})



class LogoutAPIView(PhoneCheckMixin):
    """Логаут"""
    def post(self, request):
        phone = request.data['phone']
        return Response({'status': tclient.logout(phone)})


def get_qr(request):
    """Представление для странички с qr"""
    if request.method == 'GET' and 'phone' in request.GET:
        status, token = tclient.get_token(request.GET['phone'])
        data = {'status': status, 'token': token}
        return render(request, 'api/qr.html', context=data)

    return HttpResponseNotFound()
