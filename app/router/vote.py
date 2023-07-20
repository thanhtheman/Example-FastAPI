from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schema, database, oauth2, models

router = APIRouter(prefix="/votes", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schema.Vote, db: Session=Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):
    #what if there is no post? Ok, the guy handles it now with a 404 message. This is an interesting point in term of error handling, please check note.
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exist.")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"This post id {vote.post_id} was already voted by user id {current_user.id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Your vote has been added successfully."}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You have not voted for this post {vote.post_id}.")
        vote_query.delete()
        db.commit()
        return {"message": "vote was successfully deleted"}
        
    
