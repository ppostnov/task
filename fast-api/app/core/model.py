import jwt
from .schema import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from ..config import SECRET_KEY, USER_FORM, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/create_token')


class CreateUser(object):
    """
    """
    def create_user(self, username: str, password: str, role: str) -> dict:
        """
        """
        user_form = USER_FORM.copy()
        user_form.update({"username": username})
        user_form.update({"role": role})
        user_form.update(
            {
                "encoded_password": jwt.encode(
                    {"password": password}, 
                    SECRET_KEY, 
                    ALGORITHM
                )
            }
        )
        return user_form

class UserAuthentification(object):
    """
    """
    def __init__(self, users: list):
        self.users = users

    def authenticate_user(self, username: str, password: str) -> list:
        """
        """
        auth_flag = False
        for user in self.users:
            if user["username"] == username:
                encode_password = jwt.encode(
                    {"password": password},
                    SECRET_KEY,
                    ALGORITHM
                )
                if user["encoded_password"] == encode_password:
                    auth_flag = True
                    return [auth_flag, user]
        return [auth_flag]


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

def get_current_active_user(
    current_user: User = Depends(get_current_user)
    ):
    return current_user

def check_dag(current_user: str, users: list, dag_id) -> bool:
    """
    """
    for user in users:
        if current_user == user["username"]:
            for dag in user["dags"]:
                if dag == dag_id:
                    print(dag_id, dag, user["dags"])
                    return True
    return False

def user_share_dag(users: list, dag_id: str, username:str) -> bool:
    """
    """
    for user in users:
        if username == user["username"]:
            print(user["username"])
            user["dags"].append(dag_id)
            return True
    return False
