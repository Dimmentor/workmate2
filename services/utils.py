from typing import List
import csv

from models import Row


def read_csv(file_path: str) -> List[Row]:
    """В случае, если в рейтинге или сумме есть ',' вместо '.' - сработает замена"""
    with open(file_path, encoding='utf-8') as f:
        sample = f.read(1000)
        delimiter = ',' if sample.count(',') > sample.count('\t') else '\t'
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        rows = []
        for row in reader:
            for k, v in row.items():
                if isinstance(v, str) and ',' in v:
                    v_mod = v.replace(',', '.')
                    try:
                        float(v_mod)
                        row[k] = v_mod
                    except ValueError:
                        row[k] = v
            rows.append(Row(row))
        return rows
