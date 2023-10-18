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
'''Метод `add_ship`принимает объект `ship`, представляющий корабль, и добавляет его на доску.
Сначала метод проверяет, возможно ли разместить корабль на указанных позициях. Если невозможно, выбрасывается исключение.
Затем метод обновляет состояние каждой клетки на доске, отмечая их как занятые кораблем.
Также метод добавляет корабль в список `ships` и увеличивает счетчик живых кораблей на доске.

Метод `contour` принимает объект `ship` и контурирует его на доске.Метод перебирает 
каждую позицию корабля и обновляет состояние соседних клеток на доске, 
помечая их как недопустимые для размещения корабля (как 'О').

Метод `out` проверяет, выходит ли заданная точка (`dot`) за пределы поля доски.
Если координаты `dot` выходят за пределы 6х6, то метод возвращает True, иначе - False.



Метод `shot`делает выстрел по точке `dot` на доске.
Если точка `dot` выходит за пределы доски или уже была использована (точка содержит '.'), метод выбрасывает исключение.
Если точка содержит символ '■', значит эта точка представляет корабль, и он будет помечен как 'X'.
Если точка содержит символ 'О', то это пустая клетка, и она будет помечена как '.'.

Метод `print_ship`устанавливает начальную расстановку кораблей на доске.
Он вызывает метод `add_ship` для добавления кораблей заданного размера и расположения на доску
'''


class Board:
    def __init__(self):
        self.size = 6
        self.board = [['О' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
        self.hide_ships = True
        self.num_of_alive_ships = 0

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot) or self.board[dot.x][dot.y] != 'О':
                raise Exception("Невозможно поставить корабль на эту позицию")
            if self.board[dot.x][dot.y] == '■':  # проверка на занятость точки другим кораблем или его контуром
                raise ValueError("Точка корабля занята другим кораблём или его контуром")

            self.board[dot.x][dot.y] = '■'
            self.ships.append(ship)
            self.num_of_alive_ships += 1
            self.contour(ship)

    def contour(self, ship):
        for dot in ship.dots():
            for i in range(dot.x - 1, dot.x + 2):
                for j in range(dot.y - 1, dot.y + 2):
                    if not self.out(Dot(i, j)):
                        if self.board[i][j] != '■':
                            self.board[i][j] = 'О'

    def out(self, dot):
        return dot.x < 0 or dot.x >= 6 or dot.y < 0 or dot.y >= 6

    def print_board(self):
        print('   1 2 3 4 5 6')
        for i in range(len(self.board)):
            row_str = str(i) + '  '
            for j in range(len(self.board[i])):
                row_str += self.board[i][j] + ' '
            print(row_str)

    def shot(self, dot):
        if self.out(dot) or self.board[dot.x][dot.y] == 'T':
            raise Exception("Невозможно выстрелить по этой точке")
        if self.board[dot.x][dot.y] == '■':
            self.board[dot.x][dot.y] = 'X'
        if self.board[dot.x][dot.y] == 'О':
            self.board[dot.x][dot.y] = 'T'

    def place_ships(self):
        self.add_ship(Ship(3, Dot(1, 1), 'горизонтальное'))
        self.add_ship(Ship(2, Dot(4, 2), 'вертикальное'))
        self.add_ship(Ship(2, Dot(2, 5), 'горизонтальное'))
        self.add_ship(Ship(1, Dot(0, 4), 'горизонтальное'))
        self.add_ship(Ship(1, Dot(1, 3), 'горизонтальное'))
        self.add_ship(Ship(1, Dot(5, 5), 'горизонтальное'))
        self.add_ship(Ship(1, Dot(5, 0), 'горизонтальное'))


# Класс "Player" - класс для игроков.
# У него есть методы move, который выполняет ход игрока, и ask, который запрашивает у пользователя координаты выстрела.

class Player:
    def __init__(self, player_board, enemy_board):
        player_board = Board()
        enemy_board = Board()
        self.player_board = player_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                self.enemy_board.shot(target)
                return True
            except Exception as e:
                print(e)
                continue


class AI(Player):
    def ask(self):
        # генерируем случайные координаты для выстрела
        x = random.randint(0, self.enemy_board.size - 1)
        y = random.randint(0, self.enemy_board.size - 1)
        return Dot(x, y)


class User(Player):
    def ask(self):
        # запрашиваем координаты у пользователя
        x = int(input("Введите координаты x: "))
        y = int(input("Введите координаты y: "))
        return Dot(x, y)


# Класс "Game" управляет игрой. Он имеет метод random_board для случайного размещения кораблей на поле,
# метод greet для приветствия игрока, метод loop для основного игрового цикла, и метод start, который запускает игру.

class Game:
    def __init__(self):
        user_board = Board()
        ai_board = Board()
        self.user_board = User(user_board, ai_board)
        self.ai_board = AI(ai_board, user_board)

    def random_board(self):
        # генерация доски пользователя
        while True:
            try:
                self.user_board.__init__()
                self.user_board.place_ships()
                break
            except Exception:
                continue

        # генерация случайной доски компьютера

    def generate_board(self):

        while True:  # Организуем цикл для автоматического перезапуска, если корабли не помещаются
            board = Board()  # Создаем новую доску
            ships = []

        # Создаем корабли заданных размеров
            ship_lengths = [3, 2, 2, 1, 1, 1, 1]

            try:
            # Добавляем корабли на доску
                for length in ship_lengths:
                    while True:
                    # Генерируем случайные координаты для первой точки корабля
                        x = random.randint(0, board.size - 1)
                        y = random.randint(0, board.size - 1)
                        direction = random.choice(['вертикальное', 'горизонтальное'])

                        bow_of_the_ship = Dot()
                        bow_of_the_ship.init(x, y)

                    # Создаем корабль с заданной длиной, начальной точкой и направлением
                        ship = Ship()
                        ship.init(length, bow_of_the_ship, direction)

                    # Проверяем, возможно ли добавить корабль на доску
                        board.add_ship(ship)
                    # Если удалось успешно добавить корабль, выходим из цикла
                        break

            # Если успешно создали и разместили все корабли, возвращаем доску
                return board
            except:
                continue

    def greet(self):
        print("Добро пожаловать в игру 'Морской бой'!\n")
        print("Формат ввода координат: x y")

    def loop(self):
        while self.user_board.num_of_alive_ships > 0 and self.ai_board.num_of_alive_ships > 0:
            print("Ход пользователя:")
            self.user.shoot(self.ai_board)
            self.ai_board.print_board()
            if self.ai_board.num_of_alive_ships == 0:
                print("Победа пользователя!")
                break

            print("Ход компьютера:")
            self.ai.shoot(self.user_board)
            self.user_board.print_board()
            if self.user_board.num_of_alive_ships == 0:
                print("Победа компьютера!")
                break




    def start(self):
        self.greet()
        self.random_board()
        self.generate_board()
        self.random_ships_board()
        self.loop()

board = Board()
board.place_ships()
board.print_board()
game = Game()
game.start()
