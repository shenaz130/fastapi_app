import schema
from .database2 import client, session 
   

def test_root(client,session):
    res = client.get("/")
    print(res.json().get('message'))


def test_create_user(client,session):
    res = client.post("/users/createuser",json= {"email": "hello@gmail.com", "password": "pass123"})
    #print(res.json())
    new_user = schema.UserRes(**res.json())
    assert new_user.email == "hello@gmail.com" 
    assert res.status_code ==201

def test_login(client):
    res = client.post("/login", data ={"username": "hello@gmail.com", "password": "pass123"})
    print(res.json())  # Print response to see what went wrong
    assert res.status_code == 200  # Expecting 201 Created
   