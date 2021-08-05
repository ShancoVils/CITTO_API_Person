import os

#Если размер основного лог-файла больше 500б, создается новый, а записи в этом перекидывются в хранилище

class CheckWeightLogs():       
    def __init__(self):
        if  int(os.path.getsize('logs/logs.log'))  <  int(500):
            print(os.path.getsize('logs/logs.log'))
        else:    
            log_file =  open('logs/logs.log', 'r')
            log_info = log_file.read()
            other_log_file =  open('logs/other_logs.log', 'a')
            other_log_file.write(log_info)
            open('logs/logs.log', 'w').close()
