class OlvTestStatus:
    def __init__(self, id):
        self.id = id


def convert_results(results, attr):
    """Convert results to Olv objects """
    records = []
    for record in results:
        row = OlvTestStatus(record.id)
        setattr(row, attr, getattr(record, attr))
        records.append(row)
    return records


def show_all_records(session, model, attr):
    records = session.query(model).all()
    return convert_results(records, attr)


def add_record(session, value, model, attr):
    record = model()
    setattr(record, attr, value)
    try:
        session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()
        return False, str(e)
    return True, 'Succeeded.'


def save_record(session, row, new_value, model, attr):
    if new_value and row:
        record = session.query(model).get(row.id)
        setattr(record, attr, new_value)
        try:
            session.add(record)
            session.commit()
        except Exception as e:
            session.rollback()
            return False, str(e)
        return True, 'Succeeded.'
    else:
        return False, 'Empty status not allowed.'


def delete_record(session, row, model):
    if row:
        record = session.query(model).get(row.id)
        try:
            session.delete(record)
            session.commit()
        except Exception as e:
            session.rollback()
            return False, str(e)
        return True, 'Succeeded.'
    else:
        return False, 'No row selected.'
