from fastapi import APIRouter, status, Depends, HTTPException
from .. import schema, models, utils, oauth2
from..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["authentication"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schema.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends() , db: Session=Depends(get_db)):
    #Oauth form doesn't have email field, it has a username filed, on Postman, we also need to submit a form instead of a body.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Crendentials!")
    if not utils.user_verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}