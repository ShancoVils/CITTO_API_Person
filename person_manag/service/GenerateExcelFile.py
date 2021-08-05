import random,string,re,os
from random import randint
import pandas as pd
# Метод генерирующий excel файл


class GenerateExcelFile():
    def __init__(self,request,quantity):
        account_dict = {}   
        email_list = []
        password_list =[]
        person_group_id_list = []
        def generate_random_email(self):
            for x in range(quantity):
                length = 8
                rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
                result = re.sub(r'n', rand_string, 'n@mail.ru')
                email_list.append(result)
                account_dict.update({'email': email_list})
        def generate_random_password(self):
            for x in range(quantity):
                length = 11
                rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
                password_list.append(rand_string)
                account_dict.update({'password': password_list})
        def generate_random_group_id(self):
            for x in range(quantity):
                rand_string =  randint(1, 2)
                person_group_id_list.append(rand_string)
                account_dict.update({'person_group_id': person_group_id_list})
        generate_random_email(quantity)
        generate_random_password(quantity)
        generate_random_group_id(quantity)
        df = pd.DataFrame(account_dict) 
        df.to_excel('excel_file/teams.xls')


        