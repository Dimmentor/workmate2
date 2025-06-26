import os
import argparse
from tabulate import tabulate
from services.aggregations import AggregatorFactory
from services.exceptions import CSVProcessorError, FilterFormatError, AggregateFormatError
from services.filters import FilterFactory
from services.utils import read_csv


def main():
    """Можно добавлять желаемые аргументы для последующего расширения"""
    parser = argparse.ArgumentParser(description='CSV processing')
    parser.add_argument('--file', required=True, help='Path to .csv')
    parser.add_argument('--where', help='Filter, for example: "rating>4.7"')
    parser.add_argument('--aggregate', help='Aggregation, for example: "rating=avg"')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File not found: {args.file}")
        return
    try:
        rows = read_csv(args.file)
        filter_obj = FilterFactory.create(args.where)
        if filter_obj:
            rows = [row for row in rows if filter_obj.match(row)]
        if args.aggregate:
            agg_result = AggregatorFactory.create(args.aggregate)
            if agg_result is None:
                print("Error: Invalid aggregate argument.")
                return
            col, aggregator = agg_result
            try:
                values = [float(row.data[col]) for row in rows]
            except Exception:
                print(f"Error: Column '{col}' contains non-numeric values.")
                return
            result = aggregator.aggregate(values)
            print(f"{col} {args.aggregate.split('=')[1]}: {result}")
        else:
            if rows:
                print(tabulate([row.data for row in rows], headers="keys", tablefmt="grid"))
            else:
                print("Error: There is no data matching the filter.")
    except (CSVProcessorError, FilterFormatError, AggregateFormatError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
