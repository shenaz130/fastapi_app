from fastapi.testclient import TestClient
from main import app
import schema
import pytest
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import get_db, Base

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:9586@localhost:5432/postgres_test'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
 
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope= "module")
def session():
    Base.metadata.create_all(bind=engine) #to create tables
    #Base.metadata.drop_all(bind=engine) #to delete tables
    
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope= "module")
def client(session):
    def overide_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]= overide_get_db
    yield TestClient(app) #run the test code