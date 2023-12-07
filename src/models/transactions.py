from sqlalchemy import Integer, ForeignKey
from sqlalchemy.sql.schema import Column
from src.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    post_id = Column(
        Integer,
        ForeignKey('posts.post_id', ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
    )
    from_user = Column(
        Integer,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    to_user = Column(
        Integer,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False,
    )
