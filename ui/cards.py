"""Карточки-виджеты: круговой гейдж и карточка сети."""
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget

from core.utils import fmt_rate


class GaugeCard(QWidget):
    """Круговой индикатор в процентах с подписью."""

    def __init__(self, title, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.color = QColor(color)
        self.value = 0.0
        self.subtitle = ""
        self.setMinimumSize(150, 160)

    def set_value(self, percent, subtitle=""):
        self.value = max(0.0, min(100.0, percent))
        self.subtitle = subtitle
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#161923"))
        p.drawRoundedRect(QRectF(rect.adjusted(0, 0, -1, -1)), 14, 14)

        side = min(rect.width(), rect.height()) - 64
        cx = rect.width() / 2
        cy = rect.height() / 2 - 6
        ring = QRectF(cx - side / 2, cy - side / 2, side, side)

        # Фоновая дуга
        track = QPen(QColor("#242838"), 12)
        track.setCapStyle(Qt.RoundCap)
        p.setPen(track)
        p.drawArc(ring, 225 * 16, -270 * 16)

        # Дуга значения
        arc = QPen(self.color, 12)
        arc.setCapStyle(Qt.RoundCap)
        p.setPen(arc)
        span = -270 * (self.value / 100.0)
        p.drawArc(ring, 225 * 16, int(span * 16))

        # Значение в центре
        p.setPen(QColor("#f2f4f8"))
        p.setFont(QFont("Segoe UI", 20, QFont.Bold))
        p.drawText(ring, Qt.AlignCenter, f"{self.value:.0f}%")

        # Заголовок
        p.setPen(QColor("#aab2c5"))
        p.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        p.drawText(QRectF(0, rect.height() - 48, rect.width(), 18),
                   Qt.AlignCenter, self.title)

        # Подпись
        p.setPen(QColor("#6b7385"))
        p.setFont(QFont("Segoe UI", 8))
        p.drawText(QRectF(0, rect.height() - 30, rect.width(), 16),
                   Qt.AlignCenter, self.subtitle)
        p.end()


class NetworkCard(QWidget):
    """Скорость сети: загрузка и отдача."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.up = 0.0
        self.down = 0.0
        self.setMinimumSize(150, 160)

    def set_rates(self, up, down):
        self.up = up
        self.down = down
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#161923"))
        p.drawRoundedRect(QRectF(rect.adjusted(0, 0, -1, -1)), 14, 14)

        w = rect.width()

        p.setPen(QColor("#aab2c5"))
        p.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        p.drawText(QRectF(0, 18, w, 20), Qt.AlignCenter, "Network")

        # Download
        p.setPen(QColor("#3ddc84"))
        p.setFont(QFont("Segoe UI", 9, QFont.DemiBold))
        p.drawText(QRectF(0, 54, w, 18), Qt.AlignCenter, "\u2193  Download")
        p.setPen(QColor("#f2f4f8"))
        p.setFont(QFont("Segoe UI", 13, QFont.Bold))
        p.drawText(QRectF(0, 70, w, 24), Qt.AlignCenter, fmt_rate(self.down))

        # Upload
        p.setPen(QColor("#ff6b6b"))
        p.setFont(QFont("Segoe UI", 9, QFont.DemiBold))
        p.drawText(QRectF(0, 102, w, 18), Qt.AlignCenter, "\u2191  Upload")
        p.setPen(QColor("#f2f4f8"))
        p.setFont(QFont("Segoe UI", 13, QFont.Bold))
        p.drawText(QRectF(0, 118, w, 24), Qt.AlignCenter, fmt_rate(self.up))
        p.end()
