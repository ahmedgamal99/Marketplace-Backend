from fastapi import APIRouter, Depends, HTTPException, status
from src.utils.auth import Authentication
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.transactions import Transaction
from src.models.post import Post
from src.models.user import User


transactions = APIRouter()
auth = Authentication()


@transactions.get("/get_transactions")
async def get_transactions(user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    sold_transactions = db.query(Transaction).filter_by(
        from_user=user["id"]).all()

    bought_transactions = db.query(Transaction).filter_by(
        to_user=user["id"]).all()

    response = {
        "sold": [],
        "bought": []
    }

    for s_transaction in sold_transactions:
        curr_p = db.query(Post).filter_by(
            post_id=s_transaction.post_id).all()[0]
        curr_transaction = {
            "title": curr_p.title,
            "description": curr_p.desc,
            "price": curr_p.price,
            "to": db.query(User).filter_by(user_id=s_transaction.to_user).all()[0].name
        }

        response["sold"].append(curr_transaction)

    for b_transaction in bought_transactions:
        curr_p = db.query(Post).filter_by(
            post_id=b_transaction.post_id).all()[0]
        curr_transaction = {
            "title": curr_p.title,
            "description": curr_p.desc,
            "price": curr_p.price,
            "from": db.query(User).filter_by(user_id=b_transaction.from_user).all()[0].name
        }

        response["bought"].append(curr_transaction)

    return response
