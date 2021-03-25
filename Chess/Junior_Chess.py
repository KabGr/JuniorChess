from typing import Optional


class ChessBoard:
    def __init__(self, theme: int = 2):
        self.turn = True
        self.theme = theme
        self.board = [[ChessPiece()] * 8 for _ in range(8)]
        [self.team_init(team) for team in [True, False]]

    def __getitem__(self, key: tuple[int, int]):
        return self.board[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value):
        self.board[key[1]][key[0]] = value

    def __str__(self) -> str:
        s = [' '.join(' ABCDEFGH')]
        return '\n'.join(s + [f'{8 - i} {" ".join(str(j).upper() if j.is_team() else str(j) for j in self.board[7 - i])}' for i in range(8)])

    def print(self, choice=False):
        print()
        print(f'{self.theme + 1}:' if choice else ' '.join(' ABCDEFGH'))
        a, c = (40, 37) if self.theme < 2 else (47, 30)
        b, d = (107, 90) if self.theme % 2 else (100, 97)
        for i, line in enumerate(self.board[::-1], -8):
            print('' if choice else -i, sep='', end='' if choice else ' ')
            for j, piece in enumerate(line):
                print(f'\033[1m\033[{a if (j + i + 1) % 2 else b}m\033[{c if piece.is_team() else d}m', piece.upper(), sep='', end=' ')
            print('\033[0m')

    def team_init(self, team: bool):
        y = (0 if team else 7, 1 if team else 6)
        for i, piece in enumerate([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p'] * 8]):
            self.board[y[i]] = [ChessPiece(piece[x], team) for x in range(8)]

    def move(self, xy_start: tuple[int, int], xy_end: tuple[int, int]):
        self[xy_start], self[xy_end] = ChessPiece(), self[xy_start]

    def is_en_passant(self, xy_start: tuple[int, int], xy_end: tuple[int, int], en_passant: tuple[int, int]) -> Optional[tuple[int, int]]:
        if xy_end == en_passant:
            self[en_passant[0], en_passant[1] - (1 if self.turn else -1)] = ChessPiece()
        elif self[xy_start] == 'p' and abs(xy_start[1] - xy_end[1]) == 2:
            return xy_start[0], xy_start[1] + (1 if self.turn else -1)

    def promotion(self, xy_end: tuple[int, int]):
        if self[xy_end] == 'p' and xy_end[1] == (7 if self.turn else 0):
            self.print()
            prom = input(f'Замена: ').lower()
            while prom not in ['b', 'r', 'q']:
                prom = input('Некоректная замена!\nЗамена: ').lower()
            self[xy_end] = ChessPiece(prom, self.turn)

    def castling(self, xy_start: tuple[int, int], xy_end: tuple[int, int]):
        if self[xy_start] == 'k' and abs(xy_start[0] - xy_end[0]) == 2:
            a, b = 7 if xy_end[0] > 4 else 0, 5 if xy_end[0] > 4 else 3
            self[(a, xy_end[1])], self[(b, xy_end[1])] = ChessPiece(), self[(a, xy_end[1])]

    def is_attacked(self, xy: tuple[int, int], team: bool, en_passant: tuple[int, int] = None) -> bool:
        return any(xy in find_moves(self, (x, y), en_passant) for y, line in enumerate(self.board)
                   for x, piece in enumerate(line) if piece.is_team(team) and piece != 'k')

    def king_is_attacked(self) -> bool:
        return next(self.is_attacked((x, y), self.turn) for y, line in enumerate(self.board)
                    for x, piece in enumerate(line) if piece == 'k' and piece.is_team(not self.turn))

    def draw(self) -> bool:
        ans = input(f'\n{"Белые" if self.turn else "Чёрные"} предлагаю ничью, вы принимаете её?: ').lower()
        while ans not in ['y', 'yes', 'accept', 'n', 'no', 'deny']:
            ans = input(f'Некоректный ввод!\n\n{"Белые" if self.turn else "Чёрные"} предлагаю ничью, вы принимаете её?: ').lower()
        return ans in ['y', 'yes', 'accept']

    def console(self, en_passant: tuple[int, int]):
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
                print(None if self[xy].is_free() else find_moves(self, xy, en_passant))
            elif command == 'attacked':
                xy, team = input('xy, team: ').lower().split()
                xy, team = (ord(xy[0]) - 97, int(xy[1]) - 1), team == 'w'
                print(self.is_attacked(xy, team, en_passant))
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

    def __eq__(self, other: str) -> bool:
        return str(self) == other

    def __ne__(self, other: str) -> bool:
        return str(self) != other

    def upper(self) -> str:
        return str(self).upper()

    def is_free(self) -> bool:
        return not self.name

    def is_team(self, team: bool = True) -> bool:
        return self.team is not None and self.team == team


def find_moves(board: ChessBoard, xy: tuple[int, int], en_passant: tuple[int, int] = None) -> list[tuple[int, int], ...]:
    def long_move(xy_lambdas: list[tuple]):
        for x_lambda, y_lambda in xy_lambdas:
            for d in range(1, 8):
                if not (0 <= x_lambda(x, d) < 8 and 0 <= y_lambda(y, d) < 8): break
                if board[(x_lambda(x, d), y_lambda(y, d))].is_free():
                    moves.append((x_lambda(x, d), y_lambda(y, d)))
                elif not board[(x_lambda(x, d), y_lambda(y, d))].is_team(turn):
                    moves.append((x_lambda(x, d), y_lambda(y, d)))
                    break
                else:
                    break

    piece = board[xy]
    x, y = xy
    turn, moves = board.turn, []
    if piece == 'p':
        dy = 1 if turn else -1
        moves += [(x, y + dy)] if 0 <= y + dy < 8 and board[(x, y + dy)].is_free() else []
        moves += [(x, y + 2 * dy)] if piece.moved and board[(x, y + dy)].is_free() and board[(x, y + 2 * dy)].is_free() else []
        moves += [(x + dx, y + dy) for dx in [-1, 1] if 0 <= x + dx < 8 and 0 <= y + dy < 8 and not board[(x + dx, y + dy)].is_team(turn)
                  and (str(board[(x + dx, y + dy)]) not in [' ', 'k'] or (x + dx, y + dy) == en_passant)]
    elif piece == 'r':
        long_move([(lambda xl, dl: xl + dl, lambda yl, dl: yl), (lambda xl, dl: xl, lambda yl, dl: yl + dl),
                   (lambda xl, dl: xl - dl, lambda yl, dl: yl), (lambda xl, dl: xl, lambda yl, dl: yl - dl)])
    elif piece == 'n':
        ways = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        moves += [(x + dx, y + dy) for dx, dy in ways if 0 <= x + dx < 8 and 0 <= y + dy < 8 and
                  (not board[(x + dx, y + dy)].is_team(turn) or board[(x + dx, y + dy)].is_free())]
    elif piece == 'b':
        long_move([(lambda xl, dl: xl + dl, lambda yl, dl: yl + dl), (lambda xl, dl: xl + dl, lambda yl, dl: yl - dl),
                   (lambda xl, dl: xl - dl, lambda yl, dl: yl - dl), (lambda xl, dl: xl - dl, lambda yl, dl: yl + dl)])
    elif piece == 'q':
        long_move([(lambda xl, dl: xl + dl, lambda yl, dl: yl), (lambda xl, dl: xl - dl, lambda yl, dl: yl),
                   (lambda xl, dl: xl, lambda yl, dl: yl + dl), (lambda xl, dl: xl, lambda yl, dl: yl - dl),
                   (lambda xl, dl: xl + dl, lambda yl, dl: yl + dl), (lambda xl, dl: xl + dl, lambda yl, dl: yl - dl),
                   (lambda xl, dl: xl - dl, lambda yl, dl: yl - dl), (lambda xl, dl: xl - dl, lambda yl, dl: yl + dl)])
    elif piece == 'k':
        ways = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        moves += [(x + dx, y + dy) for dx, dy in ways if 0 <= x + dx < 8 and 0 <= y + dy < 8 and
                  (not board[(x + dx, y + dy)].is_team(turn) or board[(x + dx, y + dy)].is_free()) and
                  not board.is_attacked((x + dx, y + dy), not turn, en_passant)]
        moves += [(2 if dx else 6, y) for dx in [0, 1] if piece.moved and board[(0 if dx else 7, y)].moved and
                  all(board[(d, y)].is_free() for d in ([1, 2, 3] if dx else [5, 6])) and
                  all(not board.is_attacked((d, y), not turn, en_passant) for d in ([2, 3, 4] if dx else [4, 5, 6]))]
    return moves


def start_game(theme: int = False, board: ChessBoard = None):
    if board is None:
        board = ChessBoard(theme)
    board.print()
    move = input(f'Ход Белых: ').lower()
    check, history, en_passant = '', [], None
    while move != 'give up':
        if move == 'console':
            board.console(en_passant)
        elif move == 'draw':
            if board.draw():
                break
            print('Ничья отклонена!')
        # elif re.match(r'see [a-h][1-8]$', move):
        #     pass
        else:
            try:
                xy_start, xy_end = move.split()
                xy_start = ord(xy_start[0]) - 97, int(xy_start[1]) - 1
                xy_end = ord(xy_end[0]) - 97, int(xy_end[1]) - 1
                if not board[xy_start].is_free() and board[xy_start].is_team(board.turn) and xy_end in find_moves(board, xy_start, en_passant):
                    en_passant = board.is_en_passant(xy_start, xy_end, en_passant)
                    board.castling(xy_start, xy_end)
                    board.move(xy_start, xy_end)
                    board.promotion(xy_end)
                    check = f'Шах {"Белым" if not board.turn else "Чёрным"}!\n' if board.king_is_attacked() else ''
                    history.append((f'{"W" if board.turn else "B"}', move))
                    board.turn = not board.turn
                else:
                    print('Некоректный ход!')
            except (ValueError, IndexError):
                print('Некоректный вход!')
        board.print()
        move = input(f'{check}Ход {"Белых" if board.turn else "Чёрных"}: ').lower()
    if move == 'give up':
        print(f'\nПобедили {"Белый" if not board.turn else "Чёрный"}!')
    elif move == 'draw':
        print(f'\nНичья!')
    print(f'History: {history}')


def choose_theme() -> int:
    board = ChessBoard()
    for i in range(4):
        board.theme = i
        board.print(True)
        print()
    a = input('Выберите тему: ')
    while not a.isdigit() or not 1 <= int(a) <= 4:
        a = input('Некоректный вход!\nВыберите тему: ')
    return int(a) - 1


if __name__ == '__main__':
    start_game(choose_theme())
