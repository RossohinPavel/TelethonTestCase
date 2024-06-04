from .client import CLIENTS, TelegramClient, CONFIG, LOOP
import threading


# статусы возрата для чек ф-ии
ERROR = 'error'
LOGINED = 'logined'
WAITTING = 'waiting_qr_login'


async def _await_client(phone: str) -> TelegramClient:
    """Создает объект клиента и конектит его."""   
    c = CLIENTS[phone] = TelegramClient(phone, CONFIG['API_ID'], CONFIG['API_HASH'])

    if not c.is_connected():
        await c.connect()

    return c


def check(phone: str) -> str:
    """Проверка статуса логина."""
    if phone not in CLIENTS:
        return ERROR
    
    client = CLIENTS[phone]
    if LOOP.run_until_complete(client.is_user_authorized()):
        return LOGINED
    
    return WAITTING


def login(phone: str) -> tuple[str, str|None]:
    """Логин пользователя по переданному телефону. Возвращает телеграм-токен."""
    status = check(phone)

    if status == ERROR:
        client = LOOP.run_until_complete(_await_client(phone))
        status = WAITTING
    else:
        client = CLIENTS[phone]

    qr_token = None
    if status == WAITTING:
        qr_login = LOOP.run_until_complete(client.qr_login())
        qr_token = qr_login.url
        # Будем ждать скан qr в фоне
        t = threading.Thread(
            target=LOOP.run_until_complete, 
            args=(qr_login.wait(300), )
        )
        t.start()

    return status, qr_token


def logout():
    pass