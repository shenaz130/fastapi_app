from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schema, utils
from typing import Optional, List
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
import Oauth2
from Oauth2 import get_current_user

router= APIRouter(
    prefix= ("/posts"),
    tags= ['Posts']
)

#@router.get("/") 
#@router.get("/",  response_model= List[schema.Post1]) #sqlalchemy SELECT all query 02
@router.get("/", response_model= List[schema.PostOut]) #sqlalchemy Joins, responsemodel
def get_posts(db: Session = Depends(get_db), limit: int =10, skip : int = 0, search : Optional['str']= ""):
#def get_posts(db: Session = Depends(get_db), current_user :int = Depends(Oauth2.get_current_user)):
    
    #tweets= db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #tweets= db.query(models.Post).all()
    tweets = db.query(models.Post).filter(models.Post.title.contains(search)) .limit(limit).offset(skip).all()

    #results = db.query(models.Post)

    results = db.query(models.Post, func.count(models.Vote.tweet_id).label("vote__count")) \
                .join(models.Vote, models.Vote.tweet_id == models.Post.id, isouter=True) \
                .group_by(models.Post.id).all()

    posts = [] #empty list
    for post, vote_count in results: # results contains,post and vote_count
        diccy = post.__dict__  #post means a sqlalchemy obj will convert into python dict
        diccy['vote_count'] = vote_count #add vote_count to the dictionary
        posts.append(diccy) #after modifing the dic, add this dictionary to the list

   
    #return results
    return [schema.PostOut.from_orm(post) for post in tweets] #each tweets convert into postOut model




"""@app.get("/sqlalchemy") #sqlalchemy testing root 01
def test_post(db: Session = Depends(get_db)):
    return {"message": "sqlalchemy Sucess!!"}


@app.get("/posts") 
def getPosts():
    cursor.execute(" SELECT * FROM post_tbl")
    posts= cursor.fetchall()
    return {"data": posts}"""


"""@app.get("/tweets/{tweet_id}", response_model=None)
async def get_tweet(tweet_id: int):
    # Your logic to fetch and return the tweet as a raw dictionary or object
    return {"Youtube"}"""

#sqlalchemy Create Query
@router.post("/createpost", status_code=status.HTTP_201_CREATED,  response_model= schema.Post1)
def createpost(post :schema.PostCreate , db: Session = Depends(get_db),current_user :int = Depends
               (Oauth2.get_current_user),):
    print(current_user.id)
    #new_tweet =models.Post(title=post.title, content = post.content, is_published = post.is_published)
    new_tweet= models.Post(**post.dict())
    #new_tweet= models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet

"""@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def createpost(newp : Post):
    sql = " INSERT INTO post_tbl( title, content, is_published) VALUES (%s, %s, %s) RETURNING * "
    val = (newp.title, newp.content,newp.is_published)
    cursor.execute(sql, val)

    new_post= cursor.fetchone()
    conn. commit()
    return {"data": new_post}
    print("record inserted.")"""
    
#sqlalchemy View One Query
@router.get("/{id}",  response_model= schema.Post1)
def get_post(id:int , db: Session = Depends(get_db),current_user :int = Depends
               (Oauth2.get_current_user) ):
    tweet1 = db.query(models.Post).filter(models.Post.id == id).first()
    print (tweet1)
    if not tweet1:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f" post with id :{id} was not found!!!!")
    
    """if tweet1.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail=f" no authorize to do this!!!!")"""
  
    return tweet1


"""@app.get("/posts/{id}")
def get_post(id:str ):
    cursor.execute("SELECT * FROM post_tbl WHERE id = %s", (str(id),))
    post1 = cursor.fetchone()
    if not post1:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f" post with id :{id} was not found!!!!")
    print(post1)
    return {"post details ": (post1)}"""

#sqlalchemy Delete Query
@router.delete("/{id}")
def deletePost(id :int, db: Session = Depends(get_db),current_user :int = Depends
               (Oauth2.get_current_user) ):
    tweet1_query = db.query (models.Post).filter(models.Post.id == id)

    tweet1 = tweet1_query.first()
    if tweet1 == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f" post with id :{id} was not found!!!!")
    
    """if tweet1.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail=f" no authorize to do this!!!!")"""

    tweet1_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

"""@app.delete("/posts/{id}")
def deletePost(id :int):
    cursor.execute("DELETE FROM post_tbl WHERE id = %s RETURNING * ", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f" post with id :{id} was not found!!!!")

    return Response(status_code= status.HTTP_204_NO_CONTENT)"""

#sqlalchemy Update Query
@router.put("/{id}",  response_model= schema.Post1)
def updatePost(id:int,upd :schema.PostCreate,  db: Session = Depends(get_db),current_user :int = Depends
               (Oauth2.get_current_user)):
    tweet_query = db.query (models.Post).filter(models.Post.id == id)
    post = tweet_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f" post with id :{id} was not found!!!!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail=f" no authorize to do this!!!!")

    tweet_query.update(upd.dict(),synchronize_session= False)
    db.commit()
    return tweet_query.first()

"""@app.put("/posts/{id}")
def updatePost(id:int, updp : Post):
    sql =  "UPDATE post_tbl SET title = %s, content =%s, is_published = %s WHERE id = %s RETURNING * "
    val = updp.title, updp.content, updp.is_published, (str(id),)
    cursor.execute(sql, val)
    #cursor.execute("UPDATE post_tbl SET title = %s, content =%s, is_published = %s WHERE id = %s ", updp.title, updp.content, updp.is_published, (str(id),))
    upd_post = cursor.fetchone()
    conn.commit()
    return {"updated data!!!!!!": upd_post} """