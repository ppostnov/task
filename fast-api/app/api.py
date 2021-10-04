from fastapi import FastAPI

from .root import route as root_router
from .core.route import auth  as auth_router
from .core.route import dag  as dag_router


app = FastAPI()
app.include_router(root_router.router)
app.include_router(dag_router, prefix='/dags')
app.include_router(auth_router, prefix='/auth')
