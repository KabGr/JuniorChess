from datetime import datetime, timedelta
from re import match

from scr.Board import *


def start_game(timer: str = None, theme: int = 3, reflection: bool = False):
    board = ChessBoard()
    add = 0
    if timer:
        timer, add = map(int, timer.split('+'))
        add, timer = timedelta(seconds=add), [timedelta(minutes=timer), timedelta(minutes=timer)]
    fifty_moves, check, history, start = 100, '', [], False
    while True:
        bprint(board, theme, reflection)
        if timer:
            if start: timer[board.turn] -= datetime.now() - start
            m, s = timer[board.turn].seconds // 60, timer[board.turn].seconds % 60
            print(f'У вас осталось {f"{m} мин" if m else ""}{" и " if m and s else ""}{f"{s} сек" if s or not m else ""}.')
        start, move, check = datetime.now(), input(f'{check}Ход {"Белых" if board.turn else "Чёрных"}: ').lower(), ''
        if move == 'give up':
            print(f'\nПобедили {"Белые" if not board.turn else "Чёрные"}!')
            break
        elif timer and timer[board.turn].total_seconds() <= 0:
            print(f'\nУ {"Белых" if board.turn else "Чёрных"} закончилась время!\nПобедили {"Белые" if not board.turn else "Чёрные"}!')
            break
        elif move == 'draw':
            ans = input(f'\n{"Белые" if board.turn else "Чёрные"} предлагаю ничью, вы принимаете её?: ').lower()
            while ans not in ['y', 'yes', 'accept', 'n', 'no', 'deny']:
                ans = input(f'Некоректный ввод!\n\n{"Белые" if board.turn else "Чёрные"} предлагаю ничью, вы принимаете её?: ').lower()
            if ans in ['y', 'yes', 'accept']:
                print('\nНичья!')
                break
            print('Ничья отклонена!')
        elif fifty_moves <= 0:
            print('\nНичья по правилу 50 ходов!')
            break
        elif match(r'[a-h][1-8]\s?[a-h][1-8]$', move):
            xy_start, xy_end = map(lambda x: (ord(x[0]) - 97, int(x[1]) - 1), [move[:2], move[-2:]])
            if board[xy_start].is_team(board.turn) and xy_end in board[xy_start].find_moves(board, *xy_start) and \
                    not board.evolution(xy_start, xy_end).check():  # TODO: replace to func
                if timer:
                    timer[board.turn] += add + start - datetime.now()
                    start = False
                add_history(board, history, move, xy_start, xy_end)
                p = board[xy_start] == 'p' and xy_end[1] == (7 if board.turn else 0)
                fifty_moves = fifty_moves - 1 if board[xy_start] != 'p' and not board[xy_end] else 100
                board.move(xy_start, xy_end)
                board.turn = not board.turn
                history[-1][board.turn] += repr(board[xy_end]) if p else ''
                if board.check():
                    check = f'Шах {"Белым" if board.turn else "Чёрным"}!\n'
                    if board.checkmate():
                        history[-1][board.turn] += '#'
                        print(f'\nШах и мат!\nПобедили {"Белые" if not board.turn else "Чёрные"}!')
                        break
                    history[-1][board.turn] += '+'
                elif board.stalemate():
                    print(f'\nПат!')
                    break
            else:
                print('Некоректный ход!')
        else:
            print('Некоректный вход!')

    input()
    print('История:')
    for i, move in enumerate(history, 1):
        print(f'\033[0m{i}.', *move)


if __name__ == '__main__':
    start_game()
