from pydantic import BaseModel
from pydantic import Field


# Clase de esquema para la estructura de los datos de usuario
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
