import pandas as pd


class OlvRecord:
    def __init__(self, id, kwargs):
        self.id = id
        for k,v in kwargs.items():
            setattr(self, k, v)


def add_error_cause(row):
    if row['Payment Status'] == 'Success':
        return '-'
    else:
        return ''


def load_and_convert(pathname, sheetname):
    df = pd.read_excel(pathname, sheet_name=sheetname)
    df = df.dropna(how='all').fillna('')
    df['error_cause'] = df.apply(add_error_cause, axis=1)
    columns = {}
    for col in df.columns:
        columns[col] = col.replace(' ', '_').lower()
    df = df.rename(columns=columns)
    records = []
    for idx, row in df.iterrows():
        records.append(OlvRecord(idx, row.to_dict()))
    return records, df.columns

