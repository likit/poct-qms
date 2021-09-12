from app.extension import PatientBase
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship


class TestFact(PatientBase):
    __tablename__ = 'test_fact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_datetime = Column(DateTime)
    test_date_id = Column(ForeignKey('dim_dates.id'))
    operator_id = Column(ForeignKey('dim_operators.id'))
    analyzer_id = Column(ForeignKey('dim_analyzers.id'))
    status = Column(String(255))
    error_cause = Column(String(255))

    analyzer = relationship('DimAnalyzer')
    operator = relationship('DimOperator')
    test_date = relationship('DimDate')


class DimOperator(PatientBase):
    __tablename__ = 'dim_operators'
    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_id = Column(Integer, unique=True, nullable=False)
    fullname = Column(String(255), nullable=False)


class DimDate(PatientBase):
    __tablename__ = 'dim_dates'
    id = Column(Integer, primary_key=True)
    day = Column(Integer)
    month_no = Column(Integer)
    month = Column(String(16))
    quarter = Column(Integer)
    day_of_year = Column(Integer)
    day_of_week = Column(Integer)
    weekday = Column(String(16))
    buddhist_year = Column(Integer)
    gregorian_year = Column(Integer)
    fiscal_year = Column(Integer)


class DimAnalyzer(PatientBase):
    __tablename__ = 'dim_analyzers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(16), nullable=False)
