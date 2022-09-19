from pydantic import BaseModel
from fastapi import FastAPI
from typing import Union
import uvicorn

api = FastAPI()


class Users(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: Union[str, None] = None
    recommendations: list[str]
    ZIP: Union[str, None] = None


users_dict = {}


@api.put("/users")
def create_user(user: Users):
    user = dict(user)
    if user["user_id"] not in users_dict.keys():
        users_dict[user["user_id"]] = user
        return {"Description": f"Usuario creado satisfactoriamente, user_id = {user['user_id']}"}
    else:
        return {"Description": f"Usuario repetido"}


@api.put("/users/update/{user_id}")
def update_user(user: Users, user_id: int):
    user = dict(user)
    if user_id in users_dict.keys():
        users_dict[user_id] = user
        return {"Description": f"Usuario {user['user_id']} actualizado"}
    else:
        return {"Description": f"Usuario {user_id} no existe"}


@api.get("users/{user_id}")
def pprint(user_id: int):
    if user_id in users_dict.keys():
        return {f"user_id {users_dict[user_id]['user_id']}": users_dict[user_id]}
    else:
        return {"Description": f"No existe el {user_id}"}


@api.delete("users/delete/{user_id}")
def delete(user_id: int):
    if user_id in users_dict.keys():
        users_dict.pop(user_id)
        return {"Descrition": f"Se eliminó correctamente al usuario {user_id}"}
    else:
        return {"Description": f"No existe el {user_id}"}


if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=5000, log_level="info", reload=True)
