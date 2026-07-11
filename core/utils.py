"""Вспомогательные функции форматирования."""


def fmt_bytes(num):
    """Байты -> человекочитаемый размер (1.5 GB)."""
    num = float(num)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PB"


def fmt_rate(num):
    """Байты/сек -> скорость (2.3 MB/s)."""
    num = float(num)
    for unit in ("B/s", "KB/s", "MB/s", "GB/s"):
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB/s"


def fmt_uptime(seconds):
    """Секунды -> аптайм (3d 4h 12m)."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d:
        return f"{d}d {h}h {m}m"
    if h:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"
