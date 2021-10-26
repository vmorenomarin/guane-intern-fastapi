from fastapi import FastAPI

app = FastAPI()

# Path operation definitions with path parameters and query parameters.

## Request and Response Body

@app.get("/")
async def home():
    return {"message": "Ok"}

@app.get("/api/dogs")
async def dogs():
    return {"message": "list dogs"}

@app.get("/api/dogs/{dog_name}")
async def show_dog(dog_name: str):
    return {"dog_name": dog_name}

@app.get("/api/dogs?is_adopted=True")
async def is_adopted():
    return {"dog_name": dog_name}


@app.post("dog/new")
async def create_dog():
    pass