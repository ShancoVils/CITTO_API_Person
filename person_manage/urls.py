from .import views
from django.urls import path
from .views import PersonView, generate_excel_file,activate_user, api_get_results,get_winner,api_get_and_post_questions,put_answer_results

urlpatterns = [
    # Получить данные '
    path('person/', PersonView.as_view()), 
    # Put запрос 
    path('person/<int:pk>', PersonView.as_view()),
    # Записать в бд все данные с указанного excel файла
    path('generate_users/', views.generate_users),
    # Переход по ссылке указанной в письме(подтверждение аккаунта) 
    path('confirm_form/<slug:random_code>/',activate_user),
    # Генерирует excel файл
    path('generate_excel_file/', generate_excel_file),
    # Получение результатов
    path('get_results/', api_get_results),
    #Получение победителя
    path('get_winner/', get_winner),
    #Получение вопросов(занесние в бд)
    path('get_and_post_questions/', api_get_and_post_questions),
    #Занесение результатов в опросов в бд
    path('put_answer_result/<int:pk>', put_answer_results),
]
