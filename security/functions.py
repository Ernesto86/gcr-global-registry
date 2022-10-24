import datetime
from django.shortcuts import redirect
from django.http import Http404
from core.constants import LOGO_SISTEMA, NOMBRE_SISTEMA, SISTEMA_PAGINA_WEB


def addUserData(request, data):
    if request.method == 'GET':
        data['hoy'] = datetime.datetime.now()
        data['system_logo'] = LOGO_SISTEMA
        data['system_web'] = SISTEMA_PAGINA_WEB
        data['system_name'] = NOMBRE_SISTEMA
        try:
            data['user'] = request.user
            data['user_grupos'] = request.user.groups.all()
        except:
            pass

        if 'gpid' in request.GET:
            grupo_id = int(request.GET['gpid'])
            try:
                grupos = request.user.groups.filter(id=grupo_id)
                if grupos.exists():
                    data['grupo'] = grupo = request.user.groups.filter(id=grupo_id)[0]
                    request.session['grupoid'] = grupo.id
                    data['modulos_grupos'] = grupo.segmodulogrupo_set.all().order_by('prioridad')
            except:
                raise Http404
                return redirect('/', error='error messsage')

        elif not 'grupoid' in request.session:
            try:
                if len(data['user_grupos']):
                    data['grupo'] = grupo = data['user_grupos'][0]
                    request.session['grupoid'] = grupo.id
                    data['modulos_grupos'] = grupo.segmodulogrupo_set.all().order_by('prioridad')
            except:
                pass
        else:
            try:
                data['grupo'] = grupo = request.user.groups.get(pk=request.session['grupoid'])
                data['modulos_grupos'] = grupo.segmodulogrupo_set.all().order_by('prioridad')
            except:
                pass
