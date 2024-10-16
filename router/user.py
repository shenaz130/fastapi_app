from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schema, utils
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router= APIRouter(
   prefix= ("/users"),
   #tags= ['Users']
)

#sqlalchemy Create User
@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model= schema.UserRes)
def createUser(user :schema.UserCreate , db: Session = Depends(get_db)):
    #password hashing
    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@router.get("/{id}", response_model= schema.UserRes)
def getUser (id :int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                           detail=f" user with id :{id} was not found!!!!")
    return user