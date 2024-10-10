from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import models, schema, utils
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import bcrypt
from router import post, user, auth, vote
from config import settings

print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

#Base = declarative_base()

app= FastAPI()

origins = ["http://www.google.com", "http://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""class TweetSchema(BaseModel):
    title = str
    content: str
    is_published : bool = True

class Config:
        orm_mode = True 

class Tweets(Base):
    __tablename__ = "tweet_tbl"

    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String,nullable= False)
    content = Column(String,nullable= False)
    published = Column(Boolean, server_default="TRUE", nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False, server_default= text('now()'))"""

try:
    conn = psycopg2. connect(host = 'localhost', database= 'postgres', user = 'postgres', password='9586', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Database sucessfully connected!!!!!")

except Exception as error:
    print("Database conncection failed!!!", error)

my_posts = [{"title": "title 1 for p1", "content":"Content 1 for p1", "id":1},{"title": "title 2 for p2", "content":"Content 2 for p2", "id":2}]

def Find_Post(id):
    for x in my_posts:
        if x["id"] == id:
            return x
        
def Find_Index(id):
    for i, x in enumerate(my_posts):
        if x["id"]== id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome on-board Shenaz"}

#------------------POST QUERIES -----------SQL & ORM----------------------------------------#

#------------------USER QUERIES --------------------------------------------------------------#


   

