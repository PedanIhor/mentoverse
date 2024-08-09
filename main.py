from fastapi import FastAPI
from router import user, course
from db import models
from db.database import engine

app = FastAPI()
app.include_router(user.router)
app.include_router(course.router)

models.Base.metadata.create_all(engine)
