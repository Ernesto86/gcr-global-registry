import datetime
from django.shortcuts import redirect
from django.http import Http404
from core.constants import SYSTEM_LOGO, SYSTEM_NAME, SYSTEM_WEB

def addUserData(request, data):

    data['hoy'] = datetime.datetime.now()
    data['system_logo'] = SYSTEM_LOGO
    data['system_name'] = SYSTEM_NAME
    data['system_web'] = SYSTEM_WEB

    if request.user.is_authenticated:
        try:
            data['user'] = request.user
            data['user_grupos'] = request.user.groups.all()
        except:
            pass

    if request.method == 'GET' and 'gpid' in request.GET:
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
