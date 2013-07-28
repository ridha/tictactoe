#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from tictactoe import TicTacToe, Computer, Human


class TicTacToeBoard(object):

    def __init__(self, player1, player2):
        self.create()
        self.layout()
        self.show()
        self.player1 = player1
        self.player2 = player2
        self.tictactoe = TicTacToe()

    def create(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(400, 400)
        self.window.connect("destroy", self.destroy)
        self.window.connect("delete_event", self.delete_event)
        self.table = gtk.Table(rows=3, columns=3, homogeneous=True)
        self.buttons = [gtk.Button(label=" - ") for i in xrange(9)]
        for index, button in enumerate(self.buttons):
            button.position = index
            button.connect('clicked', self.button_clicked)

    def layout(self):
        for i in xrange(3):
            for j in xrange(3):
                self.table.attach(self.buttons[i * 3 + j], j, j + 1, i, i + 1)
        self.window.add(self.table)

    def show(self):
        for button in self.buttons:
            button.show()
        self.table.show()
        self.window.show()

    def is_gameover(self):
        if self.tictactoe.is_gameover():
            if self.tictactoe.winner == self.player1.marker:
                msg = 'You wins!'
            elif self.tictactoe.winner == self.player2.marker:
                msg = 'Computer wins!'
            else:
                msg = 'Game over with Draw'
            md = gtk.MessageDialog(self.window,
                                   0,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
            md.run()
            md.destroy()
            return True
        return False

    def button_clicked(self, widget):
        if not self.is_gameover():
            if widget.position not in self.tictactoe:
                md = gtk.MessageDialog(self.window,
                                       0,
                                       gtk.MESSAGE_ERROR,
                                       gtk.BUTTONS_OK,
                                       "Invalid move. Retry")
                md.run()
                md.destroy()
            else:
                widget.set_label(self.player1.marker)
                self.tictactoe.mark(self.player1.marker, widget.position)
                if not self.is_gameover():
                    move_position, _ = self.player2.maximized_move(
                        self.tictactoe)
                    self.tictactoe.mark(self.player2.marker, move_position)
                    self.buttons[move_position].set_label(self.player2.marker)
                    self.is_gameover()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def delete_event(self, widget, event, data=None):
        return False

    def play(self):
        gtk.main()


if __name__ == "__main__":
    board = TicTacToeBoard(Human('X'), Computer('O'))
    board.play()
