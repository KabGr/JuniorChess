from datetime import datetime
from math import inf

from scr.Board import ChessBoard, bprint


def score(board: ChessBoard):
    return sum(board[x, y].price() for x in range(8) for y in range(8))


def ai(start: ChessBoard = ChessBoard()):
    evos = [start]
    path = {start: None}
    st = datetime.now()
    for depth in range(1, 6):
        previous_evos, evos = evos, []
        for board in previous_evos:
            for evo in board.evolutions():
                evo.turn = not evo.turn
                path[evo] = board
                evos.append(evo)
        print(f'Глубина: {depth}')
        if (datetime.now() - st).total_seconds() > 2:
            break
    print('Обработка')
    rating, evos = {}, set(evos)
    while len(evos) > 1:
        evos, previous_evos = set(), evos
        for evo in previous_evos:
            rating[path[evo]] = min(rating.get(path[evo], inf), score(evo)) if evo.turn else max(rating.get(path[evo], -inf), score(evo))
            evos.add(path[evo])
            bprint(evo)
        print(evos)
        print(path)
        print(rating)
        print(rating.get(start))
        input()


if __name__ == '__main__':
    ai()
