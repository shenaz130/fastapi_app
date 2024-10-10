from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import  ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from database import Base
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#Base = declartive_base()

#Create a Table
class Post(Base):
    __tablename__ = "tweet_tbl"

    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String,nullable= False)
    content = Column(String,nullable= False)
    is_published = Column(Boolean, server_default="TRUE", nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False, server_default= text('now()'))
    owner_id = Column(Integer, ForeignKey("user_tbl.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")

class User(Base):
    __tablename__ = "user_tbl"

    id = Column(Integer, primary_key=True, nullable= False)
    email = Column(String,nullable= False, unique= True )
    password = Column(String,nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False, server_default= text('now()'))

class Vote(Base):
    __tablename__ = "vote_tbl"

    user_id = Column(Integer, ForeignKey("user_tbl.id", ondelete="CASCADE"),primary_key=True, nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweet_tbl.id", ondelete="CASCADE"),primary_key=True, nullable=False) 