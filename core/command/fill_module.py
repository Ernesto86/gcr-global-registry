from django.contrib.auth.models import Group, Permission

from advisers.models import PaymentMethod, AdvisersCommissions, PeriodCommissions
from core.command.fill_country import load_countries
from core.constants import CategoryModule, TypeModule, GROUP_NAME_SOLICITANTES, GROUP_NAME_INSTITUTION, \
    GROUP_NAME_MANAGER, GROUP_NAME_DIRECTIVO, GROUP_NAME_ADVISER, GROUP_NAME_ACCIONISTA
from security.models import Module, ModuleGrupPermissions, ModuleGrupCategory
from system.models import SysParameters
from transactions.models import OrderInstitutionQuotas

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// LOAD COUNTRY /////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

load_countries()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////// COMMISSIONS /////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

PeriodCommissions.objects.create()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// LOAD DATA DEFAULT ////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# TODO: los gerentes y asesores dependen de load country
from core.command.fill_data_institution import *

print(fill_data_institution_py)

# TODO: los gerentes y asesores dependen de load country
from core.command.fill_adviser_manager_default import *

print(fill_adviser_manager_default)

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
    name=GROUP_NAME_ACCIONISTA
)
asesores = Group.objects.create(
    name=GROUP_NAME_ADVISER
)
directivos = Group.objects.create(
    name=GROUP_NAME_DIRECTIVO
)
gerentes = Group.objects.create(
    name=GROUP_NAME_MANAGER
)
instituciones = Group.objects.create(
    name=GROUP_NAME_INSTITUTION
)
solicitantes = Group.objects.create(
    name=GROUP_NAME_SOLICITANTES
)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// MODULOS //////////////////////////////////////////////////////////////////////

module_common = {
    "category_module": CategoryModule.PROCESSES,
    "type_module": TypeModule.MENU,
    "visible": True
}

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

module = Module.objects.create(
    url='/security/change-password',
    name='Cambiar contraseña',
    **module_common
)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

module = Module.objects.create(
    url='/security/users',
    name='Directivos',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id
)
for p in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=Managers._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=instituciones.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("view_institutions", "add_institutions", "change_institutions",)):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=Managers._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
for p in Permission.objects.filter(codename__in=("add_studentregisters",)):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("view_institutions",)):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

module = Module.objects.create(
    url='/transactions/shopping-cart',
    name='Obten mas registros',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=instituciones.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=OrderInstitutionQuotas._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

module = Module.objects.create(
    url='/security/organizador-registros',
    name='Organizador de registros',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=instituciones.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=('view_studentregisters',)):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
# module_group_permissions = ModuleGrupPermissions.objects.create(
#     main_category_id=registry_mdc.id,
#     group_id=directivos.id,
#     module_id=module.id,
# )

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

module = Module.objects.create(
    url='/system/sys-parameters',
    name='Parametros',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id,
)
for p in Permission.objects.filter(content_type__model=SysParameters._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

module = Module.objects.create(
    url='/advisers/period-commissions/update',
    name='Periodo comisiones',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=accionistas.id,
    module_id=module.id,
)
for p in Permission.objects.filter(codename__in=("change_periodcommissions",)):
    module_group_permissions.permissions.add(p)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////// PARAMETERS //////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


SysParameters.objects.create(
    code="RIC",
    name="CODIGO INTERNACIONAL DE CERTIFICADO",
    value="2060",
    status=True,
)

SysParameters.objects.create(
    code="FER",
    name="FECHA DE EXPIRACION DE REGISTRO",
    value="760",
    status=True,
)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////// USER ////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

user = User.objects.create_superuser(
    username='admin',
    first_name='Jefferson',
    last_name='Berrones',
    email='admin@gmail.com',
    password="admin123**",
    is_staff=True,
    is_superuser=True,
    is_active=True,
)

user.groups.add(accionistas)
user.groups.add(asesores)
user.groups.add(directivos)
user.groups.add(gerentes)
user.groups.add(instituciones)
user.groups.add(solicitantes)
