import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
import schema, database, models
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

#creating a token
# 1.SECRET_KEY
# 2.ALGORITHM
#3.Expiration_time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

#when user sends the credentials, creating a token
def create_token(data:dict):
    to_encode = data .copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

    return encoded_jwt

#taking he token to decode user_id
def verify_token(token : str, credential_exception):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = str(decoded_jwt.get("user_id"))
        #extracting the user_id
        if id is None:
            raise credential_exception
        token_data= schema.TokenData(id = id)

    except PyJWTError :
        raise credential_exception
    return token_data
    
#taking the user to retreive the data
def get_current_user(token :str = Depends(oauth2_scheme), db: Session = Depends(get_db) ):
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                                         detail=f"Cound't validate credentials",
                                         headers= {"WWW-Authenticate": "Bearer"})
    
    token = verify_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user