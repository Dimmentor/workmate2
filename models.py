from dataclasses import dataclass


@dataclass
class Row:
    """Обёртка для строки из CSV-файла, чтобы передавать данные."""
    data: dict
