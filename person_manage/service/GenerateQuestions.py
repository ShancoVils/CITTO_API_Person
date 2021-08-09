from requests.api import request
from rest_framework import serializers
from ..models import QuestionsPull
from ..serializers import GenerateQuestionSerializer
from .Hepler_class import Helper as help
from ..logs import logger
from rest_framework.response import Response
from rest_framework.views import APIView
from itertools import combinations

class GenerateQuestions(APIView):
    def get_question():
        max_factor =20
        all_questions_pull = QuestionsPull.objects.order_by('?')[:2]
        serializer = GenerateQuestionSerializer(all_questions_pull, many = True) 
        help.log_check()
        logger.debug("Вопросы получены")
        return serializer.data

    def post_answer(request):
        cof_answer = 0
        answers_api = request.data.get('answers_api')
        id_ans = 0
        for i in answers_api:
            quest_id = answers_api[id_ans]
            quest =quest_id['id']
            quest_one = QuestionsPull.objects.get(id = quest)
            if quest_one.answer==quest_id['answer']:
                cof_answer = cof_answer+1
            id_ans = id_ans+1
        return cof_answer

        