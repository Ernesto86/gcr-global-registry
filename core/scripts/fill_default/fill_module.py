from django.contrib.auth.models import Group, Permission

from advisers.models import PaymentMethod, AdvisersCommissions, PeriodCommissions, Managers, Advisers

from core.constants import CategoryModule, TypeModule, GROUP_NAME_SOLICITANTES, GROUP_NAME_INSTITUTION, \
    GROUP_NAME_MANAGER, GROUP_NAME_DIRECTIVO, GROUP_NAME_ADVISER, GROUP_NAME_ACCIONISTA, SYS_PARAMETER_CODE, \
    SYS_PARAMETER_DATE_EXPIRY_OF_REGISTER_CODE, SYS_PARAMETER_DATE_LIMIT_OF_APPROVE, CODE_MANAGER_DEFAULT, \
    CODE_ADVISER_DEFAULT
from core.models import SystemSettings
from core.scripts.fill_default.fill_country import FillCountry
from security.models import Module, ModuleGrupPermissions, ModuleGrupCategory, User
from system.models import SysParameters, AcademicLevel, SysCountries
from transactions.models import OrderInstitutionQuotas

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// LOAD COUNTRY /////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

FillCountry().run()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////// COMMISSIONS /////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

PeriodCommissions.objects.create()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////// LOAD DATA DEFAULT ////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

SystemSettings.objects.create()

# TODO: los gerentes y asesores dependen de load country
from core.scripts.fill_default.fill_data_institution import *

print(fill_data_institution_py)

# TODO: los gerentes y asesores dependen de load country
# from core.scripts.fill_default.fill_adviser_manager_default import *
#
# print(fill_adviser_manager_default)

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
    url='/security/academic-levels',
    name='Niveles academicos',
    **module_common
)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=gerentes.id,
    module_id=module.id
)
for p in Permission.objects.filter(content_type__model=AcademicLevel._meta.label.split('.')[1].lower()):
    module_group_permissions.permissions.add(p)
module_group_permissions = ModuleGrupPermissions.objects.create(
    main_category_id=registry_mdc.id,
    group_id=asesores.id,
    module_id=module.id
)
for p in Permission.objects.filter(content_type__model=AcademicLevel._meta.label.split('.')[1].lower()):
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
    name='Organ. de registros',
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
    code=SYS_PARAMETER_CODE,
    name="CODIGO INTERNACIONAL DE CERTIFICADO",
    value="2060",
    status=True,
)

SysParameters.objects.create(
    code=SYS_PARAMETER_DATE_EXPIRY_OF_REGISTER_CODE,
    name="FECHA DE EXPIRACION DE REGISTRO",
    value="760",
    status=True,
)

SysParameters.objects.create(
    code=SYS_PARAMETER_DATE_LIMIT_OF_APPROVE,
    name="FCHA LIMITE PARA FECHA DE PROVACION",
    value="20",
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

ecuador_country = SysCountries.objects.get(code="EC")

password_default = "admin123**"

user_manager = User.objects.create_user(
    username="managerdefault@gmail.com",
    first_name="Gerente Defecto",
    last_name="Gerente Defecto",
    email="managerdefault@gmail.com",
    password=password_default,
    is_active=True
)

user_manager.groups.add(gerentes)

manager_default = Managers.objects.create(
    country_origin_id=ecuador_country.id,
    country_residence_id=ecuador_country.id,
    user_id=user_manager.pkid,
    code=CODE_MANAGER_DEFAULT,
    names="Gerente Defecto Gerente Defecto",
    last_name="Gerente Defecto",
    first_name="Gerente Defecto",
    dni="1234567890",
    address="Ciudad Ecuador",
    code_postal="1234",
    telephone="1234567890",
    cell_phone="1234567890",
    email="managerdefault@gmail.com",
    email_alternate="managerdefault@gmail.com",
)

user_adviser = User.objects.create_user(
    username="adviserdefault@gmail.com",
    first_name="Asesor defecto",
    last_name="Asesor defecto",
    email="adviserdefault@gmail.com",
    password=password_default,
    is_active=True
)

user_adviser.groups.add(asesores)

adviser = Advisers.objects.create(
    country_origin_id=ecuador_country.id,
    country_residence_id=ecuador_country.id,
    manager_id=manager_default.id,
    user_id=user_adviser.pkid,
    code=CODE_ADVISER_DEFAULT,
    names="Asesor Defector Asesor Defector",
    last_name="Asesor Defector",
    first_name="Asesor Defector",
    dni="1234567890",
    address="1234567890",
    code_postal="1234",
    telephone="1234567890",
    cell_phone="1234567890",
    email="adviserdefault@gmail.com",
    email_alternate="adviserdefault@gmail.com",
)

adviser.create_commission()

fill_adviser_manager_default = 1
