from sqlalchemy import Integer, String, Sequence, ForeignKey, Boolean, func, DateTime
from sqlalchemy.sql.schema import Column
from src.database import Base


class Post(Base):
    __tablename__ = 'posts'
    post_id_seq = Sequence('user_id_seq')
    post_id = Column(Integer, post_id_seq, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    title = Column(String, nullable=False)
    desc = Column(String, nullable=True)
    img = Column(String, nullable=True)
    sold = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    price = Column(Integer, nullable=False)
