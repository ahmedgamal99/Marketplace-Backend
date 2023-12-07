from sqlalchemy import Integer, String, Sequence
from sqlalchemy.sql.schema import Column
from src.database import Base


class User(Base):
    __tablename__ = 'users'
    user_id_seq = Sequence('user_id_seq')
    user_id = Column(Integer, user_id_seq, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
