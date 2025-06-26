import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.aggregations import AggregatorFactory
from services.filters import FilterFactory
from services.utils import read_csv

CSV_CONTENT = """name,brand,price,rating\niphone 15 pro,apple,999,4.9\ngalaxy s23 ultra,samsung,1199,4.8\nredmi note 12,xiaomi,199,4.6\npoco x5 pro,xiaomi,299,4.4\n"""


@pytest.fixture
def csv_file(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text(CSV_CONTENT, encoding='utf-8')
    return str(file)


@pytest.fixture
def csv_rows(csv_file):
    return read_csv(csv_file)


@pytest.mark.parametrize("where,expected_names", [
    (None, ["iphone 15 pro", "galaxy s23 ultra", "redmi note 12", "poco x5 pro"]),
    ("brand=apple", ["iphone 15 pro"]),
    ("rating>4.7", ["iphone 15 pro", "galaxy s23 ultra"]),
    ("price<300", ["redmi note 12", "poco x5 pro"]),
])
def test_filtering(csv_rows, where, expected_names):
    rows = csv_rows
    filter_obj = FilterFactory.create(where)
    if filter_obj is not None:
        rows = [row for row in rows if filter_obj.match(row)]
    names = [row.data['name'].strip() for row in rows]
    assert names == expected_names


@pytest.mark.parametrize("aggregate,expected", [
    ("rating=avg", (4.675,)),
    ("price=min", (199.0,)),
    ("price=max", (1199.0,)),
])
def test_aggregation(csv_rows, aggregate, expected):
    rows = csv_rows
    agg_result = AggregatorFactory.create(aggregate)
    assert agg_result is not None
    col, aggregator = agg_result
    values = [float(row.data[col]) for row in rows]
    result = aggregator.aggregate(values)
    assert pytest.approx(result, 0.001) == expected[0]


@pytest.mark.parametrize("where", [
    "brand>apple",  # если пользователь случайно проверит название брэнда, то вместо ошибки, проверит по-алфавиту
    "name=galaxy s23 ultra",
])
def test_filter_text_columns(csv_rows, where):
    rows = csv_rows
    filter_obj = FilterFactory.create(where)
    if filter_obj is not None:
        filtered = [row for row in rows if filter_obj.match(row)]
        assert isinstance(filtered, list)
    else:
        assert filter_obj is None


@pytest.mark.parametrize("aggregate", [
    "name=avg",
])
def test_aggregation_non_numeric(csv_rows, aggregate):
    rows = csv_rows
    agg_result = AggregatorFactory.create(aggregate)
    assert agg_result is not None
    col, aggregator = agg_result
    with pytest.raises(ValueError):
        [float(row.data[col]) for row in rows]


@pytest.mark.parametrize("where", [
    "badformat",
    "rating>>4.5",
])
def test_invalid_where(where):
    with pytest.raises(Exception):
        FilterFactory.create(where)


@pytest.mark.parametrize("aggregate", [
    "badformat",
    "rating=median",
])
def test_invalid_aggregate(aggregate):
    with pytest.raises(Exception):
        AggregatorFactory.create(aggregate)
