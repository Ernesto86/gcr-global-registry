from advisers.models import Advisers, Managers
from security.models import User
from system.models import SysCountries

ecuador_country = SysCountries.objects.get(code="EC")

password_default = "admin123**"

user_manager = User.objects.create_user(
    username="managerdefault@gmail.com",
    first_name="Gerente Defecto",
    last_name="Gerente Defecto",
    email="managerdefault@gmail.com",
    password=password_default,
    is_active=False
)

manager_default = Managers.objects.create(
    country_origin_id=ecuador_country.id,
    country_residence_id=ecuador_country.id,
    user_id=user_manager.pkid,
    code='GERENTE-DEFAULT',
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
    is_active=False
)

adviser = Advisers.objects.create(
    country_origin_id=ecuador_country.id,
    country_residence_id=ecuador_country.id,
    manager_id=manager_default.id,
    user_id=user_adviser.pkid,
    code='ADVISER-DEFAULT',
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