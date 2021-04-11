from .Bishop import bb, bw
from .King import kb, kw
from .Knight import nb, nw
from .Pawn import pb, pw
from .Piece import ChessPiece, em
from .Queen import qb, qw
from .Rook import rb, rw

st_board = [[rw, nw, bw, qw, kw, bw, nw, rw], [pw] * 8, [em] * 8, [em] * 8,
            [em] * 8, [em] * 8, [pb] * 8, [rb, nb, bb, qb, kb, bb, nb, rb]]


class ChessBoard:  # TODO: activate found_moves
    def __init__(self, turn: bool = True, board: list[list] = None, castling: list[list[bool, bool], list[bool, bool]] = None):
        self.found_moves = {}
        self.turn = turn
        self.en_passant = None  # TODO: check inheritance
        self.board = board if board else [[st_board[y][x] for x in range(8)] for y in range(8)]
        self.castling = castling if castling else [[True, True], [True, True]]

    def __getitem__(self, key: tuple[int, int]) -> ChessPiece:
        return self.board[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value: ChessPiece):
        self.board[key[1]][key[0]] = value

    def copy(self):
        return ChessBoard(turn=self.turn, board=[[self[x, y] for x in range(8)] for y in range(8)], castling=self.castling[:])

    def move(self, xy_start: tuple[int, int], xy_end: tuple[int, int], prom: str = None):  # TODO: rework
        dy = 1 if self.turn else -1  # TODO: castling
        if self[xy_start] == 'p' and xy_end == self.en_passant:
            self[self.en_passant[0], self.en_passant[1] - dy] = ChessPiece()
            self.en_passant = None
        elif self[xy_start] == 'p' and abs(xy_start[1] - xy_end[1]) == 2:
            self.en_passant = (xy_start[0], xy_start[1] + dy)
        else:
            self.en_passant = None
        self[xy_start], self[xy_end] = ChessPiece(), self[xy_start]
        if self[xy_end] == 'p' and xy_end[1] == (7 if self.turn else 0):
            if not prom:
                bprint(self)
                prom = input(f'Замена: ').lower()
                while prom not in ['r', 'n', 'b', 'q']:
                    prom = input('Некоректная замена!\nЗамена: ').lower()
            self[xy_end] = [[rb, nb, bb, qb], [rw, nw, bw, qw]][self.turn][['r', 'n', 'b', 'q'].index(prom)]
        elif self[xy_end] == 'k' and abs(xy_start[0] - xy_end[0]) == 2:
            a, b = (7, 5) if xy_end[0] > 4 else (0, 3)
            self[a, xy_end[1]], self[b, xy_end[1]] = ChessPiece(), self[a, xy_end[1]]
        self.found_moves.clear()
        return self

    def is_attacked(self, xy: tuple[int, int], team: bool) -> bool:
        return any(xy in piece.find_moves(self, x, y) for y, line in enumerate(self.board)
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
                    for move in piece.find_moves(self, x, y):
                        if piece == 'p' and move[1] == (7 if self.turn else 0):
                            for prom in ['r', 'n', 'b']:
                                yield self.evolution((x, y), move, prom)
                        yield self.evolution((x, y), move)

    def checkmate(self) -> bool:
        return all(evo.check() for evo in self.evolutions())

    def stalemate(self) -> bool:
        return not any([move for move in piece.find_moves(self, x, y) if not self.evolution((x, y), move).check()]
                       for y, line in enumerate(self.board) for x, piece in enumerate(line) if piece.is_team(self.turn))


def add_history(board: ChessBoard, history: list, move: str, xy_start: tuple[int, int], xy_end: tuple[int, int]):
    if board[xy_start] == 'k' and abs(xy_start[0] - xy_end[0]) == 2:
        move = ('0-0' if xy_start[0] < xy_end[0] else '0-0-0')
    elif board[xy_start] != 'p':
        move = repr(board[xy_start]) + move
    move = f'\033[{3 if board.turn else 9}0m' + move
    move = move.replace(" ", "x" if board[xy_end] and board[xy_start] == "p" and xy_end == board.en_passant else "-")
    if board.turn:
        history.append([move])
    else:
        history[-1] += [move]


def bprint(board: ChessBoard, theme: int = 3, reflection: bool = False, choice: bool = False):
    print()
    print(f'{theme + 1}:' if choice else f"  {'     '.join(' ABCDEFGH')}")
    a, c = (40, 37) if theme < 2 else (47, 30)
    b, d = (107, 90) if theme % 2 else (100, 97)
    for i, line in enumerate(board.board[::-1 if not reflection or board.turn else 1], -8 if not reflection or board.turn else 1):
        print('' if choice else -i if not reflection or board.turn else i, sep='', end='' if choice else ' ')
        for j, piece in enumerate(line):
            print(f'\033[{a if (j + i + 1) % 2 else b}m\033[{c if piece.is_team() else d}m', repr(piece), sep='', end='')
        print(f'\033[0m {"" if choice else -i if not reflection or board.turn else i}')
    print('\n' if choice else f"  {'     '.join(' ABCDEFGH')}")


def choose_theme() -> int:
    board = ChessBoard()
    for i in range(4):
        bprint(board, i, True)
    a = input('Выберите тему: ')
    while not a.isdigit() or not 1 <= int(a) <= 4:
        a = input('Некоректный вход!\nВыберите тему: ')
    return int(a) - 1
