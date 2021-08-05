import random,string

# Метод генерирует код, который будет использоваться в ссылке активации

class GenerateCode():
    def activate_user():
        letters_and_digits = string.ascii_letters + string.digits
        random_char = ''.join(random.sample(letters_and_digits, 16 ))
        return str(random_char)
    