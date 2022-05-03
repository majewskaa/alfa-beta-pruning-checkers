from checkers_no_vis import Game
from tabulate import tabulate

MINIMAX_DEPTH_WHITE = [1, 2, 3]
MINIMAX_DEPTH_BLUE = [1, 2, 3]
EVALUATION_OPTIONS = [0, 1, 2]


def get_stats_depths():

    result = []
    for white_depth in MINIMAX_DEPTH_WHITE:
        result_row = []
        for blue_depth in MINIMAX_DEPTH_BLUE:
            game = Game(0, 0)
            end = game.ai_game(False, blue_depth, white_depth)

            if end == 'white':
                result_row.append('w')
            elif end == 'blue':
                result_row.append('b')
            elif end == 'tie':
                result_row.append('t')
        result.append(result_row)

    print('w - wygrana białych\nb - wygrana niebieskich\nt - remis\n')

    header = ['white/blue'] + MINIMAX_DEPTH_BLUE

    stat_data = [[d] + r for d, r in zip(MINIMAX_DEPTH_WHITE, result)]
    table = tabulate(stat_data,
        headers = header, tablefmt="presto")

    print(table)


def get_stats_algs():
    result = []
    for ev_option_w in EVALUATION_OPTIONS:
        result_row = []
        for ev_option_b in EVALUATION_OPTIONS:
            game = Game(ev_option_b, ev_option_w)
            end = game.ai_game(False, 4, 4)

            if end == 'white':
                result_row.append('w')
            elif end == 'blue':
                result_row.append('b')
            elif end == 'tie':
                result_row.append('t')
        result.append(result_row)

    print('w - wygrana białych\nb - wygrana niebieskich\nt - remis\n')

    header = ['white/blue'] + EVALUATION_OPTIONS

    stat_data = [[d] + r for d, r in zip(EVALUATION_OPTIONS, result)]
    table = tabulate(stat_data,
        headers = header, tablefmt="presto")

    print(table)


get_stats_depths()
# get_stats_algs()