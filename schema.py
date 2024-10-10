from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title : str
    content : str
    is_published : bool = True

class PostCreate(PostBase):
    pass

#these above 2 classes- user sending us data

#this class is for us sending response to user

class UserRes(BaseModel):
    email : EmailStr
    id : int
    created_at :datetime

    class Config:
        orm_mode = True

class Post1(PostBase):
    id : int
    title : str
    content : str
    created_at :datetime
    owner_id : int
    owner : UserRes

    class Config:
        orm_mode = True
 
"""class PostOut(BaseModel):
    post : PostBase
    Post1 : Post1
    votes :int

    class Config:
        orm_mode = True"""

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    vote_count: int

    class Config:
        orm_mode = True
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str
   


class UserLogin(BaseModel):
    email : EmailStr
    password : str
 
class Token(BaseModel):
    acess_token :str
    token_type : str

class TokenData (BaseModel):
    id: str


class Vote(BaseModel):
    tweet_id: int
    dir : conint(le=1) #lesser than or equal to 1
    