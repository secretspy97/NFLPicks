from django.core.mail import send_mail
from django.core.mail import EmailMessage

def send_message(title, message, attachments):
    email = EmailMessage(
        title,
        message,
        'nflpicksconnor@example.com',
        ['nflpicksconnor@example.com'],
    )

    name, content, type = attachments
    email.attach(name, content, type)
    email.send()