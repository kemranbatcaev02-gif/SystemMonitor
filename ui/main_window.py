"""Главное окно: собирает все виджеты и обновляет их по таймеру."""
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)

from core.monitor import SystemMonitor
from core.utils import fmt_bytes, fmt_uptime
from ui.graph_widget import GraphWidget
from ui.cards import GaugeCard, NetworkCard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.monitor = SystemMonitor()
        self.info = self.monitor.system_info()

        self.setWindowTitle("System Monitor")
        self.resize(1120, 740)
        self.setMinimumSize(920, 640)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        layout.addWidget(self._build_header())
        layout.addLayout(self._build_gauges())
        layout.addLayout(self._build_graphs())
        layout.addWidget(self._build_processes(), stretch=1)

        # Таймеры обновления
        self.fast_timer = QTimer(self)
        self.fast_timer.timeout.connect(self._update_fast)
        self.fast_timer.start(1000)

        self.slow_timer = QTimer(self)
        self.slow_timer.timeout.connect(self._update_processes)
        self.slow_timer.start(2000)

        # Первичное обновление
        self._update_fast()
        self._update_processes()

    # ---------- Построение UI ----------

    def _build_header(self):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(72)
        h = QHBoxLayout(header)
        h.setContentsMargins(20, 0, 20, 0)

        dot = QLabel("\u25CF")
        dot.setObjectName("accentDot")

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        title = QLabel("System Monitor")
        title.setObjectName("appTitle")
        sub = QLabel(f"{self.info['hostname']}  \u00B7  {self.info['os']}")
        sub.setObjectName("subLabel")
        title_box.addWidget(title)
        title_box.addWidget(sub)

        cpu_info = QLabel(
            f"{self.info['cpu_name']}   \u00B7   "
            f"{self.info['cores_physical']}C / {self.info['cores_logical']}T"
        )
        cpu_info.setObjectName("subLabel")

        up_box = QVBoxLayout()
        up_box.setSpacing(0)
        up_box.setAlignment(Qt.AlignRight)
        up_cap = QLabel("Uptime")
        up_cap.setObjectName("subLabel")
        up_cap.setAlignment(Qt.AlignRight)
        self.uptime_value = QLabel("--")
        self.uptime_value.setObjectName("uptimeValue")
        self.uptime_value.setAlignment(Qt.AlignRight)
        up_box.addWidget(up_cap)
        up_box.addWidget(self.uptime_value)

        h.addWidget(dot)
        h.addSpacing(10)
        h.addLayout(title_box)
        h.addSpacing(24)
        h.addWidget(cpu_info)
        h.addStretch()
        h.addLayout(up_box)
        return header

    def _build_gauges(self):
        row = QHBoxLayout()
        row.setSpacing(14)
        self.cpu_gauge = GaugeCard("CPU", "#4dd0e1")
        self.ram_gauge = GaugeCard("Memory", "#b388ff")
        self.disk_gauge = GaugeCard("Disk", "#ffb74d")
        self.net_card = NetworkCard()
        for w in (self.cpu_gauge, self.ram_gauge, self.disk_gauge, self.net_card):
            row.addWidget(w)
        return row

    def _build_graphs(self):
        row = QHBoxLayout()
        row.setSpacing(14)
        self.cpu_graph = GraphWidget("CPU Load", "#4dd0e1", is_percent=True, fixed_max=100)
        self.net_graph = GraphWidget("Network (download)", "#3ddc84",
                                     is_percent=False, fixed_max=None)
        row.addWidget(self.cpu_graph)
        row.addWidget(self.net_graph)
        return row

    def _build_processes(self):
        card = QFrame()
        card.setObjectName("sectionCard")
        v = QVBoxLayout(card)
        v.setContentsMargins(16, 12, 16, 12)

        title = QLabel("Top Processes")
        title.setObjectName("sectionTitle")
        v.addWidget(title)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "MEM %"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        v.addWidget(self.table)
        return card

    # ---------- Обновление данных ----------

    def _update_fast(self):
        s = self.monitor.snapshot()

        self.cpu_gauge.set_value(s["cpu"], f"{s['cpu_freq'] / 1000:.2f} GHz")
        self.ram_gauge.set_value(
            s["ram_percent"],
            f"{fmt_bytes(s['ram_used'])} / {fmt_bytes(s['ram_total'])}",
        )
        self.disk_gauge.set_value(
            s["disk_percent"],
            f"{fmt_bytes(s['disk_used'])} / {fmt_bytes(s['disk_total'])}",
        )
        self.net_card.set_rates(s["net_up"], s["net_down"])

        self.cpu_graph.add_value(s["cpu"])
        self.net_graph.add_value(s["net_down"])

        self.uptime_value.setText(fmt_uptime(s["uptime"]))

    def _update_processes(self):
        procs = self.monitor.processes(limit=15)
        self.table.setRowCount(len(procs))
        for r, p in enumerate(procs):
            pid = str(p.get("pid", ""))
            name = p.get("name") or "?"
            cpu = f"{p.get('cpu_percent') or 0:.1f}"
            mem = f"{p.get('memory_percent') or 0:.1f}"

            items = [
                QTableWidgetItem(pid),
                QTableWidgetItem(name),
                QTableWidgetItem(cpu),
                QTableWidgetItem(mem),
            ]
            items[0].setTextAlignment(Qt.AlignCenter)
            items[2].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            items[3].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            for c, it in enumerate(items):
                self.table.setItem(r, c, it)
