from .Piece import ChessPiece, long_move


class Queen(ChessPiece):
    def __str__(self) -> str:
        return 'q'

    def __repr__(self) -> str:
        return ' ♛ ' if self.team else ' ♕ '

    def price(self) -> int:
        return 10 if self.is_team() else -10

    def find_moves(self, board, x: int, y: int) -> list[tuple[int, int], ...]:
        team = self.is_team()
        return long_move(board, x, y, team, [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)])


qw = Queen(True)
qb = Queen(False)
