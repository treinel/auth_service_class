from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from schemas.auth import User
from models.auth import User as UserModel
from services.users import get_user_inDB, get_user_by_username, create_new_user

from config.jwt_depends import JWTBearer

from sqlalchemy.orm import Session
from config.db import get_db



users_router = APIRouter(prefix="/users",tags=["usuarios"],)


# Ruta de obtención de la base de datos #TODO: Conectar a la base de datos y obtener la información.
@users_router.get("/")
def get_all_users(db:Session = Depends(get_db)):

    out_users = get_user_inDB(db)

    return JSONResponse(content=jsonable_encoder(out_users), status_code=200)


# Ruta de obtención de un usuario por su username #TODO: Conectar a la base de datos y obtener la información.
@users_router.get("/{username}")
def get_user(username: str,db:Session = Depends(get_db) , authorized: UserModel = Depends(JWTBearer())):
    
    user = get_user_by_username(username,db)
    if user:
        return JSONResponse(content=User(**user.__dict__).__dict__, status_code=200)
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)

# Ruta para crear un nuevo usuario. #TODO: Hacer routing y Reformar el código a SOLID
@users_router.post("/")
def create_user(user: User, db:Session = Depends(get_db)):
    new_user = create_new_user(user,db)
    if new_user:
        return JSONResponse(content={"message": "User created"}, status_code=201)
    else:
        return JSONResponse(content={"message": "User not created"}, status_code=400)



