class ChessBoard:
    def __init__(self, symbol=' '):
        self.turn = True
        self.sym = symbol
        self.board = [[ChessPiece()] * 8 for _ in range(8)]
        [self.team_init(team) for team in range(2)]

    def __str__(self):
        s = [self.sym.join(' ABCDEFGH')]
        return '\n'.join(s + [str(8 - i) + self.sym + self.sym.join(map(lambda x: (str(x).upper() if x.is_team() else str(x)), self.board[7 - i]))
                              for i in range(8)])

    def __getitem__(self, key):
        return self.board[key[1]][key[0]]

    def __setitem__(self, key, value):
        self.board[key[1]][key[0]] = value

    def team_init(self, team):
        y, piece = (0 if team else 7, 1 if team else 6), [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p'] * 8]
        for i in range(2): self.board[y[i]] = [ChessPiece(piece[i][x], (x, y[i]), team) for x in range(8)]

    def is_en_passant(self, xy_start, xy_end):
        if str(self[xy_start]) == 'p' and abs(xy_start[1] - xy_end[1]) == 2:
            return xy_start[0], xy_start[1] + (1 if self.turn else -1)

    def promotion(self, xy_end):
        if str(self[xy_end]) == 'p' and xy_end[1] == (7 if self.turn else 0):
            prom = input(str(self) + '\nЗамена: ').lower()
            while prom not in ['b', 'r', 'q']:
                prom = input('Некоректная замена!\nЗамена: ').lower()
            self[xy_end] = ChessPiece(prom, xy_end, self.turn)

    def castling(self, xy_start, xy_end):
        if str(self[xy_start]) == 'k' and abs(xy_start[0] - xy_end[0]) == 2:
            a, b = 7 if xy_end[0] > 4 else 0, 5 if xy_end[0] > 4 else 3
            self[(a, xy_end[1])], self[(b, xy_end[1])] = ChessPiece(), self[(a, xy_end[1])]

    def find_pieces(self, name, team):
        return [i for j in self.board for i in j if str(i) == name and i.is_team(team)]

    def is_attacked(self, xy, team, en_passant):
        return any(map(lambda x: xy in x.find_moves(self, en_passant),
                       filter(lambda x: x.is_team(team) and str(x) != 'k', (i for j in self.board for i in j))))

    def console(self, en_passant):
        while True:
            command = input('Console: ').lower()
            if command == 'set':
                name, xy, team = input('name, xy, team: ').lower().split()
                xy, team = (ord(xy[0]) - 97, int(xy[1]) - 1), team == 'w'
                self[xy] = ChessPiece(name, xy, team)
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
                print(None if self[xy].is_free() else self[xy].find_moves(self, en_passant))
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
    def __init__(self, name=None, xy=None, team=None):
        self.name = name
        self.xy = xy
        self.team = team
        self.moved = True if name in ['p', 'r', 'k'] else None

    def __str__(self):
        return self.name if self.name else '.'

    def is_free(self):
        return not self.name

    def is_team(self, team=True):
        return self.team is not None and self.team == team

    def is_attacked(self, board, en_passant):
        return board.is_attacked(self.xy, board.turn, en_passant)

    def move(self, xy):
        self.xy = xy
        if self.name in ['p', 'r', 'k']:
            self.moved = False

    def find_moves(self, board, en_passant):
        def long_move(xy_lambdas):
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

        x, y = self.xy
        turn, moves = board.turn, []
        if str(self) == 'p':
            dy = 1 if turn else -1
            moves += [(x, y + dy)] if 0 <= y + dy < 8 and board[(x, y + dy)].is_free() else []
            moves += [(x, y + 2 * dy)] if self.moved and board[(x, y + dy)].is_free() and board[(x, y + 2 * dy)].is_free() else []
            moves += [(x + dx, y + dy) for dx in [-1, 1] if 0 <= x + dx < 8 and 0 <= y + dy < 8 and not board[(x + dx, y + dy)].is_team(turn)
                      and (str(board[(x + dx, y + dy)]) not in ['.', 'k'] or (x + dx, y + dy) == en_passant)]
        elif str(self) == 'r':
            long_move([(lambda xl, dl: xl + dl, lambda yl, dl: yl), (lambda xl, dl: xl, lambda yl, dl: yl + dl),
                       (lambda xl, dl: xl - dl, lambda yl, dl: yl), (lambda xl, dl: xl, lambda yl, dl: yl - dl)])
        elif str(self) == 'n':
            ways = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
            moves += [(x + dx, y + dy) for dx, dy in ways if 0 <= x + dx < 8 and 0 <= y + dy < 8 and
                      (not board[(x + dx, y + dy)].is_team(turn) or board[(x + dx, y + dy)].is_free())]
        elif str(self) == 'b':
            long_move([(lambda xl, dl: xl + dl, lambda yl, dl: yl + dl), (lambda xl, dl: xl + dl, lambda yl, dl: yl - dl),
                       (lambda xl, dl: xl - dl, lambda yl, dl: yl - dl), (lambda xl, dl: xl - dl, lambda yl, dl: yl + dl)])
        elif str(self) == 'q':
            long_move([(lambda xl, dl: xl + dl, lambda yl, dl: yl), (lambda xl, dl: xl - dl, lambda yl, dl: yl),
                       (lambda xl, dl: xl, lambda yl, dl: yl + dl), (lambda xl, dl: xl, lambda yl, dl: yl - dl),
                       (lambda xl, dl: xl + dl, lambda yl, dl: yl + dl), (lambda xl, dl: xl + dl, lambda yl, dl: yl - dl),
                       (lambda xl, dl: xl - dl, lambda yl, dl: yl - dl), (lambda xl, dl: xl - dl, lambda yl, dl: yl + dl)])
        elif str(self) == 'k':
            ways = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
            moves += [(x + dx, y + dy) for dx, dy in ways if 0 <= x + dx < 8 and 0 <= y + dy < 8 and
                      (not board[(x + dx, y + dy)].is_team(turn) or board[(x + dx, y + dy)].is_free()) and
                      not board.is_attacked((x + dx, y + dy), not turn, en_passant)]
            moves += [(2 if dx else 6, y) for dx in [0, 1] if self.moved and board[(0 if dx else 7, y)].moved and
                      all(board[(d, y)].is_free() for d in ([1, 2, 3] if dx else [5, 6])) and
                      all(not board.is_attacked((d, y), not turn, en_passant) for d in ([2, 3, 4] if dx else [4, 5, 6]))]
        return moves


def start_game(board=None):
    if board is None: board = ChessBoard()
    move = input(str(board) + '\nХод Белых: ').lower()
    history, en_passant = [], None
    while move != 'Give up':
        try:
            if move == 'console':
                board.console(en_passant)
                move = input(str(board) + f'\nХод {"Белых" if board.turn else "Чёрных"}: ')
                continue
            xy_start, xy_end = move.split()
            xy_start = ord(xy_start[0]) - 97, int(xy_start[1]) - 1
            xy_end = ord(xy_end[0]) - 97, int(xy_end[1]) - 1
            if not board[xy_start].is_free() and board[xy_start].is_team(board.turn) and xy_end in board[xy_start].find_moves(board, en_passant):
                if xy_end == en_passant: board[en_passant[0], en_passant[1] - (1 if board.turn else -1)] = ChessPiece()
                en_passant = board.is_en_passant(xy_start, xy_end)
                board.castling(xy_start, xy_end)
                board[xy_start].move(xy_end)
                board[xy_start], board[xy_end] = ChessPiece(), board[xy_start]
                board.promotion(xy_end)
                if board.find_pieces('k', not board.turn)[0].is_attacked(board, en_passant):
                    print(f'Шах {"Белым" if not board.turn else "Чёрным"}!')
                history.append((f'{"W" if board.turn else "B"}', move))
                board.turn = not board.turn
            else:
                print('Некоректный ход!')
        except (ValueError, IndexError):
            print('Некоректный вход!')
        move = input(str(board) + f'\nХод {"Белых" if board.turn else "Чёрных"}: ')
    print(history)


start_game()
