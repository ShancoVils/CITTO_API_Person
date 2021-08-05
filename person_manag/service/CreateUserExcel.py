from ..models import CustomUser
import os,xlrd

# Класс считывает указанный excel файл, и добавляет записи в бд

class CreateUserExcel():
    def __init__(self, request):
        # Получаю файл
        excel_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'excel_file/teams.xls')
        excel_dict = {}
        excel_file = xlrd.open_workbook(excel_file_path)
        excel_sheet = excel_file.sheet_by_index(0)
        # Считывание файла
        for i in range(excel_sheet.nrows):
            x = excel_sheet.row_values(i) 
            if i not in excel_dict:
                excel_dict[i] = x
        num_user = 1
        # Добавление в базу данных
        while (num_user < int((excel_sheet.nrows))):
            one_per = excel_dict[num_user]
            email_excel_obj = one_per[1]
            password_excel_obj = one_per[2]
            person_ge_excel_obj = int(one_per[3])
            ex_user = CustomUser.objects.create_user(email = email_excel_obj,
                                                    password=  password_excel_obj,
                                                    person_group_id = person_ge_excel_obj)
            ex_user.save()
            print("Юзер '{}' добавлен".format(num_user))
            num_user = num_user+1
