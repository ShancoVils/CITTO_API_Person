from requests.api import request
from rest_framework import serializers
from ..models import GroupPerson, QuestionsPull, CustomUser
from .GenerateQuestionSet import GenerateQuestionsSet as gqs
from ..serializers import GenerateQuestionSerializer,TestResult
from rest_framework.authtoken.models import Token
from .Hepler_class import Helper as help
from ..logs import logger
from rest_framework.views import APIView
import requests



class GenerateQuestions(APIView):
    def get_question(request):
        resp = requests.get('http://127.0.0.1:8000', headers={'Token': 'ec8b1e1792bf80a9b99c57e301bf352a51ad8013'})
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

    def post_answer(request):
        user_list = {}
        resp = requests.get('http://127.0.0.1:8000', headers={'Token': 'ec8b1e1792bf80a9b99c57e301bf352a51ad8013'})
        token_get =  resp.request.headers['Token']
        tokens_set = Token.objects.filter(key=token_get)
        token_user_id = tokens_set.values('user_id')
        first_orb_tocken = token_user_id.first()
        id_user =  first_orb_tocken.get('user_id')
        user = CustomUser.objects.get(id = id_user)
        answers_api = request.data.get('answers_api')
        id_answer = 0
        mark_list = []
        for i in answers_api:
            quest_id = answers_api[id_answer]
            quest =quest_id['id']
            quest_one = QuestionsPull.objects.get(id = quest)
            if quest_one.answer==quest_id['answer']:
                quest_factor = quest_one.factor
                mark_list.append(quest_factor)
            id_answer = id_answer+1
        mark = sum(mark_list)
        user_list['test_result'] = mark
        user_list['tested_user_id'] = id_user

        group_info = GroupPerson.objects.filter(Name_Group = user.person_group)
        group_factor = group_info.values()
        pass_factor = group_factor[0]['pass_test_factor']
        if pass_factor <=  mark:
            user_list['test_mark'] = "Pass"
        else:
            user_list['test_mark'] = "Failed"
        serializer = TestResult(data=user_list)
        if serializer.is_valid(raise_exception=True):
            person_save = serializer.save()

        
        return mark
