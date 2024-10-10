from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import models, schema, utils, Oauth2
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router= APIRouter(
   tags= ['Authentication']
)

@router.post("/login", response_model= schema.Token)
#def login(user_cred: schema.UserLogin, db: Session = Depends(get_db)):
def login(user_cred:OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):

    #user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail=f" credentials invalid !!!!")
    
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail=f" credentials invalid !!!!")
        
    access_token = Oauth2.create_token(data = {"user_id": user.id})


    return{ "acess_token":access_token,"token_type":"bearer"}