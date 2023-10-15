import random


class Dot:  # точка на игровом поле с координатами х и у
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# Класс Ship имеет конструктор c параметрами корабля (длину, точку носа и направление) и количеством жизней корабля (количество точек, которые еще не подбиты).
# метод dots(self)`: Это метод, возвращающий список клеток, занимаемых кораблем.
# В методе используется цикл, который проходит от 0 до длины корабля. В зависимости от направления корабля ('вертикальное'
# или другое), создается объект `Dot` с соответствующими координатами. Объекты `Dot` добавляются в список `ship_dots`,
# который в конце метода возвращается.

class Ship:
    def __init__(self, length, bow_of_the_ship, direction):
        self.length = length
        self.bow_of_the_ship = bow_of_the_ship
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            if self.direction == 'вертикальное':
                dot = Dot(self.bow_of_the_ship.x, self.bow_of_the_ship.y + i)
            else:
                dot = Dot(self.bow_of_the_ship.x + i, self.bow_of_the_ship.y)
            ship_dots.append(dot)
        return ship_dots


# Класс "Board" представляет игровое поле. У него есть методы  place_ship для размещения корабля на поле,
# out для проверки, выходит ли точка за пределы поля, и shot для выстрела.

class Board:
    def __init__(self):
        self.board = [['О' for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.hide_ships = True
        self.num_of_alive_ships = 0


'''
Метод `add_ship`принимает объект `ship`, представляющий корабль, и добавляет его на доску.
Сначала метод проверяет, возможно ли разместить корабль на указанных позициях. Если невозможно, выбрасывается исключение.
Затем метод обновляет состояние каждой клетки на доске, отмечая их как занятые кораблем.
Также метод добавляет корабль в список `ships` и увеличивает счетчик живых кораблей на доске.
'''


def add_ship(self, ship):
    for dot in ship.dots():
        if self.out(dot) or self.board[dot.x][dot.y] == '■':
            raise Exception("Невозможно поставить корабль на эту позицию")
    for dot in ship.dots():
        self.board[dot.x][dot.y] = '■'
    self.ships.append(ship)
    self.num_of_alive_ships += 1


'''Метод `contour` принимает объект `ship` и контурирует его на доске.Метод перебирает 
каждую позицию корабля и обновляет состояние соседних клеток на доске, 
помечая их как недопустимые для размещения корабля (как 'О').
'''


def contour(self, ship):
    for dot in ship.dots():
        for i in range(dot.x - 1, dot.x + 2):
            for j in range(dot.y - 1, dot.y + 2):
                if not self.out(Dot(i, j)):
                    if self.board[i][j] != '.':
                        self.board[i][j] = 'О'


'''Метод `out` проверяет, выходит ли заданная точка (`dot`) за пределы поля доски.
Если координаты `dot` выходят за пределы 6х6, то метод возвращает True, иначе - False.'''


def out(self, dot):
    return dot.x < 0 or dot.x >= 6 or dot.y < 0 or dot.y >= 6


'''Метод `print_board' выводит состояние доски в консоль.
Он создает  таблицу, отображающую состояние каждой клетки в виде символов '■', 'О' или 'X'.
'''


def print_board(self):
    print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
    for i in range(6):
        print(f" {i + 1} | ", end="")
        for j in range(6):
            if self.hide_ships and self.board[i][j] == '■':
                print("О | ", end="")
            else:
                print(f"{self.board[i][j]} | ", end="")
        print()


''' Метод `shot`делает выстрел по точке `dot` на доске.
Если точка `dot` выходит за пределы доски или уже была использована (точка содержит '.'), метод выбрасывает исключение.
Если точка содержит символ '■', значит эта точка представляет корабль, и он будет помечен как 'X'.
Если точка содержит символ 'О', то это пустая клетка, и она будет помечена как '.'.'''


def shot(self, dot):
    if self.out(dot) or self.board[dot.x][dot.y] == 'T':
        raise Exception("Невозможно сделать выстрел в эту точку")
    elif self.board[dot.x][dot.y] == '■':
        self.board[dot.x][dot.y] = 'X'
        self.num_of_alive_ships -= 1
    else:
        self.board[dot.x][dot.y] = 'T'


'''Метод `setup_board`устанавливает начальную расстановку кораблей на доске.
Он вызывает метод `add_ship` для добавления кораблей заданного размера и расположения на доску.'''


def place_scip(self):
    self.add_ship(Ship(3, Dot(1, 1), 'горизонтальное'))

    self.add_ship(Ship(2, Dot(2, 4), 'вертикальное'))
    self.add_ship(Ship(2, Dot(2, 5), 'горизонтальное'))

    self.add_ship(Ship(1, Dot(4, 0), 'горизонтальное'))
    self.add_ship(Ship(1, Dot(4, 2), 'горизонтальное'))
    self.add_ship(Ship(1, Dot(4, 4), 'горизонтальное'))
    self.add_ship(Ship(1, Dot(4, 5), 'горизонтальное'))


# Класс "Player" - класс для игроков.
# У него есть методы move, который выполняет ход игрока, и ask, который запрашивает у пользователя координаты выстрела.

class Player:  # игроки
    def __init__(self):
        self.own_board = Board()
        self.enemy_board = Board()

    def ask(self):  # уточнение. в какую клетку будем ходить. Пока метод останется пустым
        pass

    def move(self):  # отвечает за ход в игре. Ловим исключения, если они есть, повторяем ход
        while True:
            dot = self.ask()
            try:
                hit = self.enemy_board.shot(dot)
            except Exception as e:
                print(str(e))
            else:
                return hit


# Класс "AI" подкласс класса "Player", который  представляет компьютерного соперника.
# Метод ask используется для случайного выбора координаты выстрела.

class AI(Player):  #
    def ask(self):
        x = random.randint(0, 6)
        y = random.randint(0, 6)
        return Dot(x, y)


# Класс "User" также наследуется от класса "Player" и представляет другого игрока.
# В методе ask пользователь вводит координаты выстрела с клавиатуры.

class User(Player):
    def ask(self):
        x = int(input("Введите значение координаты х: "))
        y = int(input("Введите значение координаты у: "))
        return Dot(x, y)


# Класс "Game" управляет игрой. Он имеет метод random_board для случайного размещения кораблей на поле,
# метод greet для приветствия игрока, метод loop для основного игрового цикла, и метод start, который запускает игру.

class Game:
    def __init__(self):
        self.user = User()
        self.ai = AI()
        self.user_ships = self.random_board()
        self.ai_ships = self.random_board()

    def random_board(self):
        ships = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        for ship_size in ships:
            while True:
                x = random.randint(0, 6)
                y = random.randint(0, 6)
                direction = random.choice(['horizontal', 'vertical'])
                dot_list = []
                for i in range(ship_size):
                    if direction == 'horizontal':
                        dot = Dot(x + i, y)
                    else:
                        dot = Dot(x, y + i)
                    if board.out(dot):
                        break
                    dot_list.append(dot)
                else:
                    board.place_ship(dot_list)
                    break
        return board

    def greet(self):
        print("Добро пожаловать в игру 'Морской бой'!")

    def loop(self):
        veriable = Board()
        while True:
            print("Таблица игрока:")
            print(self.user.own_board.print_table())
            print("Таблица компьютера:")
            print(self.ai.enemy_board.print_table())

            user_hit = self.user.move()
            ai_hit = self.ai.move()

            if user_hit:
                print("Игрок попал в корабль!")
            else:
                print("Игрок промахнулся!")

            if ai_hit:
                print("Искусственный интеллект попал в корабль!")
            else:
                print("Искусственный интеллект промахнулся!")

            if self.user.own_board.field.count(1) == 0:
                print("Искусственный интеллект побеждает!")
                break
            elif self.ai.own_board.field.count(1) == 0:
                print("Игрок побеждает!")
                break

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
