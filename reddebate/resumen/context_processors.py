# coding=utf-8
from resumen.models import Debate
from debate.models import Notificacion, Argumento
from datetime import *
import pytz

def listado_notificacion(request):
    utc=pytz.UTC
    notificaciones = Notificacion.objects.all().order_by('-fecha')
    notificacion_usr = []
    ahora = datetime.now().replace(tzinfo=utc)
    for n in notificaciones:
        if n.id_usuario_id == request.user.id:
            d = ahora - n.fecha.replace(tzinfo=utc)
            if d.days == 0:
                hr = d.seconds//3600
                min = (d.seconds % 3600) // 60
                if hr == 0:
                    if min <= 1: msj = "Ahora"
                    else: msj = "Hace "+str(min)+" minutos"
                elif hr == 1: msj = "Hace 1 hora"
                elif hr > 1: msj = "Hace "+str(hr)+" horas"
            elif d.days == 1: msj = "Hace "+str(d.days)+" día"
            elif d.days < 4: msj = "Hace "+str(d.days)+" días"
            else: msj = n.fecha.strftime('%d/%m/%Y')
            notificacion_usr.append({'object':n, 'tiempo': msj})
    return {'notificaciones': notificacion_usr}
