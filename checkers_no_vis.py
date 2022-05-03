#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 08:15:45 2021

@author: Rafał Biedrzycki
Kodu tego mogą używać moi studenci na ćwiczeniach z przedmiotu Wstęp do Sztucznej Inteligencji.
Kod ten powstał aby przyspieszyć i ułatwić pracę studentów, aby mogli skupić się na algorytmach sztucznej inteligencji.
Kod nie jest wzorem dobrej jakości programowania w Pythonie, nie jest również wzorem programowania obiektowego, może zawierać błędy.
Mam świadomość wielu jego braków ale nie mam czasu na jego poprawianie.

Zasady gry: https://en.wikipedia.org/wiki/English_draughts (w skrócie: wszyscy ruszają się po 1 polu. Pionki tylko w kierunku wroga, damki w dowolnym)
  z następującymi modyfikacjami: a) bicie nie jest wymagane,  b) dozwolone jest tylko pojedyncze bicie (bez serii).

Nalezy napisac funkcje minimax_a_b_recurr, minimax_a_b (woła funkcje rekurencyjną) i  evaluate, która ocenia stan gry

Chętni mogą ulepszać mój kod (trzeba oznaczyć komentarzem co zostało zmienione), mogą również dodać obsługę bicia wielokrotnego i wymagania bicia.
Mogą również wdrożyć reguły: https://en.wikipedia.org/wiki/Russian_draughts
"""

from copy import deepcopy
from math import inf

BOARD_WIDTH = 8
MAX_WHITE = True
ITERATIONS_LIMIT = 150

class Move:
    def __init__(self, piece, dest_row, dest_col, captures=None):
        self.piece=piece
        self.dest_row=dest_row
        self.dest_col=dest_col
        self.captures=captures

class Field:
    def is_empty(self):
        return True

    def is_white(self):
        return False

    def is_blue(self):
        return False

    def __str__(self):
        return "."


class Pawn(Field):
    def __init__(self, is_white, row, col):
        self.__is_white=is_white
        self.row = row
        self.col = col

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result

    def __str__(self):
        if self.is_white():
            return "w"
        return "b"

    def is_king(self):
        return False

    def is_empty(self):
        return False

    def is_white(self):
        return self.__is_white

    def is_blue(self):
        return not self.__is_white

class King(Pawn):
    def __init__(self, pawn):
        super().__init__(pawn.is_white(), pawn.row, pawn.col)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result

    def is_king(self):
        return True

    def __str__(self):
        if self.is_white():
            return "W"
        return "B"

class Board:
    def __init__(self): #row, col
        self.board = [] #np.full((BOARD_WIDTH, BOARD_WIDTH), None)
        self.white_turn = True
        self.white_fig_left = 12
        self.blue_fig_left = 12

        self.__set_pieces()

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        result.board= deepcopy(self.board)
        return result

    def __str__(self):
        to_ret=""
        for row in range(8):
            for col in range(8):
                to_ret+=str(self.board[row][col])
            to_ret+="\n"
        return to_ret

    def __set_pieces(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                self.board[row].append( Field() )

        for row in range(3):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(False, row, col)

        for row in range(5, 8):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(True, row, col)


    def get_piece_moves(self, piece):
        pos_moves=[]
        row = piece.row
        col = piece.col
        if piece.is_blue():
            enemy_is_white = True
        else:
            enemy_is_white = False

        if piece.is_white() or (piece.is_blue() and piece.is_king()):
            dir_y = -1
            if row > 0:
                new_row=row+dir_y
                if col > 0:
                    new_col=col-1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))
                        #ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y>=0 and new_col-1>=0 and self.board[new_row+dir_y][new_col-1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col-1, self.board[new_row][new_col]))

                if col < BOARD_WIDTH-1:
                    new_col=col+1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))
                        #ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y>=0 and new_col+1<BOARD_WIDTH and self.board[new_row+dir_y][new_col+1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col+1, self.board[new_row][new_col]))

        if piece.is_blue() or (piece.is_white() and self.board[row][col].is_king()):
            dir_y = 1
            if row<BOARD_WIDTH-1:
                new_row=row+dir_y
                if col > 0:
                    new_col=col-1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y<BOARD_WIDTH and new_col-1>=0 and self.board[new_row+dir_y][new_col-1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col-1, self.board[new_row][new_col]))

                if col < BOARD_WIDTH-1:
                    new_col=col+1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))
                        #ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y<BOARD_WIDTH and new_col+1<BOARD_WIDTH and self.board[new_row+dir_y][new_col+1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col+1, self.board[new_row][new_col]))
        return pos_moves

#-----------------------------------------------------------#
    # options:
    # 0 - regular
    # 1 - pawn for 5 + row nr (from its start)
    # 2 - pwan for 7 if on enemy's half, for 5 if not
    def evaluate(self, option : int):
        sum=0
        factor=-1
        if MAX_WHITE:
            factor=1

        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                field_f = self.board[row][col]

                if field_f.is_empty():
                    continue

                # white pawns
                if field_f.is_white():
                    if field_f.is_king():
                        sum += 10 * factor
                    else:
                        sum += 1 * factor
                        if option == 1:
                            sum += (4 + (BOARD_WIDTH - 1 - row)) * factor
                        elif option == 2:
                            p = 4 if row >= BOARD_WIDTH/2 else 6
                            sum += p * factor

                # blue pawns
                elif field_f.is_king():
                    sum += 10 * (-factor)
                else:
                    sum += 1 * (-factor)
                    if option == 1:
                        sum += (4 + (row)) * (-factor)
                    elif option == 2:
                        p = 4 if row < BOARD_WIDTH/2 else 6
                        sum += p * (-factor)
        return sum


    def get_possible_moves(self):
        pos_moves = []
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                if not self.board[row][col].is_empty():
                    if (not self.white_turn and self.board[row][col].is_blue()) or (self.white_turn and self.board[row][col].is_white()):
                        pos_moves.extend( self.get_piece_moves(self.board[row][col]) )
        return pos_moves


#----------------------------------------------------------------------------------
    def end(self):
        if self.blue_fig_left==0:
            return 'white'
        if self.white_fig_left==0:
            return 'blue'

        moves = self.get_possible_moves()
        if not moves:
            return 'tie'

        return None

    def make_ai_move(self, move):
        d_row = move.dest_row
        d_col = move.dest_col
        row_from = move.piece.row
        col_from = move.piece.col

        self.board[d_row][d_col]=self.board[row_from][col_from]
        self.board[d_row][d_col].row=d_row
        self.board[d_row][d_col].col=d_col
        self.board[row_from][col_from]=Field()

        if move.captures:
            fig_to_del = move.captures

            self.board[fig_to_del.row][fig_to_del.col]=Field()
            if self.white_turn:
                self.blue_fig_left -= 1
            else:
                self.white_fig_left -= 1

        if self.white_turn and d_row==0:#damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        if not self.white_turn and d_row==BOARD_WIDTH-1:#damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        self.white_turn = not self.white_turn


    def copy_and_move(self, move):
        board_cpy = deepcopy(self)
        board_cpy.make_ai_move(move)
        return board_cpy


class Game:
    def __init__(self, blue_evaluation : int, white_evaluation : int):
        self.board = Board()
        self.blue_evaluation = blue_evaluation
        self.white_evaluation = white_evaluation

    def ai_game(self, print_game : bool, min_max_depth_blue : int, min_max_depth_white : int):
        end = self.end()

        iterations = 0

        while not end and iterations < ITERATIONS_LIMIT:

            if print_game:
                print(self.board)

            if self.board.white_turn:
                move = minimax_a_b(deepcopy(self.board), min_max_depth_white, self.white_evaluation)
            else:
                move = minimax_a_b(deepcopy(self.board),  min_max_depth_blue, self.blue_evaluation)

            self.board.make_ai_move(move)
            end = self.end()
            iterations += 1

        if iterations >= ITERATIONS_LIMIT:
            return 'tie'
        return end

    def end(self):
        return self.board.end()


#--------------------------------------------------------------
def minimax_a_b(board : Board, depth : int, evaluate_option : int):
    moves = board.get_possible_moves()

    do_max = (MAX_WHITE == board.white_turn)

    if do_max:
        return max(moves,
    key=lambda move: minimax_a_b_recurr(board.copy_and_move(move), depth - 1, -inf, inf, evaluate_option))

    else:
        return min(moves,
    key=lambda move: minimax_a_b_recurr(board.copy_and_move(move), depth - 1, -inf, inf, evaluate_option))


def minimax_a_b_recurr(board : Board, depth : int, a : int , b : int, evaluate_option : int):
    moves = board.get_possible_moves()

    if not moves or depth == 0:
        return board.evaluate(evaluate_option)

    max_player = (MAX_WHITE == board.white_turn)

    if max_player:
        for move in moves:
            if move:
                a = max(a, minimax_a_b_recurr(board.copy_and_move(move), depth - 1, a, b, evaluate_option))
                if a >= b:
                    break
        return a
    else:
        for move in moves:
            if move:
                b = min(b, minimax_a_b_recurr(board.copy_and_move(move), depth - 1, a, b, evaluate_option))
                if a >= b:
                    break
        return b
