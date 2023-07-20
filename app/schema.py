from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint
#this is the pydantic model, it helps with data type of the post
class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True

# define exactly the schema in the response sent back to the user
class PostResponse(Post):
    id: int
    owner_id: int
    owner: UserResponse
    # this class inherits title, content, published from the Post class
    # the below code is to ensure pydantic can read non-dictionary format. Our post is an SQLAlchemy object, not a python dictionary.
    # The tutorial guy says we need the class Config, but removing it doesn't affect much. I just leave it here to follow him. His was orm_mode = True
    # The doc says orm_mode is deprecated.
    class Config:
        from_attributes = True

# this is the updated returned data with the number of votes attached to each post
class PostResponseWithVote(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

# this is to make sure we send out the token in a specific format
class Token(BaseModel):
    access_token: str
    token_type: str


# this is to verify the user_id that we get back after decoding the token submmited by user
# then we extract the id from the payload.
class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)