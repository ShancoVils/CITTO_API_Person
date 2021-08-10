from requests.api import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from django.http import HttpResponse
from rest_framework.response import Response
from .service.CreateUserExcel import CreateUserExcel
from .service.GenerateExcelFile import GenerateExcelFile
from .service.PersonApiFunctional import PersonView as api
from .service.UserAutentificate import ActivateCodeForm
from .service.GenerateQuestions import GenerateQuestions
from .models import QuestionsPull, CustomUser, GroupPerson
import itertools
import numpy 
'''
Класс реализует основной функционал API и стандартные методы GET,PUT, POST, DELETE

'''
class PersonView(APIView):

    # Метод получает все данные о пользователях

    def get(self, request):
        get_user = api.get_person_data() 
        return Response({"person_api": get_user})

    # Метод создает пользователя, чтобы активировать его,
    # необходимо зайти на указаннуб почту и перейти по ссылке

    def post(self,request):
        post_user = api.post_person_data(request)
        return Response({
        "success": "{}, активируйте аккаунт на указанной вами почте ".format(post_user)
        })

    #Метод редактирует данные, указанного пользователя,
    #но если токен, указанный в headers не соответствует токену редактируемого пользователя 
    #метод не сработает

    def put(self,request, pk):
        put_user = api.put_person_data(request, pk)
        return Response({
            "success": " {} ".format(put_user)
        })
            
    #Метод удаляет указанного пользователя
        
    def delete(self, request, pk):
        delete_user = api.delete_person_data(pk)
        return Response({
            "message": "{}".format(delete_user)
        })

#Считывает указанный excel файл, и добавляет записи в бд

def generate_users(request):
    CreateUserExcel(request)
    return HttpResponse("Пользователи добавлены в бд")

#Считывает указанный excel файл, и добавляет записи в бд
quantity =  5

def generate_excel_file(request):
    GenerateExcelFile(request, quantity)
    return HttpResponse("Excel файл сгенерирован")

# Класс активирует аккаунт, который перешел по ссылке

def activate_user(request, random_code):
    ActivateCodeForm(random_code)
    return HttpResponse("Пользователь акивирован")




@api_view(['GET'])
def api_get_questions(request):
    question_pull =  GenerateQuestions.get_question(request)
    return Response({"Вопросы": question_pull})


@api_view(['POST'])
def api_post_answers(request):
    answers_pull =  GenerateQuestions.post_answer(request)
    return Response({"Ваш результат": answers_pull})


def test_algoritm(request):
    user_data = CustomUser.objects.get(id=12)
    group_info = GroupPerson.objects.filter(Name_Group = user_data.person_group)
    group_factor = group_info.values()
    max_factor_group = group_factor[0]['max_test_factor']
    return HttpResponse(max_factor_group)
