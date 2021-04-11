from .Piece import ChessPiece


class King(ChessPiece):
    def __str__(self) -> str:
        return 'k'

    def __repr__(self) -> str:
        return ' ♚ ' if self.team else ' ♔ '

    def find_moves(self, board, x: int, y: int) -> list[tuple[int, int], ...]:
        team = self.is_team()
        return [(x + dx, y + dy) for dx, dy in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
                if 0 <= x + dx < 8 and 0 <= y + dy < 8 and not board[(x + dx, y + dy)].is_team(team) and
                not board.is_attacked((x + dx, y + dy), not team)] + \
               [(2 if dx else 6, y) for dx in [0, 1] if board.castling[team][dx] and
                all(not board[(d, y)] for d in ([1, 2, 3] if dx else [5, 6])) and
                all(not board.is_attacked((d, y), not team) for d in ([2, 3, 4] if dx else [4, 5, 6]))]


kw = King(True)
kb = King(False)
