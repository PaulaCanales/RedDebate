from resumen.models import Debate
from debate.models import Notificacion

def listado_notificacion(request):
    notificaciones = Notificacion.objects.all()
    notificacion_usr = []
    for n in notificaciones:
        deb_usr=Debate.objects.get(id_debate = n.id_debate.id_debate).id_usuario
        if deb_usr == request.user:
            notificacion_usr.append(n)
    print("notificacion_usr")
    print(notificacion_usr)
    return {'notificaciones': notificacion_usr}
