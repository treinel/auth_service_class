from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse


from pydantic import BaseModel, Field

from config.db import Base, engine, get_db
from sqlalchemy.orm import Session


from fastapi.security import HTTPBearer
from jwt_manage import decode_jwt, encode_jwt

from models.auth import User as UserModel

class JWTBearer(HTTPBearer):

    async def __call__(self, request , db: Session = Depends(get_db)):
        credentials = await super().__call__(request)
        
        print("credentials", credentials)
        data = decode_jwt(credentials.credentials)
        
        if data:
        
            user = db.query(UserModel).filter(UserModel.username == data["username"]).first()
            if user:
                return credentials
            else:
                raise HTTPException(status_code=403, detail="Invalid authorization code")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")


class User(BaseModel):
    username: str 
    email: str = Field(pattern="^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$", default="no@mail.com")
    name: str
    password: str
    role: str
    cel: str

class UserLogin(BaseModel):
    username: str
    password: str

app = FastAPI(title="rest_auth backend", version="0.0.1")

Base.metadata.create_all(bind=engine)

user_db = [
    {
        "username": "reinel",
        "email": "rtabares@gmail.com",
        "name": "Reinel Tabares",
        "password": "123456",
        "role": "admin",
        "cel": "1234567890"
    },
    {   "username": "jose",
        "email": "jose@gmail.com",
        "name": "Jose Perez",
        "password": "123456",
        "role": "user",
        "cel": "1234567890"
    },
    {
        "username": "maria",
        "email": "maria@gmail.com",
        "name": "Maria Lopez",
        "password": "123456",
        "role": "user",
        "cel": "1234567890"
    }
]

@app.get("/")
def hello_world():
    return JSONResponse(content={"message": "Hello, World!"}, status_code=200)


@app.get("/users", tags=['usuarios'])
def get_all_users():
    return JSONResponse(content=user_db, status_code=200)

@app.get("/users/{username}", tags=['usuarios'], dependencies=[Depends(JWTBearer())])
def get_user(username: str):
    for user in user_db:
        if user["username"] == username:
            return JSONResponse(content=user, status_code=200)
    return JSONResponse(content={"message": "User not found"},status_code=404)

@app.post("/users", tags=['usuarios'])
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = UserModel(**user.__dict__)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(content={"message": "User created"}, status_code=201)

@app.post("/login", tags=['auth'])
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if db_user:
        if db_user.password == user.password:
            token = encode_jwt(user.__dict__)
            return JSONResponse(content=token, status_code=200)
        else:
            return JSONResponse(content={"message": "Login failed"}, status_code=401)
    else:
        return JSONResponse(content={"message": "User does not exist"}, status_code=401)
