from ..logs import logger
from ..models import CustomUser
from .CheckWeightLogs import CheckWeightLogs

# Класс активирует аккаунт, который перешел по ссылке

class ActivateCodeForm():
    def __init__(self, random_code):
        profile = CustomUser.objects.get(activate_code=random_code)
        profile.is_active = True
        profile.save()
        CheckWeightLogs
        logger.debug("Пользователь '{}'активирован".format(profile))