from institutions.models import InsTypeRegistries
from security.models import User
from students.models import StudentRegisters
from transactions.models import InstitutionQuotesTypeRegister


class OrganizadorRegistrosManager:
    def __init__(self, user: User):
        self.__user = user

    def get_type_registries_list(self):
        type_registries_list = []

        for ins_type_registries in InsTypeRegistries.objects.all().order_by('code'):
            registers_level = StudentRegisters.objects.filter(
                type_register_id=ins_type_registries.id,
                institution_id=self.__user.institution_id,
                deleted=False
            ).count()

            if registers_level:
                type_registries_list.append(
                    {
                        "id": ins_type_registries.id,
                        "name": ins_type_registries.name,
                        "detail": ins_type_registries.detail,
                        "color": ins_type_registries.color,
                        "registers_level_count": registers_level,
                    }
                )
        return type_registries_list

    def get_type_registries_count_available_list(self):
        type_registries_list = []

        for ins_type_registries in InsTypeRegistries.objects.all().order_by('code'):
            try:
                quotas_balance = InstitutionQuotesTypeRegister.objects.get(
                    institution_id=self.__user.institution_id,
                    type_register_id=ins_type_registries.id
                ).quotas_balance
            except InstitutionQuotesTypeRegister.DoesNotExist:
                continue
            except Exception as ex:
                continue

            type_registries_list.append(
                {
                    "id": ins_type_registries.id,
                    "name": ins_type_registries.name,
                    "detail": ins_type_registries.detail,
                    "color": ins_type_registries.color,
                    "quotas_balance": quotas_balance,
                }
            )
        return type_registries_list
