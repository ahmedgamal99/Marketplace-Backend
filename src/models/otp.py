from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.sql.schema import Column
from src.database import Base

class Otp(Base):
    __tablename__ = 'otp'
    email = Column(String, ForeignKey('users.email', ondelete='CASCADE'),  nullable=False, primary_key=True)
    otp = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    attempts = Column(Integer, nullable=False, default=4)


