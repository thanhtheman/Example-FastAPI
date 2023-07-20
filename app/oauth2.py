from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from . import schema, database, models
from sqlalchemy.orm import Session
from .config import settings

# this is to require an extra step for any protected route: like logging in
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#secret key
#expired time
#hashing algorith

SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ALGORITHM = settings.algorithm


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # this is to validate the data type of the ID, schema can be called to verify things.
        token_data = schema.TokenData(id=str(id))
        print(f"The current user id is {token_data}")
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials", headers={"WWW-Authenticate": "Bearer"})
    # return verify_access_token(token, credentials_exception)
    # the above return is not really helpful, it only give us an id, with an it we can access the whole user profile
    # because we attach this function as a condition to all protected routes, this is like a gateway for other routes to access the user profile
    # which can be used for various purposes later on.
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user