'''
Класс `BoardOutException` будет использоваться, когда
игрок пытается выстрелить в клетку за пределами поля.
Мы вызываем конструктор суперкласса `Exception`, чтобы объявить исключение.'''
class BoardOutException(Exception):
    def __init__(self, message="Попытка выстрела за пределы поля"):
        self.message = message
        super().__init__(self.message)

'''
Класс `DotAlreadyHitException` будет использоваться, когда игрок пытается выстрелить в уже подбитую клетку. 
'''
class DotAlreadyHitException(Exception):
    def __init__(self, message="Попытка выстрела в уже подбитую клетку"):
        self.message = message
        super().__init__(self.message)

