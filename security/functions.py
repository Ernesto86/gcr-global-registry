import datetime
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
            user_grups  = request.user.groups.all()
        except:
            pass

        if 'gpid' in request.GET:
            try:
                grup = request.user.groups.get(pk=int(request.GET.get('gpid')))
            except:
                raise Http404

        elif not 'grup_id' in request.session:
            grup = user_grups.first()
        else:
            grup = user_grups.filter(pk=request.session['grup_id']).first()

        try:
            data['user_grups'] = user_grups
            if grup is not None:
                data['grup'] = grup
                request.session['grup_id'] = grup.id
                data['module_grup_categories'] = grup.modulegruppermissions_set.filter(
                        module__visible=True
                    ).order_by(
                        'main_category_id', 'main_category__is_out' , 'main_category__name'
                    ).distinct('main_category_id')
        except:
            pass

        data['title'] = "Home"
        data['active'] = "index"
        # data['bodyClass'] = "uikit"
        data['isTour'] = False
        data['isFlatpickr'] = True
        data['isBanner'] = True
        data['isSidebar'] = True
        data['isNavbar'] = True
        data['dev'] = True
        data['version'] = '2.0.0'

        data['isSidebar'] = True
        data['isNavbar'] = True
        data['isBanner'] = True
        data['isPageContainer'] = True
        data['title'] = "index"
        data['isFlatpickr'] = True
        data['isNoUISlider'] = True
        data['active'] = "index"
        # data['bodyClass'] = "uikit"
        # data['isFlatpickr'] = True


