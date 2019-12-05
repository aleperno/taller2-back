import os
from sendgrid import SendGridAPIClient, Personalization, Substitution
from sendgrid.helpers.mail import Mail


API_KEY = os.environ.get('SENDGRID_API_KEY')

TEMPLATE = r"""Has solicitado resetear tu contraseña, tu token es <strong>{token}</strong>.
               Expira el {expires}."""


def send_token_to_mail(token, email, expiration):
    html_content = TEMPLATE.format(token=token, expires=expiration)
    mail = Mail(
        from_email='security@foodie.com',
        to_emails=email,
        subject='Password Reset',
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(API_KEY)
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
