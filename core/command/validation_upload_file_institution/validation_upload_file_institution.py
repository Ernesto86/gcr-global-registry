from datetime import datetime, timedelta

from django.db.models import Q

from core.common.email_common import EmailCommon
from core.constants import RegistrationStatus, SYSTEM_NAME
from institutions.models import Institutions
from security.models import User
from system.models import SysParameters


class ValidationUploadFileInstitution:
    days_after_to_send_email = 5

    def __init__(self):
        self.__sys_parameter = SysParameters.get_sys_parameter_date_limit_of_approve_code()
        self.__days_limit = int(self.__sys_parameter.value)
        self.__date_today = datetime.now().date()
        self.__user_id_list = []
        self.__user_id_to_send_email_list = []

    def run(self):
        users = User.objects.select_related(
            'institution'
        ).filter(
            Q(institution__registration_status=RegistrationStatus.PENDIENTE) | Q(institution__isnull=True),
            is_handle_institution=True
        )

        for user in users:

            if not self.has_complete_files(user):

                date_limit = self.get_date_limit(user)

                date_to_send_email = date_limit - timedelta(
                    days=ValidationUploadFileInstitution.days_after_to_send_email)

                is_send_email = self.is_send_email(date_to_send_email, date_limit)

                if is_send_email:
                    self.__user_id_to_send_email_list.append(user.pkid)

                if self.date_limit_is_exceeded(date_limit):
                    self.__user_id_list.append(user.pkid)

        self.send_email(users)
        self.delete_user(users)

    def has_complete_files(self, user):

        if user.institution is None:
            return False

        return Institutions.has_complete_files(user.institution)

    def is_send_email(self, date_to_send_email, date_limit):

        if date_to_send_email <= self.__date_today < date_limit:
            return True

        return False

    def get_date_limit(self, user):
        return user.create_at.date() + timedelta(days=self.__days_limit)

    def date_limit_is_exceeded(self, date_limit):
        return self.__date_today > date_limit

    def send_email(self, users_query_set):

        if len(self.__user_id_to_send_email_list) > 0:

            email_list = [x.email for x in users_query_set.filter(pkid__in=self.__user_id_to_send_email_list)]

            try:
                EmailCommon(
                    subject="Señor administrador",
                    receiver=email_list,
                    template='email/remember_create_fill_institution_user.html',
                    body={
                        'system_name': SYSTEM_NAME
                    },
                ).render_to_email_send()
            except Exception as e:
                pass

    def delete_user(self, users_query_set):
        if len(self.__user_id_list) > 0:

            institution_delete_id_list = []

            for user in users_query_set:

                if user.institution is not None:
                    institution_delete_id_list.append(user.institution_id)

            User.objects.filter(pkid__in=self.__user_id_list).delete()
            Institutions.objects.filter(id__in=institution_delete_id_list).delete()
