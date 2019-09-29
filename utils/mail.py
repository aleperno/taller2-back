import os
from sendgrid import SendGridAPIClient, Personalization, Substitution
from sendgrid.helpers.mail import Mail

TEMPLATE_ID = 'd-3ea9b70314594c52b3b359d84de0601f'
API_KEY = os.environ.get('SENDGRID_API_KEY')

TEMPLATE = r"""Has solicitado resetear tu contraseña, tu token es <strong>{token}</strong>.
               Expira el {expires}."""

message_orig = Mail(
    from_email='foodie@foodie.com',
    to_emails='alepernin@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')


message_template = Mail(
    from_email='foodie@foodie.com',
    to_emails='alepernin@gmail.com',
)
message_template.template_id = TEMPLATE_ID


def personalize():
    personalization = Personalization()
    token = Substitution('token', 'abc1234')
    personalization.add_substitution(token)
    return personalization


# message_template.add_personalization(personalize())

message_template.dynamic_template_data = {
    'token': 'esteesuntokendelaputamadre',
    'Sender_Name': 'Foodie S.R.L'
}

"""
try:
    sg = SendGridAPIClient(API_KEY)
    response = sg.send(message_template)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
"""


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
