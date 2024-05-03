
from sqlalchemy.orm import Session

from schemas.auth import User
from models.auth import User as UserModel

def get_user_inDB(db:Session):
    users = db.query(UserModel).all()
    out_users = [User(**user.__dict__) for user in users]
    return out_users
    
def get_user_by_username(username:str, db:Session):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    return user

def create_new_user(new_user:User, db:Session):
    db_user = UserModel(**new_user.__dict__)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user