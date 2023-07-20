
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schema, oauth2
from typing import List, Optional # we need this for Pydantic to apply the post response structure to the list of all posts - get all posts
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["post"])


# @router.get('/', status_code=status.HTTP_200_OK, response_model=List[schema.PostResponse])
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schema.PostResponseWithVote])
def get_posts(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, 
              skip: int = 0, search: Optional[str] = ""):
    print(current_user.email)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.PostResponseWithVote)
def get_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    print(f"The post owner id is {post.Post.owner_id}")
    if post.Post.owner.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to view post id {id}")
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.Post, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # what if we have 50 fields?
    # new_post = models.Post(title=post.title, content=post.content)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {id} was not found")
    if post.first().owner_id == current_user.id:
        post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to delete post id {id}")
    return {"message": "Your post was successfully deleted."}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.PostResponse)
def update_post(id: int, post: schema.Post, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post_query.first().owner_id == current_user.id:
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to delete post id {id}")
    return post_query.first()
