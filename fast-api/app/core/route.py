import jwt
import json
import requests
from requests.models import HTTPBasicAuth
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from ..config import (
    ALGORITHM, SECRET_KEY, WEBSERVER_URL, 
    AIR_LOGIN, AIR_PASSWORD
    )
from .model import (
    CreateUser, 
    UserAuthentification, 
    get_current_active_user,
    check_dag,
    user_share_dag
    )
from .schema import DagShare, Token, DagRuns, User


auth = APIRouter()
dag = APIRouter()
users = []

    
@auth.post('/create_user')
async def create_user(username: str, password: str, role: str):
    """
    """
    user = CreateUser()
    new_user = user.create_user(username, password, role)
    users.append(new_user)
    return new_user

@auth.get('/users_list')
async def get_users():
    return users

@auth.post('/create_token', response_model=Token)
async def create_token(form: OAuth2PasswordRequestForm=Depends()):
    """
    """
    auth = UserAuthentification(users)
    user = auth.authenticate_user(form.username, form.password)
    if user[0]:
        token = jwt.encode(user[1], SECRET_KEY, ALGORITHM)
        return {"access_token": token}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='User cannot be authorized'
    )


@dag.get('/list')
async def get_list_dags(token: str=Depends(get_current_active_user)):
    """
    """
    url = "{WEBSERVER_URL}/api/v1/dags"
    resp = requests.get(
        url,
        auth=HTTPBasicAuth(AIR_LOGIN, AIR_PASSWORD)
    )
    return resp.json()


@dag.post('/trigger')
async def trigger_dag(
    dag_id: str, 
    body: DagRuns,
    token: str=Depends(get_current_active_user)
    ):

    accept = check_dag(token["username"], users, dag_id)
    print(f"trigger accept: {accept}")
    
    if (token["role"] == "superuser") or (accept and token["role"] == "user"):
        url = f"{WEBSERVER_URL}/api/v1/dags/{dag_id}/dagRuns"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        resp = requests.post(
            url,
            auth=HTTPBasicAuth(AIR_LOGIN, AIR_PASSWORD),
            data=json.dumps(body.parameters),
            headers=headers
        )
        return resp.json()
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'User have not permissions to trigger dag_id: {dag_id}'
    )


@dag.post('/submit')
async def submit_new_dag(
    file: UploadFile = File(...),
    token: str=Depends(get_current_active_user)
    ):
    path = f"opt/airflow/dags/{file.filename}"
    with open(path, "wb+") as file_object:
        file_object.write(file.file.read())
    
    for user in users:
        if token["username"] == user["username"]:
            user["dags"].append(str(file.filename).split(".")[0])

    return {"info": f"file '{file.filename}' saved at '{path}'"}


@dag.get('/status')
async def check_status(
    dag_id: str, 
    dag_run_id: str,
    token: str=Depends(get_current_active_user)
    ):
    url = f"{WEBSERVER_URL}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}"
    resp = requests.get(
        url,
        auth=HTTPBasicAuth(AIR_LOGIN, AIR_PASSWORD)
    )
    return resp.json()

@dag.get('/share')
async def share_dag(
    dag_id: str,
    username: str,
    token: str=Depends(get_current_active_user)
    ):
    accept = user_share_dag(users, dag_id, username)
    print(f"share accept: {accept}")
    if not accept:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Cannot found user: {username}'
        )
    return {
        "message": f"dag_id: {dag_id} shared to user: {username}"
    }
