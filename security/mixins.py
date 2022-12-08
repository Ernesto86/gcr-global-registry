from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages


class ModuleMixin(object):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_superuser:
                return super().get(request, *args, **kwargs)

            user.set_group_session()
            group = user.get_group_session()
            group_module = group.modulegruppermissions_set.filter(
                module__deleted=False,
                module__url=request.path,
                module__visible=True,
            ).first()
            if group_module is not None:
                request.session['module_id'] = group_module.module.id
                return super().get(request, *args, **kwargs)
        except Exception as ex:
            pass
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return redirect('home')


class PermissionMixin(object):
    permission_required = None

    def get_permissions(self):
        permissions = []
        if isinstance(self.permission_required, str):
            permissions.append(self.permission_required)
        else:
            permissions = list(self.permission_required)
        return permissions

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_superuser:
                return super().get(request, *args, **kwargs)

            user.set_group_session()
            if 'group_id' in request.session:
                group = user.get_group_session()
                permissions = self.get_permissions()

                for permission in permissions:

                    if not group.modulegruppermissions_set.filter(permissions__codename=permission).exists():
                        messages.error(request, 'No tiene permiso para ingresar a este módulo')
                        return redirect('home')

                modulegruppermission = group.modulegruppermissions_set.filter(
                    permissions__codename=permissions[0]
                ).first()
                if modulegruppermission is not None:
                    request.session['module_id'] = modulegruppermission.module.id
                return super().get(request, *args, **kwargs)
        except Exception as ex:
            return redirect('login')
