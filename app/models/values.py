from app.extension import Base
from sqlalchemy import Column, String, Integer, DateTime, Date


class TestStatus(Base):
    __tablename__ = 'test_statuses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(255), unique=True, nullable=False)

    def __str__(self):
        return self.status


class ErrorCause(Base):
    __tablename__ = 'error_causes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cause = Column(String(255), unique=True, nullable=False)

    def __str__(self):
        return self.cause
