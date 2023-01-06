from django.contrib.auth.models import Group, Permission

from advisers.models import Managers, PaymentMethod, Advisers, AdvisersCommissions
from core.constants import CategoryModule, TypeModule
from security.models import Module, ModuleGrupPermissions, ModuleGrupCategory
from system.models import SysParameters
from transactions.models import OrderInstitutionQuotas

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// CATEGORIA PRINCIPAL //////////////////////////////////////////////////////////

query_mdc = ModuleGrupCategory.objects.create(
    name="CONSULTAS",
)
registry_mdc = ModuleGrupCategory.objects.create(
    name="REGISTROS",
    is_out=True
)
maintenance_mdc = ModuleGrupCategory.objects.create(
    name="MANTENIMIENTOS",
)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// GRUPO ////////////////////////////////////////////////////////////////////////

accionistas = Group.objects.create(
    name="Accionistas"
)
asesores = Group.objects.create(
    name="Asesores"
)
directivos = Group.objects.create(
    name="Directivos"
)
gerentes = Group.objects.create(
    name="	Gerentes"
)
instituciones = Group.objects.create(
    name="Instituciones"
)
solicitantes = Group.objects.create(
    name="	Solicitantes"
)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// MODULOS //////////////////////////////////////////////////////////////////////

module_common = {
    "category_module": CategoryModule.PROCESSES,
    "type_module": TypeModule.MENU,
    "visible": True
}

module = Module.objects.create(
    url='/advisers/advisers',
    name='Asesores',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=gerentes.id,
    module_id=module.id
)
for p in Permission.objects.filter(content_type__model=Advisers._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/security/change-password',
    name='Cambiar contraseña',
    **module_common
)

module = Module.objects.create(
    url='/advisers/advisers-commissions',
    name='Comisiones asesores',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=gerentes.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=AdvisersCommissions._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/advisers/managers-commissions',
    name='Comisiones gerentes',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=directivos.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=Managers._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/institutions/configuration',
    name='Configuracion de datos',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=solicitantes.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("view_institutions", "add_institutions", "change_institutions",)):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/advisers/dashboard-admin',
    name='Dashboard admin',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id,
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=directivos.id,
    module_id=module.id,
)

module = Module.objects.create(
    url='/advisers/dashboard-advisor',
    name='Dashboard asesores',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=asesores.id,
    module_id=module.id,
)
module_group_permissions.permissions.add()

module = Module.objects.create(
    url='/advisers/dashboard-manager',
    name='Dashboard gerente',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=gerentes.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("dashboard_managers",)):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/advisers/managers',
    name='Gerentes',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=directivos.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=Managers._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/students/students-registers',
    name='Ingreso de registros',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=instituciones.id,
    module_id=module.id,
)

module = Module.objects.create(
    url='/institutions/register-status',
    name='Instituciones',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=directivos.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("view_institutions",)):
    module_group_permissions.permissions.add(p)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=gerentes.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("view_institutions",)):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/transactions/shopping-cart',
    name='Obten mas registros',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=instituciones.id,
    module_id=instituciones.id,
)
for p in Permission.objects.filter(content_type__model=OrderInstitutionQuotas._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/security/organizador-registros',
    name='Organiador de registros',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=instituciones.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=('view_studentregisters',)):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/advisers/advisers-commissions-payment',
    name='Pagos de comisiones',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id,
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=directivos.id,
    module_id=module.id,
)

module = Module.objects.create(
    url='/advisers/adviser-profile/update',
    name='Perfil asesor',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=asesores.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("change_advisers",)):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/advisers/manager-profile/update',
    name='Perfil gerente',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=gerentes.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=Managers._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/institutions/institutions/view',
    name='Instituciones asesor',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=asesores.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("view_institutions",)):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/system/sys-parameters',
    name='Parametros',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=directivos.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=SysParameters._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/advisers/period-commissions/update',
    name='Periodo comisiones',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=directivos.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("change_periodcommissions",)):
    module_group_permissions.permissions.add(p)

module = Module.objects.create(
    url='/advisers/payment-method',
    name='Tarjetas',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=asesores.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=PaymentMethod._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)
