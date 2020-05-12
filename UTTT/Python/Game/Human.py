# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget

from ..UTTT import UTTT

P1 = UTTT.P1
P2 = UTTT.P2
N = UTTT.N
T = UTTT.T


class UTTT_Widget(QWidget):

    top_margin = 15
    bottom_margin = 25
    left_margin = 10
    right_margin = 10

    def __init__(self, player, width=700, height=700):
        self.player = player
        super().__init__()
        self.setWindowTitle("Ultimate Tic Tac Toe by AntonioJKim")
        self.width = width
        self.height = height
        self.resize(width, height)
        self.installEventFilter(self)
        self.setMouseTracking(True)

        # Graphics attributes
        self.large_grid_spacing = 225
        self.small_grid_margins = 15
        self.small_grid_spacing = (
            self.large_grid_spacing - 2 * self.small_grid_margins
        ) // 3

        self.locked = True

        self.mouse_i = -1
        self.mouse_j = -1

        self.current_player = P1
        self.legal_moves = set()
        self.filled = set()
        self.quadrant_filled = set()

    def lock(self):
        self.locked = True
        self.update()
        self.repaint()

    def unlock(self):
        self.locked = False
        self.update()
        self.repaint()

    def mouseMoveEvent(self, event):
        if not self.locked:
            x = event.x()
            y = event.y()

            i = sum(
                (
                    min((x - self.left_margin) // self.large_grid_spacing, 2),
                    3 * min((y - self.top_margin) // self.large_grid_spacing, 2),
                )
            )
            x = max(
                x
                - min((x - self.left_margin) // self.large_grid_spacing, 2)
                * self.large_grid_spacing
                - 2 * self.small_grid_margins
                + 5,
                0,
            )
            y = max(
                y
                - min((y - self.top_margin) // self.large_grid_spacing, 2)
                * self.large_grid_spacing
                - 2 * self.small_grid_margins,
                0,
            )
            j = sum(
                (
                    min(x // self.small_grid_spacing, 2),
                    3 * min(y // self.small_grid_spacing, 2),
                )
            )

            if 0 <= i < 9 and 0 <= j < 9 and (i != self.mouse_i or j != self.mouse_j):
                self.mouse_i = i
                self.mouse_j = j
                self.update()

    def mouseReleaseEvent(self, event):
        if not self.locked:
            self.player.move = (self.mouse_i, self.mouse_j)
            self.player.end_turn()

    def keyReleaseEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_W:
                sys.exit(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grids(painter)
        self.draw_legal(painter)
        self.draw_filled(painter)
        self.draw_quadrant_filled(painter)
        self.draw_hover(painter)

    def draw_grids(self, painter):
        # Draw Large Grid
        painter.setPen(QPen(Qt.black, 4))
        for i in range(1, 3):
            painter.drawLine(
                self.left_margin + i * self.large_grid_spacing,
                self.top_margin,
                self.left_margin + i * self.large_grid_spacing,
                self.height - self.bottom_margin,
            )
            painter.drawLine(
                self.left_margin,
                self.top_margin + i * 225,
                self.width - self.right_margin,
                self.top_margin + i * 225,
            )

        # Draw Small Grids
        painter.setPen(QPen(Qt.black, 2))
        for i in range(3):
            for j in range(3):
                for k in range(1, 3):
                    painter.drawLine(
                        self.left_margin
                        + i * self.large_grid_spacing
                        + k * self.small_grid_spacing
                        + self.small_grid_margins,
                        self.top_margin
                        + j * self.large_grid_spacing
                        + self.small_grid_margins,
                        self.left_margin
                        + i * self.large_grid_spacing
                        + k * self.small_grid_spacing
                        + self.small_grid_margins,
                        self.top_margin
                        + j * self.large_grid_spacing
                        + 3 * self.small_grid_spacing
                        + self.small_grid_margins,
                    )
                    painter.drawLine(
                        self.left_margin
                        + i * self.large_grid_spacing
                        + self.small_grid_margins,
                        self.top_margin
                        + j * self.large_grid_spacing
                        + k * self.small_grid_spacing
                        + self.small_grid_margins,
                        self.left_margin
                        + i * self.large_grid_spacing
                        + 3 * self.small_grid_spacing
                        + self.small_grid_margins,
                        self.top_margin
                        + j * self.large_grid_spacing
                        + k * self.small_grid_spacing
                        + self.small_grid_margins,
                    )

    legal_brushes = {
        P1: QBrush(QColor(0, 204, 0, 84)),
        P2: QBrush(QColor(0, 128, 255, 84)),
    }

    def get_rect(self, i, j):
        return QRect(
            (i % 3) * self.large_grid_spacing
            + (j % 3) * self.small_grid_spacing
            + self.left_margin
            + self.small_grid_margins,
            (i // 3) * self.large_grid_spacing
            + (j // 3) * self.small_grid_spacing
            + self.top_margin
            + self.small_grid_margins,
            self.small_grid_spacing,
            self.small_grid_spacing,
        )

    def draw_legal(self, painter):
        if self.current_player is not None:
            brush = self.legal_brushes[self.current_player]
            for i, j in self.legal_moves:
                painter.fillRect(self.get_rect(i, j), brush)

    player_symbols = {
        P1: ("X", (0, 204, 0)),
        P2: ("O", (0, 128, 255)),
        T: ("", (0, 0, 0)),
    }

    def draw_filled(self, painter):
        painter.setFont(QFont("system", 30))

        quadrant_filled = set(i for i, p in self.quadrant_filled)

        for i, j, player in self.filled:
            symbol, (r, g, b) = self.player_symbols[player]
            if i not in quadrant_filled:
                painter.setPen(QPen(QColor(r, g, b, 255)))
            else:
                painter.setPen(QPen(QColor(r, g, b, 96)))

            painter.drawText(self.get_rect(i, j), Qt.AlignCenter, symbol)

    def draw_quadrant_filled(self, painter):
        painter.setFont(QFont("system", 150))

        def draw_symbol(i, player):
            symbol, (r, g, b) = self.player_symbols[player]
            painter.setPen(QPen(QColor(r, g, b, 255)))

            painter.drawText(
                QRect(
                    (i % 3) * self.large_grid_spacing + self.top_margin,
                    (i // 3) * self.large_grid_spacing + self.left_margin,
                    self.large_grid_spacing,
                    self.large_grid_spacing,
                ),
                Qt.AlignCenter,
                symbol,
            )

        for i, player in self.quadrant_filled:
            draw_symbol(i, player)

    def draw_hover(self, painter):
        if not self.locked and (self.mouse_i, self.mouse_j) in self.legal_moves:
            painter.setFont(QFont("system", 30))
            symbol, (r, g, b) = self.player_symbols[self.current_player]
            painter.setPen(QPen(QColor(r, g, b, 255)))
            painter.drawText(
                self.get_rect(self.mouse_i, self.mouse_j), Qt.AlignCenter, symbol
            )


class HumanPlayer:
    def __init__(self, game):
        self.game = game
        self.move = []
        self.ui = UTTT_Widget(self)
        self.ui.show()

    def update(self):
        if self.game.get_winner() != N:
            if self.game.get_winner() == T:
                self.ui.current_player = None
            else:
                self.ui.current_player = self.game.get_winner()

            self.ui.legal_moves = {(i, j) for i in range(9) for j in range(9)}
        else:
            self.ui.current_player = self.game.get_current_player()
            self.ui.legal_moves = self.game.get_legal_moves()

        self.ui.filled = self.game.get_filled()
        self.ui.quadrant_filled = self.game.get_quadrant_filled()

    def start_turn(self):
        self.update()
        if self.game.get_winner() == N:
            self.ui.unlock()
        else:
            self.ui.lock()

    def end_turn(self):
        self.game.make_move(*self.move)
        self.update()
        self.ui.lock()
        self.game.next()
