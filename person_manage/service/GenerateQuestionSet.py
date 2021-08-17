from ..models import QuestionsPull
import itertools
from random import randint
from itertools import chain


class GenerateQuestionsSet():
    '''

    Класс генерирует пулл вопросов, в зависимости от отдела пользователя,
    который будет его проходить. Количество и максимальный возможный балл 
    определяет переменная max_factor

    '''
    def get_question_set(request, max_factor):
            quest_pull = QuestionsPull.objects.all()
            quest_pull = quest_pull.values()
            list_test = []
            counter_factor = 0
            for i in range(len(quest_pull)):
                ff = quest_pull[counter_factor]['factor']
                list_test.append(ff)
                counter_factor = counter_factor+1
            print(list_test)
            list_true_char = []
            iteration = 0
            for item in  range(len(quest_pull)):
                results = itertools.combinations(list_test, iteration)
                for item in results:
                    if sum(item)==max_factor:
                        list_true_char.append(item)
                    else:
                        print(item)
                iteration = iteration+1
            print(list_true_char)
            random_key =  randint(0, len(list_true_char)-1)
            print(random_key)
            pull_one = list_true_char[random_key]
            pull_elem = 0
            all_questions_pull = []
            for i in range(len(pull_one)):
                index_one_pull = QuestionsPull.objects.filter(factor = pull_one[pull_elem])[:1]
                all_questions_pull = list(chain(all_questions_pull, index_one_pull))
                pull_elem = pull_elem + 1
            return all_questions_pull
