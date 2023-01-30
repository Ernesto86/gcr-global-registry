from decimal import Decimal

from core.constants import TYPE_REGISTER_CODE_CUARTO_NIVEL, TYPE_REGISTER_CODE_TERCER_NIVEL, \
    TYPE_REGISTER_CODE_SEGUNDO_NIVEL, TYPE_REGISTER_CODE_PRIMER_NIVEL
from institutions.models import InsTypeRegistries
from students.models import Certificates


class FillDataInstitution:
    def start(self):
        type_registries = InsTypeRegistries.objects.create(
            code=TYPE_REGISTER_CODE_CUARTO_NIVEL,
            name="CUARTO NIVEL",
            detail="POSTGRADO Y DOCTORADO",
            color="warning",
            price=Decimal("100.00"),
        )

        Certificates.objects.create(
            type_registry_id=type_registries.id
        )

        InsTypeRegistries.objects.create(
            code=TYPE_REGISTER_CODE_TERCER_NIVEL,
            name="TERCER NIVEL",
            detail="Registro de Títulos de Pregrado y Especializaciones",
            color="success",
            price=Decimal("50.00"),
        )

        InsTypeRegistries.objects.create(
            code=TYPE_REGISTER_CODE_SEGUNDO_NIVEL,
            name="SEGUNDO NIVEL",
            detail="Registro de Certificados de Executive Education",
            color="danger",
            price=Decimal("10.00"),
        )

        InsTypeRegistries.objects.create(
            code=TYPE_REGISTER_CODE_PRIMER_NIVEL,
            name="PRIMER NIVEL",
            detail="Registro de Certificados de Educación Continua",
            color="primary",
            price=Decimal("5.00"),
        )

        fill_data_institution_py = 1
