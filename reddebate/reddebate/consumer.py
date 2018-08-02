from channels import Group
import threading
import random
import json
import logging
from resumen.models import Debate
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

# def sendmsg(num):
#     Group('stocks').send({'text':num})
#
# t = 0
# count = 0
# def periodic(sms):
#     global t;
#     # n = random.randint(10,200);
#     # sendmsg(str(n))
#     Group('stocks').send({'text':sms})
#     t = threading.Timer(5, periodic)
#     t.start()
#
# def ws_message(message):
#     global t
#     print(message.content['text'])
#     if ( message.content['text'] != 'stop'):
#         periodic(message.content['text'])
#     else:
#         t.cancel()
log = logging.getLogger(__name__)

@channel_session_user_from_http
def ws_connect(message):
    Group('stocks').add(message.reply_channel)
    Group('stocks').send({'accept':True})

@channel_session_user
def ws_receive(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if set(data.keys()) != set(('titulo', 'descripcion', 'alias_c', 'largo', 'num_rebate', 'date_fin', 'img', 'id_usuario_id')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('debate=%s de=%s',
            data['titulo'], message.user)
        data['id_usuario_id'] = message.user.id
        m = Debate.objects.create(**data)
        Group('stocks').send({'text': json.dumps(m.as_dict())})


@channel_session_user
def ws_disconnect(message):
    Group('stocks').send({'close':True})
    Group('stocks').discard(message.reply_channel)
