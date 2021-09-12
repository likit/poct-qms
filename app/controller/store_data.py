from calendar import Calendar
from datetime import date

from sqlalchemy.orm import sessionmaker
from app.extension import patient_engine
from app.models.patient_warehouse import *

Session = sessionmaker(bind=patient_engine)
session = Session()

quarters = {
    1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4
}


def insert_dates(year):
    c = Calendar()
    newyear_date = date(year, 1, 1)
    for month in range(1, 13):
        for d in c.itermonthdates(year, month):
            if d.year == year:
                if session.query(DimDate).filter(DimDate.day == d.day,
                                                 DimDate.month == d.month,
                                                 DimDate.gregorian_year == d.year).first():
                    continue
                else:
                    if d.month != month:
                        continue
                    from_newyear = d - newyear_date
                    if d.month < 9:
                        fiscal_year = d.year - 1
                    else:
                        fiscal_year = d.year
                    date_id = str(d.year) + '{0:02d}'.format(d.month) + '{0:02d}'.format(d.day)
                    date_id = int(date_id)
                    new_date = DimDate(id=date_id,
                                       day=d.day,
                                       month_no=d.month,
                                       month=d.strftime('%B'),
                                       quarter=quarters[d.month],
                                       gregorian_year=d.year,
                                       day_of_year=from_newyear.days + 1,
                                       day_of_week=d.weekday(),
                                       buddhist_year=d.year + 540,
                                       fiscal_year=fiscal_year,
                                       weekday=d.strftime('%A'))
                    session.add(new_date)
                    session.commit()


def store_data(records):
    years = set()
    for rec in records:
        year = rec.test_datetime.year
        if year not in years:
            _rec = session.query(DimDate).filter(DimDate.gregorian_year == year).first()
            if not _rec:
                insert_dates(year)
            years.add(year)
        date_id = rec.test_datetime.strftime('%Y%m%d')
        operator = session.query(DimOperator).filter(DimOperator.operator_id == int(rec.operator_id)).first()
        if not operator:
            operator = DimOperator(
                fullname=rec.operator_name,
                operator_id=rec.operator_id,
            )
        analyzer = DimAnalyzer(no=rec.analyzer_no)
        fact = TestFact(
            test_date_id=date_id,
            test_datetime=rec.test_datetime,
            analyzer=analyzer,
            operator=operator,
            status=rec.payment_status,
            error_cause=rec.error_cause
        )
        session.add(fact)
    session.commit()
