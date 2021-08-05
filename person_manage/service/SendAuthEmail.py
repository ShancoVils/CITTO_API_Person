from django.core.mail import send_mail
from django.conf import settings
from .CheckWeightLogs import CheckWeightLogs
from ..logs import logger
# Класс реализует отправку письма на указанную почту со ссылкой на активацию аккаунта

class SendAuthEmail():
    def __init__(self,email, code):
        try:
            message ="Ссылка для подтверждения аккаунта http://127.0.0.1:8000/confirm_form/"+code
            send_mail('Код подтверждения', message,
            settings.EMAIL_HOST_USER,
            [email], 
            fail_silently=False) 
            CheckWeightLogs
            logger.debug("Письмо подтверждение отправлено на '{}' ".format(email))
        except:
            logger.error("Почты '{}' не существует ".format(email))