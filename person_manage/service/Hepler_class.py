import os
import random,string



class Helper():

    # Если размер основного лог-файла больше 500б, создается новый, а записи в этом перекидывются в хранилище
    
    def log_check():
        if  int(os.path.getsize('logs/logs.log'))  <  int(500):
            print(os.path.getsize('logs/logs.log'))
        else:    
            log_file =  open('logs/logs.log', 'r')
            log_info = log_file.read()
            other_log_file =  open('logs/other_logs.log', 'a')
            other_log_file.write(log_info)
            open('logs/logs.log', 'w').close()

    # Метод генерирует код

    def rnd_generate():
        letters_and_digits = string.ascii_letters + string.digits
        random_char = ''.join(random.sample(letters_and_digits, 16 ))
        return str(random_char)


    

