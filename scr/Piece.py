class ChessPiece:
    def __init__(self, team: bool = None):
        self.team = team

    def __str__(self) -> str:
        return ' '

    def __repr__(self) -> str:
        return '   '

    def __eq__(self, other: str) -> bool:
        return str(self) == other

    def __ne__(self, other: str) -> bool:
        return str(self) != other

    def __bool__(self) -> bool:
        return self.team is not None

    def is_team(self, team: bool = True) -> bool:
        return self.team == team

    def price(self) -> int:
        return 0

    def find_moves(self, board, x: int, y: int) -> list[tuple[int, int], ...]:
        return []


def long_move(board, x: int, y: int, team: bool, directs: list[tuple[int, int], ...]) -> list[tuple[int, int], ...]:
    for d_x, d_y in directs:
        for d in range(1, 8):
            x_cur, y_cur = x + d_x * d, y + d_y * d
            if not (0 <= x_cur < 8 and 0 <= y_cur < 8):
                break
            elif board[x_cur, y_cur]:
                if board[x_cur, y_cur].is_team(not team):
                    yield x_cur, y_cur
                break
            yield x_cur, y_cur


em = ChessPiece()
