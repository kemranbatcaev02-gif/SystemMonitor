"""Живой скроллящийся график (кастомная отрисовка через QPainter)."""
from collections import deque

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import (
    QPainter, QPen, QColor, QLinearGradient, QPainterPath, QBrush, QFont
)
from PySide6.QtWidgets import QWidget

from core.utils import fmt_rate


class GraphWidget(QWidget):
    """
    График с плавной линией и градиентной заливкой.

    fixed_max=100 для процентов; fixed_max=None -> автомасштаб (для сети).
    """

    def __init__(self, title, color, max_points=60, is_percent=True,
                 fixed_max=100, parent=None):
        super().__init__(parent)
        self.title = title
        self.color = QColor(color)
        self.max_points = max_points
        self.is_percent = is_percent
        self.fixed_max = fixed_max
        self.data = deque([0.0] * max_points, maxlen=max_points)
        self.setMinimumHeight(170)

    def add_value(self, value):
        self.data.append(float(value))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(0, 0, -1, -1)
        w, h = rect.width(), rect.height()

        # Фон-карточка
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#161923"))
        p.drawRoundedRect(QRectF(rect), 14, 14)

        pad_l, pad_r, pad_t, pad_b = 14, 14, 44, 16
        plot = QRectF(pad_l, pad_t, w - pad_l - pad_r, h - pad_t - pad_b)

        # Верхняя граница шкалы
        if self.fixed_max is not None:
            vmax = self.fixed_max
        else:
            vmax = (max(self.data) or 1.0) * 1.25

        # Сетка
        p.setPen(QPen(QColor("#232735"), 1))
        for i in range(5):
            y = plot.top() + plot.height() * i / 4
            p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))

        # Линия + заливка
        n = len(self.data)
        if n > 1 and plot.width() > 0:
            dx = plot.width() / (n - 1)
            points = []
            for i, v in enumerate(self.data):
                x = plot.left() + dx * i
                y = plot.bottom() - (min(v, vmax) / vmax) * plot.height()
                points.append(QPointF(x, y))

            line = QPainterPath()
            line.moveTo(points[0])
            for pt in points[1:]:
                line.lineTo(pt)

            fill = QPainterPath(line)
            fill.lineTo(plot.right(), plot.bottom())
            fill.lineTo(plot.left(), plot.bottom())
            fill.closeSubpath()

            grad = QLinearGradient(0, plot.top(), 0, plot.bottom())
            top = QColor(self.color); top.setAlpha(150)
            bot = QColor(self.color); bot.setAlpha(10)
            grad.setColorAt(0, top)
            grad.setColorAt(1, bot)
            p.fillPath(fill, QBrush(grad))

            pen = QPen(self.color, 2)
            pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(pen)
            p.drawPath(line)

        # Заголовок
        p.setPen(QColor("#e6e9ef"))
        p.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        p.drawText(QRectF(pad_l, 12, plot.width(), 20),
                   Qt.AlignLeft | Qt.AlignVCenter, self.title)

        # Текущее значение
        cur = self.data[-1] if self.data else 0.0
        txt = f"{cur:.0f}%" if self.is_percent else fmt_rate(cur)
        p.setPen(self.color)
        p.setFont(QFont("Segoe UI", 12, QFont.Bold))
        p.drawText(QRectF(pad_l, 10, plot.width() - pad_r, 24),
                   Qt.AlignRight | Qt.AlignVCenter, txt)
        p.end()
