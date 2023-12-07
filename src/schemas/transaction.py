from pydantic import BaseModel


class CreateTransaction(BaseModel):
    post_id: int
    from_user: int
    to_user: int
