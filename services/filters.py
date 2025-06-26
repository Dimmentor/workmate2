import re
from abc import ABC, abstractmethod
from typing import Optional
from services.exceptions import FilterFormatError


class Filter(ABC):
    @abstractmethod
    def match(self, row) -> bool:
        pass


class OperatorFilter(Filter):
    def __init__(self, column: str, operator: str, value: str):
        self.column = column
        self.operator = operator
        self.value = value

    def match(self, row) -> bool:
        cell = row.data.get(self.column)
        if cell is None:
            return False
        try:
            cell_val = float(cell)
            value_val = float(self.value)
            if self.operator == '>':
                return cell_val > value_val
            elif self.operator == '<':
                return cell_val < value_val
            elif self.operator == '=':
                return cell_val == value_val
            else:
                raise FilterFormatError(f"Wrong operator: {self.operator}")
        except ValueError:
            cell_val = str(cell)
            value_val = str(self.value)
            if self.operator == '>':
                return cell_val > value_val
            elif self.operator == '<':
                return cell_val < value_val
            elif self.operator == '=':
                return cell_val == value_val
            else:
                raise FilterFormatError(f"Wrong operator: {self.operator}")


class FilterFactory:
    @staticmethod
    def create(where: Optional[str]):
        if not where:
            return None
        is_valid = re.fullmatch(r"([a-zA-Z0-9_ ]+)([><=])([^><=]+)", where)
        if not is_valid:
            raise FilterFormatError(f"Invalid where format: {where}")
        column, operator, value = is_valid.group(1).strip(), is_valid.group(2), is_valid.group(3).strip()
        return OperatorFilter(column, operator, value)
