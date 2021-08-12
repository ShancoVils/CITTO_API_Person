from .import views
from django.urls import path
from .views import PersonView, generate_excel_file,activate_user,api_get_questions,api_post_answers,get_winner,api_get_results


urlpatterns = [
    # Получить данные '
    path('person/', PersonView.as_view()), 
    # Put запрос 
    path('person/<int:pk>', PersonView.as_view()),
    # Записать в бд все данные с указанного excel файла
    path('generate_users/', views.generate_users),
    # Переход по ссылке указанной в письме(подтверждение аккаунта) 
    path('confirm_form/<slug:random_code>/',activate_user),
    #Генерирует excel файл
    path('generate_excel_file/', generate_excel_file),
    #Генерация вопросов 
    path('generate_questions/', api_get_questions),
    #Отправка ответов
    path('post_answers/', api_post_answers),
    #Получение результатов
    path('get_results/', api_get_results),
    #Получение победителя
    path('get_winner/', get_winner),
]
