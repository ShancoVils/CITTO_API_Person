import os
import random,string,requests
from rest_framework.authtoken.models import Token
from ..logs import logger
from ..models import CustomUser


class Helper():

    # Если размер основного лог-файла больше 500б, создается новый, а записи в этом перекидывются в хранилище
    
    def log_check():
        if  int(os.path.getsize('logs/logs.log'))  <  int(500):
            print(os.path.getsize('logs/logs.log'))
        else:    
            log_file =  open('logs/logs.log', 'r')
            log_info = log_file.read()
            other_log_file =  open('logs/other_logs.log', 'a')
            other_log_file.write(log_info)
            open('logs/logs.log', 'w').close()

    # Метод генерирует код

    def rnd_generate():
        letters_and_digits = string.ascii_letters + string.digits
        random_char = ''.join(random.sample(letters_and_digits, 16 ))
        return str(random_char)

    # Метод проверяет токен на корректность(принимает токен, возвращает id или отказ)

    def tocken_check():
        resp = requests.get('http://127.0.0.1:8000', headers={'Token': "0b027cb20327469e8229e48a4fca5f77bc073c69"})
        token_get =  resp.request.headers['Token']
        tokens_set = Token.objects.filter(key=token_get)
        if not tokens_set:
            logger.error("Токен '{}' не существует".format(token_get))
            return ("Токен не действителен")
        else:
            token_user_id = tokens_set.values('user_id')
            first_orb_tocken = token_user_id.first()
            id_user =  first_orb_tocken.get('user_id')
            return True,id_user
