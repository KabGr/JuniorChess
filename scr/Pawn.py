from .Piece import ChessPiece


class Pawn(ChessPiece):
    def __str__(self) -> str:
        return 'p'

    def __repr__(self) -> str:
        return ' ♟ ' if self.team else ' ♙ '

    def price(self) -> int:
        return 1 if self.is_team() else -1

    def find_moves(self, board, x: int, y: int) -> list[tuple[int, int], ...]:
        team = self.is_team()
        dy = 1 if team else -1
        return ([(x, y + dy)] if not board[(x, y + dy)] else []) + \
               ([(x, y + 2 * dy)] if (y == 1 if team else y == 6) and not board[(x, y + dy)] and not board[(x, y + 2 * dy)] else []) + \
               [(x + dx, y + dy) for dx in [-1, 1] if 0 <= x + dx < 8 and board[(x + dx, y + dy)].is_team(not team)
                or (x + dx, y + dy) == board.en_passant]


pw = Pawn(True)
pb = Pawn(False)
