from telethon import TelegramClient
import asyncio


# Получение настроек телеграм клиента из файла или из окружения.
def _get_config_from_file() -> dict:
    from . import config
    return {'API_ID': config.API_ID, 'API_HASH': config.API_HASH}

def _get_config_from_enviroment():
    pass


CONFIG = _get_config_from_enviroment() or _get_config_from_file()
CLIENTS: dict[str, TelegramClient] = {}
LOOP = asyncio.get_event_loop()
