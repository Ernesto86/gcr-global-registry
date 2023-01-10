from decimal import Decimal

from institutions.models import InsTypeRegistries
from students.models import Certificates

type_registries = InsTypeRegistries.objects.create(
    code="001",
    name="CUARTO NIVEL",
    detail="POSTGRADO Y DOCTORADO",
    color="warning",
    price=Decimal("100.00"),
)

Certificates.objects.create(
    type_registry_id=type_registries.id
)

InsTypeRegistries.objects.create(
    code="002",
    name="TERCER NIVEL",
    detail="Registro de Títulos de Pregrado y Especializaciones",
    color="success",
    price=Decimal("50.00"),
)

InsTypeRegistries.objects.create(
    code="003",
    name="SEGUNDO NIVEL",
    detail="Registro de Certificados de Executive Education",
    color="danger",
    price=Decimal("10.00"),
)

InsTypeRegistries.objects.create(
    code="004",
    name="PRIMER NIVEL",
    detail="Registro de Certificados de Educación Continua",
    color="primary",
    price=Decimal("5.00"),
)

fill_data_institution_py = 1
