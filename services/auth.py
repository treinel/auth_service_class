
from fastapi import Depends
from schemas.auth import User, UserLogin
from models.auth import User as UserModel
from config.db import get_db
from utils.jwt_manage import encode_jwt

from sqlalchemy.orm import Session


def get_user_by_username_and_role(data: dict, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == data["username"] and UserModel.role==data['role']).first()
    return user
    
def get_token(data: dict):
    return encode_jwt(data)

def validate_password(db_user: UserModel, user:UserLogin):
    if db_user.password == user.password:
            
        token = get_token(User(**db_user.__dict__).__dict__)

        return token
    else:
        return None
