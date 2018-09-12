from resumen.models import Debate
from debate.models import Notificacion, Argumento

def listado_notificacion(request):
    notificaciones = Notificacion.objects.all().order_by('-id')
    notificacion_usr = []
    for n in notificaciones:
        if n.id_usuario_id == request.user.id:
            notificacion_usr.append(n)
    return {'notificaciones': notificacion_usr}
