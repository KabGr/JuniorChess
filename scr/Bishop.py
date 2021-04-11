from .Piece import ChessPiece, long_move


class Bishop(ChessPiece):
    def __str__(self) -> str:
        return 'b'

    def __repr__(self) -> str:
        return ' ♝ ' if self.team else ' ♗ '

    def price(self) -> int:
        return 4 if self.is_team() else -4

    def find_moves(self, board, x: int, y: int) -> list[tuple[int, int], ...]:
        team = self.is_team()
        return long_move(board, x, y, team, [(1, 1), (1, -1), (-1, -1), (-1, 1)])


bw = Bishop(True)
bb = Bishop(False)
