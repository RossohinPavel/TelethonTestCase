from .client import CLIENTS, TelegramClient, CONFIG, LOOP
import threading


# статусы возрата для чек ф-ии
ERROR = 'error'
LOGINED = 'logined'
WAITTING = 'waiting_qr_login'


async def _await_client(phone: str):
    """Создает объект клиента и конектит его."""   
    c = CLIENTS[phone] = TelegramClient(phone, CONFIG['API_ID'], CONFIG['API_HASH'])
    await c.connect()


def check(phone: str) -> str:
    """Проверка статуса логина."""
    if phone not in CLIENTS:
        return ERROR
    
    client = CLIENTS[phone]
    if LOOP.run_until_complete(client.is_user_authorized()):
        return LOGINED
    
    return WAITTING


def login(phone: str):
    """Логин пользователя по переданному телефону"""
    if check(phone) == ERROR:
        LOOP.run_until_complete(_await_client(phone))


def get_token(phone: str) -> tuple[str, str|None]:
    """
        Возвращает статус подключения и токен, если ожидается авторизация.
        Инициализирует поток ожидания скана qr кода.
    """
    status = check(phone)
    qr_token = None

    if status == WAITTING:
        qr_login = LOOP.run_until_complete(CLIENTS[phone].qr_login())
        qr_token = qr_login.url
        # Будем ждать скан qr в фоне 5 минут
        t = threading.Thread(
            target=LOOP.run_until_complete, 
            args=(qr_login.wait(120), )
        )
        t.start()

    return status, qr_token


def logout(phone: str) -> str:
    """Логаут))"""
    if phone not in CLIENTS:
        return ERROR
    
    LOOP.run_until_complete(CLIENTS[phone].log_out())
    return 'logout success'
