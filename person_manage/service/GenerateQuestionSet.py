from ..models import QuestionsPull
import itertools
from random import randint
from itertools import chain



class GenerateQuestionsSet():
    def get_question_set(request, max_factor):
            qs = QuestionsPull.objects.all()
            qs_jj = qs.values()
            list_test = []
            schetchik = 0
            for i in range(len(qs)):
                ff = qs_jj[schetchik]['factor']
                list_test.append(ff)
                schetchik = schetchik+1
            print(list_test)
            list_true_char = []
            iteration = 0
            for item in  range(len(qs)):
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
