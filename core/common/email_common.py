from django.core.mail import EmailMessage

from django.template.loader import get_template

from api.settings import EMAIL_HOST_USER


class EmailCommon:

    def __init__(self, subject, receiver, template, body):
        self.__subject = subject
        self.__template = template
        self.__body = body
        self.__receiver = receiver
        self.__transmitter = EMAIL_HOST_USER

    def render_to_email_send(self):
        email_message = self.get_email_message()
        email_message.content_subtype = "html"
        email_message.send()

    def get_email_message(self):
        return EmailMessage(
            self.__subject,
            self.get_template(),
            self.__transmitter,
            self.__receiver
        )

    def get_template(self):
        return get_template(
            self.__template
        ).render(
            self.__body
        )

    def set_receiver(self, receiver):
        self.__receiver = receiver

    def set_transmitter(self, transmitter):
        self.__transmitter = transmitter
