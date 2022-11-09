from django.core.mail import EmailMessage
from django.template.loader import get_template
from api.settings import EMAIL_HOST_USER

def render_to_email_send(subject=None,body=None,transmitter=EMAIL_HOST_USER,receiver=[],template=None):
    email_message = EmailMessage(
        subject,
        get_template(template).render(body),
        transmitter,
        receiver
    )
    email_message.content_subtype = "html"
    email_message.send()
