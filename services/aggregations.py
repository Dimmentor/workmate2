import re
from abc import ABC, abstractmethod
from typing import List, Any, Optional
from services.exceptions import AggregateFormatError


class Aggregator(ABC):
    @abstractmethod
    def aggregate(self, values: List[float]) -> Any:
        pass


class AvgAggregator(Aggregator):
    def aggregate(self, values: List[float]) -> float:
        return sum(values) / len(values) if values else float('Not a Number')


class MinAggregator(Aggregator):
    def aggregate(self, values: List[float]) -> float:
        return min(values) if values else float('Not a Number')


class MaxAggregator(Aggregator):
    def aggregate(self, values: List[float]) -> float:
        return max(values) if values else float('Not a Number')


class AggregatorFactory:
    @staticmethod
    def create(aggregate: Optional[str]):
        if not aggregate:
            return None
        m = re.match(r"(.+?)=(avg|min|max)", aggregate)
        if not m:
            raise AggregateFormatError(f"Error: Invalid aggregate format: {aggregate}")
        column, func = m.group(1).strip(), m.group(2)
        if func == 'avg':
            return column, AvgAggregator()
        elif func == 'min':
            return column, MinAggregator()
        elif func == 'max':
            return column, MaxAggregator()
        else:
            raise AggregateFormatError(f"Error: Unknown aggregation: {func}")
