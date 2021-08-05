from rest_framework.views import APIView
from rest_framework.generics import  get_object_or_404
from ..models import CustomUser
from ..serializers import CustomUserSerializer
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from ..logs import logger
from .Hepler_class import Helper as help
from .UserAutentificate import SendAuthEmail
# Метод получает все данные о пользователях

class PersonView(APIView):


    def get_person_data():
        person_api = CustomUser.objects.all()
        serializer = CustomUserSerializer(person_api, many=True)
        help.log_check()
        logger.debug("Данные получены")
        return serializer.data

    def post_person_data(request):
        person_api = request.data.get("person_api")
        email =person_api['email']
        code = help.rnd_generate()
        person_api["activate_code"] = code
        SendAuthEmail(email,code)
        serializer = CustomUserSerializer(data=person_api)
        if serializer.is_valid(raise_exception=True):
            person_save = serializer.save()
        obtain_auth_token(sender=settings.AUTH_USER_MODEL)
        help.log_check()
        logger.debug("Пользователь '{}' создан (не активирован)".format(email))
        return email

    def put_person_data(request, pk):
            resp = requests.get('http://127.0.0.1:8000', headers={'Token': '2f869396dfa524f9e1319961480ee3fa056638ea'})
            token_get =  resp.request.headers['Token']
            tokens_set = Token.objects.filter(key=token_get)
            if not tokens_set:
                help.log_check()
                logger.error("Токен '{}' не существует".format(token_get))
                return ("Токен не действителен")
            else:
                token_user_id = tokens_set.values('user_id')
                first_orb_tocken =  token_user_id.first()
                id_user =  first_orb_tocken.get('user_id')
                CustomUser.objects.filter(id =id_user)
                main_id=pk
                if  id_user != main_id:
                    help.log_check()
                    logger.error("Не достаточно прав для редактирование аккаунта")
                    return ("Не достаточно прав ")
                else:
                    person_save = get_object_or_404(CustomUser.objects.all(), pk=pk)
                    data = request.data.get('person_api')
                    serializer = CustomUserSerializer(instance=person_save, data=data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        personal_save = serializer.save()
                        help.log_check()
                        logger.debug("Профиль пользователя '{}' обновлен".format(personal_save.email))
                    return ("Челик {} обновился ".format(personal_save.email))

    def delete_person_data(pk):
        person_obj = get_object_or_404(CustomUser.objects.all(), pk=pk)
        person_obj.delete()
        help.log_check()
        logger.debug("Профиль пользователя '{}' удален".format(person_obj.email))
   
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def obtain_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 
    help.log_check()
    logger.debug("Пользователю  на '{}' был выдан токен  ".format(instance))