"""Сбор системных метрик через psutil."""
import os
import time
import platform

import psutil


class SystemMonitor:
    """Собирает метрики системы: CPU, RAM, диск, сеть, процессы."""

    def __init__(self):
        # Праймим счётчики CPU (первый вызов всегда 0)
        psutil.cpu_percent(interval=None, percpu=True)
        self._prev_net = psutil.net_io_counters()
        self._prev_time = time.time()
        self._boot_time = psutil.boot_time()

        # Корень диска: системный на Windows, "/" на *nix
        if platform.system() == "Windows":
            self._disk_root = os.getenv("SystemDrive", "C:") + "\\"
        else:
            self._disk_root = "/"

    def snapshot(self):
        """Один срез всех «быстрых» метрик — вызывать раз в секунду."""
        now = time.time()

        per_core = psutil.cpu_percent(interval=None, percpu=True)
        overall = sum(per_core) / len(per_core) if per_core else 0.0

        vm = psutil.virtual_memory()
        sm = psutil.swap_memory()

        try:
            disk = psutil.disk_usage(self._disk_root)
            disk_percent, disk_used, disk_total = disk.percent, disk.used, disk.total
        except OSError:
            disk_percent = disk_used = disk_total = 0

        net = psutil.net_io_counters()
        dt = max(now - self._prev_time, 1e-6)
        up_rate = (net.bytes_sent - self._prev_net.bytes_sent) / dt
        down_rate = (net.bytes_recv - self._prev_net.bytes_recv) / dt
        self._prev_net = net
        self._prev_time = now

        freq = psutil.cpu_freq()

        return {
            "cpu": overall,
            "per_core": per_core,
            "cpu_freq": freq.current if freq else 0.0,
            "ram_percent": vm.percent,
            "ram_used": vm.used,
            "ram_total": vm.total,
            "swap_percent": sm.percent,
            "disk_percent": disk_percent,
            "disk_used": disk_used,
            "disk_total": disk_total,
            "net_up": up_rate,
            "net_down": down_rate,
            "uptime": now - self._boot_time,
        }

    def processes(self, limit=15):
        """Топ процессов по загрузке CPU."""
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                procs.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        procs.sort(key=lambda x: (x.get("cpu_percent") or 0.0), reverse=True)
        return procs[:limit]

    def system_info(self):
        """Статичная информация о системе."""
        uname = platform.uname()
        return {
            "hostname": uname.node,
            "os": f"{uname.system} {uname.release}",
            "cpu_name": platform.processor() or uname.processor or "Unknown CPU",
            "cores_physical": psutil.cpu_count(logical=False) or 0,
            "cores_logical": psutil.cpu_count(logical=True) or 0,
        }
