from pydantic import BaseModel

class Token(BaseModel):
    access_token: str

class User(BaseModel):
    username: str
    encoded_password: str
    dags: list

class DagRuns(BaseModel):
    parameters: dict

class DagShare(BaseModel):
    username: str
    dag_id:str