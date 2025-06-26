class CSVProcessorError(Exception):
    """Базовое исключение для ошибок в обработке CSV."""
    pass


class FilterFormatError(CSVProcessorError):
    """Ошибка формата фильтра."""
    pass


class AggregateFormatError(CSVProcessorError):
    """Ошибка формата агрегации."""
    pass
