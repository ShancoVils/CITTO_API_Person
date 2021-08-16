from os import times
from ..models import GroupPerson, QuestionsPull, CustomUser, TestResults
from .GenerateQuestionSet import GenerateQuestionsSet as gqs
from .Hepler_class import Helper as help
from ..logs import logger
from rest_framework.views import APIView
import requests, datetime
from datetime import timedelta
from rest_framework.generics import  get_object_or_404
from ..serializers import GenerateQuestionSerializer,TestResultSerializer,TestResults
'''
Класс реализует систему тестов в системе, а именно: 
Генерация вопросов, проверка ответов, получение результатов
всех прошедших, а так же определение пользователя, который
прошел тест лучше всего

'''
class GenerateQuestions(APIView): 


    # Метод возвращает результаты (доступно только админу)
    def get_result(request):
        # Проверка токена (ТОКЕН НЕ МЕНЯТЬ)
        token = "e164ab1c3e19d899b2d62f2ee3515fbae7d6e481"
        tocken_result =  help.tocken_check(token)
        if tocken_result[0] == True:
            test_result_data = TestResults.objects.all()
            serializer = TestResultSerializer(test_result_data, many=True)
            help.log_check()
            logger.debug("Результаты получены")
            return serializer.data
        else:
            return tocken_result
   

    # Метод возвращает лучшего прошедшего тест
    def get_winner(request):
        # Создание "контейнера для матрицы"
        main_matrix = []
        big_matrix = []
        all_test_results = TestResults.objects.all()
        test_result_index = 0
        # Основной цикл, количество итерация зависит от количества прошедших тест
        for i in range(len(all_test_results)):
            final_list = []
            user_result_list = []
            test_user_data = all_test_results.values()
            test_user_data = test_user_data[test_result_index]
            test_user_data = test_user_data.values()

            id_user = list(test_user_data)[1]
            id_quest_vall = list(test_user_data)[2]
            answer_test = list(test_user_data)[3]

            user_quest_check_list = list(zip(id_quest_vall, answer_test))
            user_result_list.append(id_user)
            user_result_list.append(user_quest_check_list)
            final_list.append(id_user)

            false_quest_id = []
            true_quest_id = []
            iter_answer = 0
            for i in range(len(user_quest_check_list)):
                if user_quest_check_list[iter_answer][1] == True:
                    true_quest_id.append(user_quest_check_list[iter_answer][0])
                    iter_answer+=1
                elif user_quest_check_list[iter_answer][1] == False:
                    false_quest_id.append(user_quest_check_list[iter_answer][0])
                    iter_answer+=1
            
            true_factor = []
            iter_test = 0
            for i in range(len(true_quest_id)):
                all_quest_factor = QuestionsPull.objects.filter(id=true_quest_id[iter_test])
                quest_factor_data = all_quest_factor.values()
                quest_factor_data = quest_factor_data[0].values()
                factor_answer = list(quest_factor_data)[5]
                true_factor.append(factor_answer)
                iter_test +=1

            false_factor = []
            iter_test = 0
            for i in range(len(false_quest_id)):
                all_quest_factor = QuestionsPull.objects.filter(id=false_quest_id[iter_test])
                quest_factor_data = all_quest_factor.values()
                quest_factor_data = quest_factor_data[0].values()
                factor_answer = list(quest_factor_data)[5]
                false_factor.append(factor_answer)
                iter_test +=1
                
            best_factor = float(sum(true_factor))-float(sum(false_factor))
            big_matrix.append(best_factor)

            final_list.append(best_factor)
            main_matrix.append(final_list)
            test_result_index+=1
        # print(true_quest_id)
        # print(false_quest_id)
        # print(quest_factor_data)
        # print(true_factor)
        # print(false_factor)
        print(main_matrix)
        winner_i = 0
        for i in range(len(main_matrix)):
            if main_matrix[winner_i][1] == (max(big_matrix)):
                winner_id = main_matrix[winner_i][0]
                winner_i+=1
            else:
                winner_i+=1
        print (winner_id)
        return (winner_id)


    # Метод возвращает сгенерированные вопросы и записывает их без результата в бд
    def get_and_post_questions(request):
        token = "0b027cb20327469e8229e48a4fca5f77bc073c69"
        tocken_result =  help.tocken_check(token)
        if tocken_result[0] == True:
            id_user = tocken_result[1]
            user_data = CustomUser.objects.get(id=id_user)
            group_info = GroupPerson.objects.filter(Name_Group = user_data.person_group)
            group_factor = group_info.values()
            max_factor = group_factor[0]['max_test_factor']
            question_pull = gqs.get_question_set(request, max_factor)
            serializer_question = GenerateQuestionSerializer(question_pull, many = True)
            help.log_check()
            logger.debug("Вопросы получены")


            # Занесение списка вопросов в бд'
            id_quest_list_iter = 0
            user_quest_dict = {}
            user_quest_dict['tested_user_id'] = id_user
            all_question_id_list = []
            for i in range(len(question_pull)):
                quest_id = question_pull[id_quest_list_iter]
                quest =quest_id.id
                all_question_id_list.append(quest)
                id_quest_list_iter = id_quest_list_iter+1
            user_quest_dict['test_questions'] = all_question_id_list
            date = datetime.datetime.now()
            time_now = date.strftime('%H:%M')
            user_quest_dict['test_time_begin'] = time_now
            serializer_test = TestResultSerializer(data=user_quest_dict)
            if serializer_test.is_valid(raise_exception=True):
                person_save = serializer_test.save()
            return serializer_question.data
        else:
            help.log_check()
            logger.error("Токен '{}' не существует".format(token))
            return tocken_result
            
            
            
    def put_answer_result(request,pk): 
        user_list = {}
        token = "0b027cb20327469e8229e48a4fca5f77bc073c69"
        tocken_result =  help.tocken_check(token)
        if tocken_result[0] == True:
            id_user = tocken_result[1]
            user = CustomUser.objects.get(id = id_user)
            answers_api = request.data.get('answers_api')
            answers_result_iter = 0
            answer_list = []
            # Проверки вопросов
            for i in answers_api:
                quest_id = answers_api[answers_result_iter]
                quest =quest_id['id']
                quest_one = QuestionsPull.objects.get(id = quest)
                if quest_one.answer==quest_id['answer']:
                    quest_factor = quest_one.factor
                    answer_list.append(True)
                else:
                    answer_list.append(False)
                answers_result_iter = answers_result_iter+1
            user_list['test_answers'] = answer_list
            # Проверка оценки
            factor_anser_iter = 0
            factor_answer_list = []
            for i in answers_api:
                quest_id = answers_api[factor_anser_iter]
                quest =quest_id['id']
                quest_one = QuestionsPull.objects.get(id = quest)
                if quest_one.answer==quest_id['answer']:
                    quest_factor = quest_one.factor
                    factor_answer_list.append(quest_factor)
                factor_anser_iter = factor_anser_iter+1
            mark = sum(factor_answer_list)
            user_list['test_sum_factor'] = int(mark)
            # Проверка на "сдал/не сдал"
            # Получение проходного балла
            group_info = GroupPerson.objects.filter(Name_Group = user.person_group)
            group_factor = group_info.values()
            pass_factor = group_factor[0]['pass_test_factor']
            # Получение времени начаал теста
            test_info = TestResults.objects.filter(id = pk)
            test_info = test_info.values()
            time_begin_info = test_info[0]['test_time_begin']
            date_end =  datetime.datetime.now()
            time_now = date_end.strftime('%H:%M')
            # Вычисление разницы
            time_rec = datetime.datetime.now() - timedelta(minutes=2)
            time_recsf = time_rec.strftime('%H:%M')
            print(type(time_begin_info))
            print(type(time_recsf))
            user_list['test_time_end'] = time_now
            # Контрольная проверка на результат
            if pass_factor <=  mark and str(time_begin_info)>=time_recsf:
                user_list['test_result'] = "Pass"
            else:
                user_list['test_result'] = "Failed"
            test_result_save = get_object_or_404(TestResults.objects.all(), pk=pk)
            serializer = TestResultSerializer(instance=test_result_save, data=user_list, partial=True)
            if serializer.is_valid(raise_exception=True):
                person_save = serializer.save()
            return answer_list
        else:
            return tocken_result
