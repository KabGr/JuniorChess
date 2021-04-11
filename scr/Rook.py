from .Piece import ChessPiece, long_move


class Rook(ChessPiece):
    def __str__(self) -> str:
        return 'r'

    def __repr__(self) -> str:
        return ' ♜ ' if self.team else ' ♖ '

    def price(self) -> int:
        return 1 if self.is_team() else -1

    def find_moves(self, board, x: int, y: int) -> list[tuple[int, int], ...]:
        team = self.is_team()
        return long_move(board, x, y, team, [(1, 0), (0, 1), (-1, 0), (0, -1)])


rw = Rook(True)
rb = Rook(False)
