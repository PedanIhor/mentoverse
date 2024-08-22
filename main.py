from fastapi import FastAPI, Request
from router import user, course, appointments
from db import models
from db.database import engine
from fastapi.responses import JSONResponse
from auth import authentication
import uvicorn

app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(appointments.router)


models.Base.metadata.create_all(engine)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
