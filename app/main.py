from fastapi import FastAPI
from routes.user import user
from routes.dog import dog


app = FastAPI(title="Guane-Intern-FastAPI",
              description="REST API builded using FastAPI framework and MondoDB as database."
              )

app.include_router(user)
app.include_router(dog)
