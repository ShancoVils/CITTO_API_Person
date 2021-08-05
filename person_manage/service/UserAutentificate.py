from django.core.mail import send_mail
from django.conf import settings
from .Hepler_class import Helper as hepl
from ..logs import logger
from ..models import CustomUser

# Класс реализует отправку письма на указанную почту со ссылкой на активацию аккаунта

class SendAuthEmail():
    def __init__(self,email, code):
        try:
            message ="Ссылка для подтверждения аккаунта http://127.0.0.1:8000/confirm_form/"+code
            send_mail('Код подтверждения', message,
            settings.EMAIL_HOST_USER,
            [email], 
            fail_silently=False) 
            hepl.log_check()
            logger.debug("Письмо подтверждение отправлено на '{}' ".format(email))
        except:
            logger.error("Почты '{}' не существует ".format(email))

# Класс активирует аккаунт, который перешел по ссылке

class ActivateCodeForm():
    def __init__(self, random_code):
        profile = CustomUser.objects.get(activate_code=random_code)
        profile.is_active = True
        profile.save()
        hepl.log_check()
        logger.debug("Пользователь '{}'активирован".format(profile))