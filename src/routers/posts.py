from fastapi import APIRouter, Depends, HTTPException, status
from src.utils.auth import Authentication
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.post import Post
from src.models.user import User
from src.models.transactions import Transaction
from src.schemas.posts import CreatePost, IdentifyPost
from src.schemas.transaction import CreateTransaction

posts = APIRouter()
auth = Authentication()


@posts.post("/create_post")
async def create_post(data: CreatePost, user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    to_create = Post(
        user_id=user["id"],
        title=data.title,
        desc=data.desc,
        img=data.img,
        sold=False,
        created_at=data.created_at,
        price=data.price
    )
    try:
        db.add(to_create)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error has occured, please try again later",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "success": True,
        "created_id": to_create.post_id
    }


@posts.post("/remove_post")
async def remove_post(data: IdentifyPost, user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    req_post = db.query(Post).filter_by(post_id=data.post_id).all()

    if user["id"] == req_post[0].user_id:
        db.query(Post).filter_by(post_id=data.post_id).delete()
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The post you're trying to remove is not yours!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "success": True
    }


@posts.get("/list_posts")
async def list_posts(user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    to_return = set()
    for post in db.query(Post).filter_by(sold=False).all():

        if post.user_id == user["id"]:
            continue

        curr_post = Post(post_id=post.post_id, user_id=db.query(
            User).filter_by(user_id=post.user_id).all()[0].name, title=post.title, price=post.price, desc=post.desc)

        to_return.add(curr_post)

    return to_return


@posts.put("/buy_post")
async def buy_post(data: IdentifyPost, user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    req_post = db.query(Post).filter_by(post_id=data.post_id).all()[0]
    req_post.sold = True
    db.commit()

    print(req_post.user_id)
    to_create = Transaction(
        post_id=req_post.post_id,
        from_user=req_post.user_id,
        to_user=user["id"]
    )

    db.add(to_create)
    db.commit()
    return {
        "success": True
    }
