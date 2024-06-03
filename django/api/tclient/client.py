from telethon import TelegramClient
import threading
from . import qr_render


CLIENT: TelegramClient
THREAD: threading.Thread


# Получение настроек телеграм клиента из файла или из окружения.
def _get_config_from_file() -> dict:
    from . import config
    return {'API_ID': config.API_ID, 'API_HASH': config.API_HASH}

def _get_config_from_enviroment():
    pass

CONFIG = _get_config_from_enviroment() or _get_config_from_file()


async def _login(client: TelegramClient):
    pass


def login(phone_num: str):
    global CLIENT
    CLIENT = TelegramClient(f'session_{phone_num}', CONFIG['APP_id'], CONFIG['APP_HASH'])
    CLIENT.loop.run_until_complete(_login(CLIENT))


def logout():
    pass