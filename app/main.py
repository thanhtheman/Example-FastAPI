
from fastapi import FastAPI
from . import models
from .database import engine
from .router import post, user, authentication, vote
#enabling CORS
from fastapi.middleware.cors import CORSMiddleware

#this is to set up the connection of our models to the databse
#after setting up Alembic, we will need to comment this out.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.yorku.ca", "https://www.google.ca"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)
    
@app.get('/')
def home ():
    return {"message": "This is the home page MY FREN"}




