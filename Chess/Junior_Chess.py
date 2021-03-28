from datetime import *
from re import match

pieces = [{'k': ' ♚ ', 'q': ' ♛ ', 'r': ' ♜ ', 'b': ' ♝ ', 'n': ' ♞ ', 'p': ' ♟ '},
          {'k': ' ♔ ', 'q': ' ♕ ', 'r': ' ♖ ', 'b': ' ♗ ', 'n': ' ♘ ', 'p': ' ♙ '}]
st_board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p'] * 8, [''] * 8, [''] * 8,
            [''] * 8, [''] * 8, ['p'] * 8, ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]


class ChessBoard:
    def __init__(self, theme: int = 2, reflection: bool = False, turn: bool = True, board: list[list] = None):
        self.theme = theme
        self.reflection = reflection
        self.turn = turn
        self.en_passant = None
        self.found_moves = {}
        self.board = board if board else [[ChessPiece(st_board[y][x], y < 4) if st_board[y][x] else ChessPiece() for x in range(8)] for y in range(8)]

    def __getitem__(self, key: tuple[int, int]):
        return self.board[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value):
        self.board[key[1]][key[0]] = value

    def copy(self):
        return ChessBoard(turn=self.turn, board=[[self[x, y] for x in range(8)] for y in range(8)])

    def move(self, xy_start: tuple[int, int], xy_end: tuple[int, int], prom: str = None):
        dy = 1 if self.turn else -1
        if self[xy_start] == 'p' and xy_end == self.en_passant:
            self[self.en_passant[0], self.en_passant[1] - dy] = ChessPiece()
        self.en_passant = (xy_start[0], xy_start[1] + dy) if self[xy_start] == 'p' and abs(xy_start[1] - xy_end[1]) == 2 else None
        self[xy_start], self[xy_end] = ChessPiece(), self[xy_start]
        if self[xy_end] == 'p' and xy_end[1] == (7 if self.turn else 0):
            self.print()
            prom = prom if prom else input(f'Замена: ').lower()
            while prom not in ['r', 'n', 'b', 'q']:
                prom = input('Некоректная замена!\nЗамена: ').lower()
            self[xy_end] = ChessPiece(prom, self.turn)
        elif self[xy_end] == 'k' and abs(xy_start[0] - xy_end[0]) == 2:
            a, b = 7 if xy_end[0] > 4 else 0, 5 if xy_end[0] > 4 else 3
            self[a, xy_end[1]], self[b, xy_end[1]] = ChessPiece(), self[a, xy_end[1]]
        self.found_moves.clear()
        return self

    def is_attacked(self, xy: tuple[int, int], team: bool) -> bool:
        return any(xy in self.find_moves((x, y)) for y, line in enumerate(self.board)
                   for x, piece in enumerate(line) if piece.is_team(team) and piece != 'k')

    def check(self) -> bool:
        return next(self.is_attacked((x, y), not self.turn) for y, line in enumerate(self.board)
                    for x, piece in enumerate(line) if piece == 'k' and piece.is_team(self.turn))

    def evolution(self, xy_start: tuple[int, int], xy_end: tuple[int, int], prom: str = 'q'):
        return self.copy().move(xy_start, xy_end, prom)

    def evolutions(self):
        for y, line in enumerate(self.board):
            for x, piece in enumerate(line):
                if piece.is_team(self.turn):
                    for move in self.find_moves((x, y)):
                        if piece == 'p' and move[1] == (7 if self.turn else 0):
                            for prom in ['r', 'n', 'b', 'q']:
                                yield self.evolution((x, y), move, prom)
                        else:
                            yield self.evolution((x, y), move)

    def checkmate(self) -> bool:
        return all(evo.check() for evo in self.evolutions())

    def stalemate(self) -> bool:
        return not any([move for move in self.find_moves((x, y)) if not self.evolution((x, y), move).check()]
                       for y, line in enumerate(self.board) for x, piece in enumerate(line) if piece.is_team(self.turn))

    def find_moves(self, xy: tuple[int, int]) -> list[tuple[int, int], ...]:
        def long_move(d_xy: list[tuple[int, int], ...]):
            for d_x, d_y in d_xy:
                for d in range(1, 8):
                    if not (0 <= x + d_x * d < 8 and 0 <= y + d_y * d < 8): break
                    if self[x + d_x * d, y + d_y * d].is_free():
                        moves.append((x + d_x * d, y + d_y * d))
                    elif self[x + d_x * d, y + d_y * d].is_team(not team):
                        moves.append((x + d_x * d, y + d_y * d))
                        break
                    else:
                        break

        if xy in self.found_moves:
            return self.found_moves[xy]

        piece = self[xy]
        x, y = xy
        team, moves = piece.is_team(), []
        if piece == 'p':
            dy = 1 if team else -1
            moves += [(x, y + dy)] if 0 <= y + dy < 8 and self[(x, y + dy)].is_free() else []
            moves += [(x, y + 2 * dy)] if piece.moved and self[(x, y + dy)].is_free() and self[(x, y + 2 * dy)].is_free() else []
            moves += [(x + dx, y + dy) for dx in [-1, 1] if 0 <= x + dx < 8 and 0 <= y + dy < 8 and self[(x + dx, y + dy)].is_team(not team)
                      or (x + dx, y + dy) == self.en_passant]
        elif piece == 'r':
            long_move([(1, 0), (0, 1), (-1, 0), (0, -1)])
        elif piece == 'n':
            ways = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
            moves += [(x + dx, y + dy) for dx, dy in ways if 0 <= x + dx < 8 and 0 <= y + dy < 8 and not self[(x + dx, y + dy)].is_team(team)]
        elif piece == 'b':
            long_move([(1, 1), (1, -1), (-1, -1), (-1, 1)])
        elif piece == 'q':
            long_move([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)])
        elif piece == 'k':
            ways = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
            moves += [(x + dx, y + dy) for dx, dy in ways if 0 <= x + dx < 8 and 0 <= y + dy < 8 and not self[(x + dx, y + dy)].is_team(team) and
                      not self.is_attacked((x + dx, y + dy), not team)]
            moves += [(2 if dx else 6, y) for dx in [0, 1] if piece.moved and self[(0 if dx else 7, y)].moved and
                      all(self[(d, y)].is_free() for d in ([1, 2, 3] if dx else [5, 6])) and
                      all(not self.is_attacked((d, y), not team) for d in ([2, 3, 4] if dx else [4, 5, 6]))]
        self.found_moves[xy] = moves
        return moves

    def add_history(self, history: list, move: str, xy_start: tuple[int, int], xy_end: tuple[int, int]):
        if self[xy_start] == 'k' and abs(xy_start[0] - xy_end[0]) == 2:
            move = ('0-0' if xy_start[0] < xy_end[0] else '0-0-0')
        elif str(self[xy_start]) != 'p':
            move = pieces[self[xy_start].is_team()][str(self[xy_start])] + move
        move = f'\033[{3 if self.turn else 9}0m' + move
        move = move.replace(" ", "-" if self[xy_end].is_free() and not (self[xy_start] == "p" and xy_end == self.en_passant) else "x")
        if self.turn:
            history.append([move])
        else:
            history[-1] += [move]

    def print(self, choice: bool = False):
        print()
        print(f'{self.theme + 1}:' if choice else f"  {'     '.join(' ABCDEFGH')}")
        a, c = (40, 37) if self.theme < 2 else (47, 30)
        b, d = (107, 90) if self.theme % 2 else (100, 97)
        for i, line in enumerate(self.board[::-1 if not self.reflection or self.turn else 1], -8 if not self.reflection or self.turn else 1):
            print('' if choice else -i if not self.reflection or self.turn else i, sep='', end='' if choice else ' ')
            for j, piece in enumerate(line):
                print(f'\033[{a if (j + i + 1) % 2 else b}m\033[{c if piece.is_team() else d}m', repr(piece), sep='', end='')
            print(f'\033[0m {"" if choice else -i if not self.reflection or self.turn else i}')
        print('\n' if choice else f"  {'     '.join(' ABCDEFGH')}")

    def console(self):
        while True:
            command = input('Console: ').lower()
            if command == 'set':
                name, xy, team = input('name, xy, team: ').lower().split()
                xy, team = (ord(xy[0]) - 97, int(xy[1]) - 1), team == 'w'
                self[xy] = ChessPiece(name, team)
            elif command == 'get':
                xy = input('xy: ').lower()
                xy = ord(xy[0]) - 97, int(xy[1]) - 1
                print(self[xy])
            elif command == 'del':
                xy = input('xy: ').lower()
                xy = ord(xy[0]) - 97, int(xy[1]) - 1
                self[xy] = ChessPiece()
            elif command == 'moves':
                xy = input('xy: ').lower()
                xy = ord(xy[0]) - 97, int(xy[1]) - 1
                print(None if self[xy].is_free() else self.find_moves(xy))
            elif command == 'attacked':
                xy, team = input('xy, team: ').lower().split()
                xy, team = (ord(xy[0]) - 97, int(xy[1]) - 1), team == 'w'
                print(self.is_attacked(xy, team))
            elif command == 'board':
                print(self)
            elif command == 'help':
                print(f"Commands: {['set', 'get', 'del', 'moves', 'board', 'help', 'exit']}")
            elif command == 'exit':
                break
            else:
                print('Некоректный ввод!')


class ChessPiece:
    def __init__(self, name: str = None, team: bool = None):
        self.name = name
        self.team = team
        self.moved = True if name in ['p', 'r', 'k'] else None

    def __str__(self) -> str:
        return self.name if self.name else ' '

    def __repr__(self) -> str:
        return '   ' if not self else pieces[self.is_team()][str(self)]

    def __eq__(self, other: str) -> bool:
        return str(self) == other

    def __ne__(self, other: str) -> bool:
        return str(self) != other

    def __bool__(self):
        return bool(self.name)

    def is_free(self) -> bool:
        return not self.name

    def is_team(self, team: bool = True) -> bool:
        return self.team is not None and self.team == team


def choose_theme() -> int:
    board = ChessBoard()
    for i in range(4):
        board.theme = i
        board.print(True)
    a = input('Выберите тему: ')
    while not a.isdigit() or not 1 <= int(a) <= 4:
        a = input('Некоректный вход!\nВыберите тему: ')
    return int(a) - 1


def start_game(timer: str = None, theme: int = 3, reflection: bool = False, board: ChessBoard = None):
    if board is None:
        board = ChessBoard(theme, reflection)
    add = 0
    if timer:
        timer, add = map(int, timer.split('+'))
        add, timer = timedelta(seconds=add), [timedelta(minutes=timer), timedelta(minutes=timer)]
    fifty_moves, check, history, start = 100, '', [], False
    while True:  # TODO: PyGame
        board.print()
        if timer:
            if start: timer[board.turn] -= datetime.now() - start
            m, s = timer[board.turn].seconds // 60, timer[board.turn].seconds % 60
            print(f'У вас осталось {f"{m} мин" if m else ""}{" и " if m and s else ""}{f"{s} сек" if s or not m else ""}.')
        start, move = datetime.now(), input(f'{check}Ход {"Белых" if board.turn else "Чёрных"}: ').lower()
        if move == 'console':
            board.console()
        elif move == 'give up':
            print(f'\nПобедили {"Белые" if not board.turn else "Чёрные"}!')
            break
        elif timer[board.turn].total_seconds() <= 0:
            print(f'\nУ {"Белых" if board.turn else "Чёрных"} закончилась время!\nПобедили {"Белые" if not board.turn else "Чёрные"}!')
            break
        elif move == 'draw':
            ans = input(f'\n{"Белые" if board.turn else "Чёрные"} предлагаю ничью, вы принимаете её?: ').lower()
            while ans not in ['y', 'yes', 'accept', 'n', 'no', 'deny']:
                ans = input(f'Некоректный ввод!\n\n{"Белые" if board.turn else "Чёрные"} предлагаю ничью, вы принимаете её?: ').lower()
            if ans in ['y', 'yes', 'accept']:
                print('\nНичья!')
                break
            print('Ничья отклонена!')
        elif fifty_moves <= 0:
            print('\nНичья по правилу 50 ходов!')
            break
        elif match(r'[a-h][1-8] [a-h][1-8]$', move):
            xy_start, xy_end = map(lambda x: (ord(x[0]) - 97, int(x[1]) - 1), move.split())
            if board[xy_start].is_team(board.turn) and xy_end in board.find_moves(xy_start) and not board.evolution(xy_start, xy_end).check():
                if timer:
                    timer[board.turn] += add + start - datetime.now()
                    start = False
                board.add_history(history, move, xy_start, xy_end)
                p = board[xy_start] == 'p' and xy_end[1] == (7 if board.turn else 0)
                fifty_moves = fifty_moves - 1 if board[xy_start] != 'p' and board[xy_end].is_free() else 100
                board.move(xy_start, xy_end)
                board[xy_start].moved = False
                board.turn = not board.turn
                history[-1][board.turn] += pieces[board[xy_end].is_team()][str(board[xy_end])] if p else ''
                if board.check():
                    check = f'Шах {"Белым" if board.turn else "Чёрным"}!\n'
                    if board.checkmate():
                        history[-1][board.turn] += '#'
                        print(f'\nШах и мат!\nПобедили {"Белые" if not board.turn else "Чёрные"}!')
                        break
                    history[-1][board.turn] += '+'
                elif board.stalemate():
                    print(f'\nПат {"Белым" if board.turn else "Чёрным"}!')
                    break
            else:
                print('Некоректный ход!')
        else:
            print('Некоректный вход!')

    input()
    print('История:')
    for i, move in enumerate(history, 1):
        print(f'\033[0m{i}.', *move)


if __name__ == '__main__':
    start_game(timer=input('Таймер: '))
