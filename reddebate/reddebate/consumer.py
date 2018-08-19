# -*- coding: utf-8 -*-

from channels import Group
import threading
import random
import json
import logging
from resumen.models import Debate
from debate.models import Argumento, Postura, Participantes
from django.contrib.auth.models import User
from perfil.models import Perfil
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

log = logging.getLogger(__name__)

def actualiza_reputacion(id_usr, puntaje):
    perfil = Perfil.objects.get(user_id=id_usr)
    reputacion = perfil.reputacion + puntaje
    perfil.reputacion = reputacion
    perfil.save()

@channel_session_user_from_http
def ws_connect(message):
    # prefix, label, id = message['path'].decode('ascii').strip('/').split('/')
    grupo = message['path'].replace("/","")
    Group(grupo).add(message.reply_channel)
    Group(grupo).send({'accept':True})

@channel_session_user
def ws_receive(message):
    grupo = message['path'].replace("/","")
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if data:
        if set(data.keys()) == set(('titulo', 'descripcion', 'alias_c', 'largo', 'num_argumento', 'num_rebate', 'tipo_rebate', 'tipo_participacion', 'num_cambio_postura','date_fin', 'id_usuario_id', 'participantes')):
            data['id_usuario_id'] = message.user.id
            participantes = data['participantes']
            del data['participantes']
            m = Debate.objects.create(**data)
            if data['tipo_participacion']=='1':
                for participante in participantes:
                    usuario = User.objects.get(id=participante)
                    n = Participantes(id_usuario=usuario, id_debate=m)
                    n.save()
            actualiza_reputacion(message.user.id, 5)

        elif set(data.keys()) == set(('descripcion','alias_c','id_debate','postura','id_usuario_id')):
            debate = Debate.objects.get(id_debate=data['id_debate'])
            postura = Postura.objects.get(id_debate_id=debate.id_debate, id_usuario_id = message.user.id)
            data['id_usuario_id'] = message.user.id
            data['postura'] = postura.postura
            data['id_debate'] = debate
            m = Argumento.objects.create(**data)
            actualiza_reputacion(message.user.id, 3)

        elif set(data.keys()) == set(('postura','id_usuario','id_debate')):
            debate = Debate.objects.get(id_debate=data['id_debate'])
            data['id_usuario'] = message.user
            data['id_debate'] = debate
            m = Postura.objects.create(**data)
            actualiza_reputacion(message.user.id, 3)


        elif set(data.keys()) == set(('postura', 'id_debate', 'razon')):
            debate = Debate.objects.get(id_debate=data['id_debate'])
            data['id_debate'] = debate
            m = Postura.objects.get(id_debate_id=debate.id_debate, id_usuario_id=message.user.id)
            m.postura = data['postura']
            m.cambio_postura = data['razon']
            m.cuenta_cambios = m.cuenta_cambios + 1
            m.save()

        Group(grupo).send({'text': json.dumps(m.as_dict())})

@channel_session_user
def ws_disconnect(message):
    grupo = message['path'].replace("/","")
    Group(grupo).send({'close':True})
    Group(grupo).discard(message.reply_channel)
