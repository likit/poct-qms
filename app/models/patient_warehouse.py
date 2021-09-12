from app.extension import PatientBase
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey


class TestFact(PatientBase):
    __tablename__ = 'test_fact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_datetime = Column(DateTime)
    test_date_id = Column(ForeignKey('dim_dates.id'))
    operator_id = Column(ForeignKey('dim_operators.id'))
    analyzer_id = Column(ForeignKey('dim_analyzers.id'))


class DimOperator(PatientBase):
    __tablename__ = 'dim_operators'
    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_id = Column(Integer, unique=True, nullable=False)
    fullname = Column(String(255), nullable=False)


class DimDate(PatientBase):
    __tablename__ = 'dim_dates'
    id = Column(Integer, primary_key=True)
    day = Column(Integer)
    month = Column(Integer)
    quarter = Column(Integer)
    day_no = Column(Integer)
    gregorian_year = Column(Integer)
    fiscal_year = Column(Integer)


class DimAnalyzer(PatientBase):
    __tablename__ = 'dim_analyzers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(16), nullable=False)
