# -*- coding: utf-8 -*-

"""
Interactively play the game of Tic-Tac-Toe against a human player
and never lose.
"""

EMPTY_POSITION = '-'


class TicTacToe(object):

    def __init__(self):
        self.winner = None
        self._board = [EMPTY_POSITION] * 9
        self._win_positions = [(0, 1, 2),
                               (3, 4, 5),
                               (6, 7, 8),
                               (0, 3, 6),
                               (1, 4, 7),
                               (2, 5, 8),
                               (0, 4, 8),
                               (2, 4, 6)]
        self._lastmoves = []

    def __contains__(self, pos):
        return pos in self.get_free_positions()

    def __iter__(self):
        return (i for i, v in enumerate(self._board) if v == EMPTY_POSITION)

    def get_free_positions(self):
        for pos in self:
            yield pos

    def display_game_area(self):
        print '\nCurrent board:'
        for j, v in enumerate(self._board):
            print '{} |'.format(j if v == EMPTY_POSITION else v),
            if not (j + 1) % 3:
                print '\n', '-' * 11

    def is_gameover(self):
        for i, j, k in self._win_positions:
            if (self._board[i] == self._board[j] == self._board[k] and
                self._board[i] != EMPTY_POSITION):
                self.winner = self._board[i]
                return True

        if EMPTY_POSITION not in self._board:
            self.winner = EMPTY_POSITION
            return True
        return False

    def mark(self, marker, pos):
        '''Mark a position with marker X or O'''
        self._board[pos] = marker
        self._lastmoves.append(pos)

    def revert_last_move(self):
        ''' Reset the recent move '''
        self._board[self._lastmoves.pop()] = EMPTY_POSITION
        self.winner = None

    def play(self, player1, player2):
        ''' Executes the game play '''

        for i, _ in enumerate(self._board):
            self.display_game_area()

            if not i % 2:
                print "\t\t[{}'s Move]".format('Human'
                                 if isinstance(player1, Human) else 'Computer')
                player1.move(self)
            else:
                print "\t\t[{}'s Move]".format('Human'
                                if isinstance(player2, Human) else 'Computer')
                player2.move(self)

            if self.is_gameover():
                self.display_game_area()
                if self.winner == EMPTY_POSITION:
                    print '\nGame over with Draw'
                else:
                    print '\n{} wins!'.format('Computer'
                                              if self.winner == 'O' else 'You')
                break


class Player(object):

    def __init__(self, marker):
        self.marker = marker
        self.opponentmarker = 'O' if self.marker == 'X' else 'X'

    def move(self, tictactoe):
        ''' Chooses the next move '''
        raise NotImplementedError


class Computer(Player):
    '''Computer Player'''

    def move(self, tictactoe):
        move_position, _ = self.maximized_move(tictactoe)
        tictactoe.mark(self.marker, move_position)

    def get_score(self, tictactoe):
        ''' Returns the status of game: Win, lose or draw '''
        if tictactoe.is_gameover():
            if tictactoe.winner == self.marker:
                return 1  # won
            elif tictactoe.winner == self.opponentmarker:
                return -1  # opponent won
        return 0  # draw

    def minimized_move(self, tictactoe):
        ''' Returns the next best move for opponent '''
        best_score = None
        best_move = None

        for pos in tictactoe.get_free_positions():
            tictactoe.mark(self.opponentmarker, pos)

            if tictactoe.is_gameover():
                score = self.get_score(tictactoe)
            else:
                _, score = self.maximized_move(tictactoe)

            tictactoe.revert_last_move()

            if best_score is None or score < best_score:
                best_score = score
                best_move = pos
        return best_move, best_score

    def maximized_move(self, tictactoe):
        ''' Returns the next best move '''
        best_score = None
        best_move = None

        for pos in tictactoe.get_free_positions():
            tictactoe.mark(self.marker, pos)

            if tictactoe.is_gameover():
                score = self.get_score(tictactoe)
            else:
                _, score = self.minimized_move(tictactoe)

            tictactoe.revert_last_move()

            if best_score is None or score > best_score:
                best_score = score
                best_move = pos
        return best_move, best_score


class Human(Player):
    '''Human player'''

    def move(self, tictactoe):
        while True:
            pos = raw_input('Input position:')
            try:
                pos = int(pos)
            except ValueError:
                pos = -1
            if pos not in tictactoe:
                print 'Invalid move. Retry'
            else:
                break
        tictactoe.mark(self.marker, pos)


if __name__ == '__main__':
    game = TicTacToe()
    player1 = Human('X')
    player2 = Computer('O')
    game.play(player1, player2)
