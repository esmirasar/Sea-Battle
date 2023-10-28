import random

class BoardOutException(Exception):#будет использоваться, когда
    # игрок пытается выстрелить в клетку за пределами поля.
    pass

class DotOccupiedException(Exception): #будет использоваться,
    # когда игрок пытается выстрелить в клетку, которая уже занята.
    pass

class RepeatedShotException(Exception):#будет использоваться,
    # когда игрок попытается выстрелить в клетку, в которую он уже стрелял ранее.
    pass

class ContourOccupiedException(Exception): #будет использоваться,
    # когда игрок попытается разместить судно в контуре, который уже занят другими судами.
    pass


class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def __repr__(self):
        return f'({self.x + 1}, {self.y + 1})'


EMPTY = 'O'
MISS = 'T'
HIT = 'X'
CONTOUR = '*'
SHIP = '■'


class Board:

    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.ships = []

    def add_ship(self, ship):
        # Добавление корабля на поле.
        # Проверяет возможность добавления корабля, проверяя каждую точку корабля на выход за пределы поля,
        # занятость точки другим кораблем и контуром соседнего корабля.
        # Если все точки корабля могут быть добавлены, то добавляет их на поле и в список кораблей.
        for dot in ship.dots():  # Сперва проверяем точки
            if self.out(dot):
                raise BoardOutException(f'Точка: {dot} выходит за пределы доски')
            if self.board[dot.x][dot.y] == SHIP:
                raise DotOccupiedException(f'Точка: {dot} уже занята другим кораблем')
            if self.board[dot.x][dot.y] == CONTOUR:  # Данная проверка никогда не срабатывает
                raise ContourOccupiedException(f'Точка: {dot} является контуром соседнего корабля')
        for dot in ship.dots():  # Далее отдельно проставляем точки
            self.board[dot.x][dot.y] = SHIP
        self.ships.append(ship)
        return True  # Флаг, что корабль успешно поставлен и можно переходить к следующему

    def out(self, dot):
        # Проверяет, выходит ли точка dot за пределы поля.
        return (0 > dot.x > self.size - 1) or (0 > dot.y > self.size - 1)

    def contour(self, dot):  # Обводим точку контуром
        pass

    def shot(self, dot):
        # Выстрел по точке dot.
        # Проверяет, выходит ли точка dot за пределы поля или уже была поражена.
        # Если точка dot содержит корабль, то уменьшает его счетчик жизни.
        # Если счетчик жизни корабля достигает нуля, то выводит сообщение о потоплении корабля.
        # Возвращает True при попадании, False при промахе.
        if self.out(dot):
            raise BoardOutException(f'Точка: {dot} выходит за пределы доски')
        if self.board[dot.x][dot.y] == MISS or self.board[dot.x][dot.y] == HIT:
            raise RepeatedShotException(f'Точка: {dot} уже была поражена ранее')

        if self.board[dot.x][dot.y] == SHIP:
            self.board[dot.x][dot.y] = HIT
            print('Корабль подбит!')
            ship = self._get_ship_by_dot(dot)
            ship.health_count -= 1

            if ship.health_count == 0:
                print('Корабль потоплен!')
            return True  # Попадание
        self.print_board()
        if self.board[dot.x][dot.y] == EMPTY:
            self.board[dot.x][dot.y] = MISS
            return False  # Промах
        self.print_board()



    def all_ships_hit(self):
        # Проверяет, все ли корабли на поле потоплены.
        for ship in self.ships:
            if ship.health_count > 0:
                return False
        return True

    def print_board(self):
        # Выводит состояние игрового поля на экран.
        if not self.hid:
            print('  1 2 3 4 5 6')
            for i in range(len(self.board)):
                print(f'{i + 1}', end=' ')
                print(*self.board[i])

    def _get_ship_by_dot(self, dot):
        # Возвращает корабль, который содержит точку dot.
        for ship in self.ships:
            if dot in ship.dots():
                return ship

    def has_neighboring_ships(self, dot):
        # Проверяет, есть ли соседние корабли вокруг данной точки.
        # return: True, если есть соседние корабли, иначе - False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:  # Пропускаем текущую точку
                    continue
                new_x = dot.x + i
                new_y = dot.y + j
                if (0 <= new_x < self.size) and (0 <= new_y < self.size):
                    if self.board[new_x][new_y] == SHIP:  # Соседняя точка содержит корабль
                        return True
        return False


class Ship:

    def __init__(self, length, nose, direction):
        self.length = length
        self.nose = nose
        self.direction = direction
        self.health_count = length

    def dots(self):
        dots = []
        if self.direction == Direction.Vertical:  # В случае вертикального всегда двигаемся вверх
            for i in range(0, self.length):
                next_dot = Dot(self.nose.x + i, self.nose.y)
                dots.append(next_dot)
        else:
            for i in range(0, self.length):  # В случае горизонтального всегда двигаемся вправо
                next_dot = Dot(self.nose.x, self.nose.y + i)
                dots.append(next_dot)
        return dots

    def __repr__(self):
        return f'Ship[{self.dots()}]'


# Задаем длины кораблей, которые будут использованы в игре
SHIPS_LENGTH = [3, 2, 2, 1, 1, 1, 1]  # [3, 2, 2, 1, 1, 1, 1]

# Максимальное количество попыток заполнения доски
CREATE_BOARD_MAX_RETRY_COUNT = 1000


class Player:

    def __init__(self, own_board, opponent_board):
        self.own_board = own_board
        self.opponent_board = opponent_board

    def ask(self):
        pass

    def name(self):
        pass

    def move(self):
        print(f'Игрок {self.name()} делает ход')
        dot = self.ask()

        try:
            return self.opponent_board.shot(dot)
        except Exception as ex:
            print(ex)
            return True


class User(Player):

    def ask(self):
        x = int(input('Введите координаты x: '))
        y = int(input('Введите координаты y: '))
        return Dot(x - 1, y - 1)


    def name(self):
        return 'User'


class AI(Player):

    def ask(self):
        x = random.randint(0, self.opponent_board.size - 1)
        y = random.randint(0, self.opponent_board.size - 1)
        return Dot(x, y)

    def name(self):
        return 'AI'


class Game:

    def __init__(self):
        # Инициализируем игру (доски, игроков)
        user_board = self.random_board()
        ai_board = self.random_board()
        self.user_board = user_board
        self.ai_board = ai_board
        self.user = User(user_board, ai_board)
        self.ai = AI(ai_board, user_board)

    @staticmethod
    def greet():
        # Приветствие игрока перед началом игры
        print("Добро пожаловать в игру 'Морской бой'!")

    def loop(self):
        while True:
            while True:
                if self.ai_board.all_ships_hit():
                    # Если все корабли AI повреждены, то игрок User победил
                    print('Игрок User одерживает победу! ПОЗДРАВЛЯЕМ!')
                    return
                if not self.user.move():
                    # Если игрок User не может сделать ход, переходим к следующему ходу
                    break
            while True:
                if self.user_board.all_ships_hit():
                    # Если все корабли User повреждены, то AI победил
                    print('Игрок AI одерживает победу! ПОЗДРАВЛЯЕМ!')
                    return
                if not self.ai.move():
                    # Если AI не может сделать ход, переходим к следующему ходу
                    break

    @staticmethod
    def random_board():
        # Генерация случайной доски с расставленными случайным образом кораблями
        board = Board()

        create_board_retry_count = 0
        for curr_length in SHIPS_LENGTH:
            while True:
                if create_board_retry_count == CREATE_BOARD_MAX_RETRY_COUNT:
                    # Если достигнуто максимальное количество попыток, создаем новую доску и начинаем сначала
                    print('Превысили количество попыток заполнения доски, начинаем сначала!')
                    create_board_retry_count = 0
                    board = Board()
                x = random.randint(0, board.size - 1)
                y = random.randint(0, board.size - 1)
                direction = random.choice([Direction.Vertical, Direction.Horizontal])
                ship = Ship(curr_length, Dot(x, y), direction)

                # Проверка на контуры кораблей
                if board.has_neighboring_ships(Dot(x, y)):
                    create_board_retry_count += 1
                    continue

                try:
                    if board.add_ship(ship):
                        break
                except Exception:
                    create_board_retry_count += 1
                    continue
        return board

    def start(self):
        # Запуск игры: приветствие, вывод начальных досок и начало цикла ходов
        self.greet()
        print('Доска User-a!')
        self.user_board.print_board()
        #print('Доска AI')
        #self.ai_board.print_board()
        self.loop()
        print('Игра окончена!')


if __name__ == '__main__':
    game = Game()
    game.start()

