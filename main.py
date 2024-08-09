from fastapi import FastAPI, Request
from exceptions import MentoverseException
from router import user, course
from db import models
from db.database import engine
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(user.router)
app.include_router(course.router)


@app.exception_handler(MentoverseException)
def mentoverse_exception_handler(request: Request, exc: MentoverseException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )

models.Base.metadata.create_all(engine)
