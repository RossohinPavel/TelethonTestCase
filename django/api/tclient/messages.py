from .client import CLIENTS, LOOP
from threading import Thread
import os

if not os.path.exists('Messages'):
    os.mkdir('Messages')


def _convert(msg) -> dict:
    """Конвертирует объекты в нужный формат"""
    return {'username': msg.sender.username, 'is_self': msg.out, 'message_text': msg.message}


def _save(msgs):
    """Сохранение сообщений"""
    if not isinstance(msgs, list):
        msgs = [msgs]

    chat = msgs[0].sender.username
    with open(f'Messages/{chat}', 'w', encoding='utf-8') as file:
        g = (f'{m.sender.username}: {m.message}\n' for m in msgs)
        file.writelines(g)


def get_messages(phone: str, uname: str, save: bool):
    """Получает сообщения пользователя"""
    client = CLIENTS[phone]
    msgs = LOOP.run_until_complete(client.get_messages(uname, 50))
    if msgs is None:
        raise Exception('No messages')
    
    if save:
        Thread(target=_save, args=(msgs, )).start()

    if isinstance(msgs, list):
        converted_msgs = (_convert(m) for m in msgs)
    else:
        converted_msgs = (_convert(msgs), )
    
    return converted_msgs


def send_message(text: str, from_phone: str, username: str):
    """Посылает сообщение пользователю"""
    client = CLIENTS[from_phone]
    r = LOOP.run_until_complete(client.send_message(username, text))
