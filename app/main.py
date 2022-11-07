from sqlalchemy.engine import Engine
from fastapi import APIRouter
from app.database import get_engine
from app import admin
from app.router import router
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from sqladmin import Admin, ModelView
from fastapi import FastAPI
import jinja2

# patch https://jinja.palletsprojects.com/en/3.0.x/changes/
# pass_context replaces contextfunction and contextfilter.
jinja2.contextfunction = jinja2.pass_context
# flake8: noqa F402


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

engine: Engine = get_engine()
sql_admin = Admin(app, engine)

sql_admin.add_view(admin.user.UserAdmin)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    """Redirect to documentation"""
    return RedirectResponse(url="/api/docs")


# @app.get("/")
# def root():
#     return {"Hello": "Hello World"}
