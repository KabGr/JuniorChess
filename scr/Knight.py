from .Piece import ChessPiece


class Knight(ChessPiece):
    def __str__(self) -> str:
        return 'n'

    def __repr__(self) -> str:
        return ' ♞ ' if self.team else ' ♘ '

    def price(self) -> int:
        return 1 if self.is_team() else -1

    def find_moves(self, board, x: int, y: int) -> list[tuple[int, int], ...]:
        team = self.is_team()
        return [(x + dx, y + dy) for dx, dy in [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
                if 0 <= x + dx < 8 and 0 <= y + dy < 8 and not board[(x + dx, y + dy)].is_team(team)]


nw = Knight(True)
nb = Knight(False)
