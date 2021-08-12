from ..models import GroupPerson, QuestionsPull, CustomUser, TestResults,DetailedTestResult as dtr
from .GenerateQuestionSet import GenerateQuestionsSet as gqs
from ..serializers import GenerateQuestionSerializer,TestResultSerializer,DetailedTestResultSerializer,TestResultSerializerView
from rest_framework.authtoken.models import Token
from .Hepler_class import Helper as help
from ..logs import logger
from rest_framework.views import APIView
import requests
from django.db.models import Count

'''
Класс реализует систему тестов в системе, а именно: 
Генерация вопросов, проверка ответов, получение результатов
всех прошедших, а так же определение пользователя, который
прошел тест лучше всего

'''
class GenerateQuestions(APIView):
    #Метод генерирует пулл вопросов
    def get_question(request):
        #Проверка на токен
        resp = requests.get('http://127.0.0.1:8000', headers={'Token': 'd94c3ce10d6850d880fc325b64f9a3c90734f1da'})
        token_get =  resp.request.headers['Token']
        tokens_set = Token.objects.filter(key=token_get)
        if not tokens_set:
            help.log_check()
            logger.error("Токен '{}' не существует".format(token_get))
            return ("Токен не действителен")
        else:
            token_user_id = tokens_set.values('user_id')
            first_orb_tocken = token_user_id.first()
            id_user =  first_orb_tocken.get('user_id')
            user_data = CustomUser.objects.get(id=id_user)
            group_info = GroupPerson.objects.filter(Name_Group = user_data.person_group)
            group_factor = group_info.values()
            max_factor = group_factor[0]['max_test_factor']
            question_pull = gqs.get_question_set(request, max_factor)
            serializer = GenerateQuestionSerializer(question_pull, many = True)
            help.log_check()
            logger.debug("Вопросы получены")
            return serializer.data
    # Метод передает ответы
    def post_answer(request):
        # Проверка токена
        user_list = {}
        resp = requests.get('http://127.0.0.1:8000', headers={'Token': '2f869396dfa524f9e1319961480ee3fa056638ea'})
        token_get =  resp.request.headers['Token']
        tokens_set = Token.objects.filter(key=token_get)
        token_user_id = tokens_set.values('user_id')
        first_orb_tocken = token_user_id.first()
        id_user =  first_orb_tocken.get('user_id')
        user = CustomUser.objects.get(id = id_user)
        answers_api = request.data.get('answers_api')
        id_answer = 0
        mark_list = []
        # Проверки вопросов
        for i in answers_api:
            quest_id = answers_api[id_answer]
            quest =quest_id['id']
            quest_one = QuestionsPull.objects.get(id = quest)
            if quest_one.answer==quest_id['answer']:
                quest_factor = quest_one.factor
                mark_list.append(quest_factor)
            id_answer = id_answer+1
        mark = sum(mark_list)
        # Проверка на "сдал/не сдал"
        user_list['test_result'] = mark
        user_list['tested_user_id'] = id_user
        group_info = GroupPerson.objects.filter(Name_Group = user.person_group)
        group_factor = group_info.values()
        pass_factor = group_factor[0]['pass_test_factor']
        if pass_factor <=  mark:
            user_list['test_mark'] = "Pass"
        else:
            user_list['test_mark'] = "Failed"
        serializer = TestResultSerializer(data=user_list)
        if serializer.is_valid(raise_exception=True):
            person_save = serializer.save()


        user_result_list = {}
        id_res_ans = 0
        test_id = TestResults.objects.get(tested_user = id_user)
        for i in  answers_api:
            quest_id = answers_api[id_res_ans]
            quest =quest_id['id']
            quest_one = QuestionsPull.objects.get(id = quest)
            if quest_one.answer==quest_id['answer']:
               user_result_list['test_number_id'] = test_id.id
               user_result_list['question'] = quest_one.question
               user_result_list['factor'] = quest_one.factor
               user_result_list['qustion_result'] = "Верно"
            else:
                user_result_list['test_number_id'] = test_id.id
                user_result_list['question'] = quest_one.question
                user_result_list['factor'] = quest_one.factor
                user_result_list['qustion_result'] = "Не верно"
            id_res_ans = id_res_ans+1
            serializer = DetailedTestResultSerializer(data=user_result_list)
            if serializer.is_valid(raise_exception=True):
                person_save = serializer.save()
        return mark
    # Метод возвращает результаты (доступно только админу)
    def get_result(request):
        # Проверка токена (ТОКЕН НЕ МЕНЯТЬ)
        resp = requests.get('http://127.0.0.1:8000', headers={'Token': '2f869396dfa524f9e1319961480ee3fa056638ea'})
        token_get =  resp.request.headers['Token']
        tokens_set = Token.objects.filter(key=token_get)
        if not tokens_set:
            help.log_check()
            logger.error("Токен '{}' не существует".format(token_get))
            return ("Токен не действителен")
        else:
            test_result_data = TestResults.objects.all()
            serializer = TestResultSerializerView(test_result_data, many=True)
            help.log_check()
            logger.debug("Результаты получены")
            return serializer.data
    # Метод возвращает лучшего прошедшего тест
    def get_winner(request):
        # Создание "контейнера для матрицы"
        big_matrix = []
        # Создание списка с проверенными результатами (из них выбирается лучший)
        best_factor_list = []
        all_test_num = dtr.objects.all().values('test_number_id').annotate(total=Count('test_number_id')).order_by('test_number_id')
        test_result_index = 0
        # Основной цикл, количество итерация зависит от количества прошедших тест
        for i in range(len(all_test_num)):
            user_result_list = []
            user_val = all_test_num[test_result_index]
            user_val = user_val.values()
            user_val=list(user_val)[0]
            # Получаю id и email пользователя для занесения в матрицу
            id_answer = 0
            all_quest = dtr.objects.filter(test_number_id = int(user_val)).order_by('factor')
            user_id_source = TestResults.objects.filter(id = int(user_val))
            id_quest_list = []
            user_id = user_id_source.values()
            user_id=list(user_id)[0]['tested_user_id']
            user_email_source = CustomUser.objects.filter(id = user_id)
            user_email = user_email_source.values()
            user_email=list(user_email)[0]['email']
            # Добавляю email пользователя в список
            user_result_list.append(user_email) 
            # Цикл для получения всех коэфициентов вопросов, на которые ответил пользователь
            for i in all_quest:
                question_val = all_quest.values()
                question_val = question_val[id_answer]
                question_val = question_val.values()
                if list(question_val)[4] == "Верно":
                    question_val=list(question_val)[3]
                    id_quest_list.append(question_val)
                    id_answer = id_answer+1
                else:
                    id_answer = id_answer+1
            # Добавляю список коэффиуиентов в список
            user_result_list.append(id_quest_list)

            # Получаю общий список всех коэффициентов для будующего сравнения
            id_answer = 0
            all_quest = QuestionsPull.objects.all().order_by('factor')
            factor_list = []
            for i in all_quest:
                factor_val = all_quest.values()
                factor_val = factor_val[id_answer]
                factor_val = factor_val.values()
                factor_val=list(factor_val)[5]
                factor_list.append(factor_val)
                id_answer = id_answer+1
            # Удаляю повторяющиеся коэффициенты
            unic_factor_list = list(set(factor_list))
            # Добавляю  все коэффициенты в список
            user_result_list.append(unic_factor_list)
            
            # Вычесление лучшего прошедшего тест
            # Создаю список с коэфициентами вопросов, на которые пользователь не ответил
            wrong_answer_list = [x for x in id_quest_list + unic_factor_list 
                                if x not in id_quest_list or x not in unic_factor_list]
            answer_factor = sum(id_quest_list)
            wrong_factor = sum(wrong_answer_list)
            # Получаю коэффциент
            best_factor = float(answer_factor)-float(wrong_factor)
            # Добавляю коэффициент в основной спсок и список для тестов
            best_factor_list.append(best_factor)
            user_result_list.append(best_factor)
            big_matrix.append(user_result_list)
            test_result_index = test_result_index + 1
        # Из общей матрицы считываю каждый элемент, и если он соответствует лучшему коф. то вывожу его
        winner_i = 0
        for i in range(len(big_matrix)):
            big_matrix_elem = big_matrix[winner_i]
            if big_matrix_elem[3] == (max(best_factor_list)):
                print("Победил '{}'".format(big_matrix_elem[0]))
                winner_i = winner_i +1
            else:
                winner_i = winner_i +1
        return (big_matrix_elem[0])
