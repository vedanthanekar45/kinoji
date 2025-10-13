from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class Directors(str, Enum):
    Christopher_Nolan = "nolan"
    David_Fincher = "fincher"
    Quentin_Tarantino = "tarantino"

@app.get("/")
async def root():
    return {"message": "Hello, World"}

@app.get("/movies/{movie_id}")
async def read_item(movie_id: int):
    return {"item_id": movie_id}

@app.get("/directors/{director_name}")
async def read_director(director_name: Directors):
    if director_name is Directors.Christopher_Nolan:
        return {"director_name": director_name, "message": "Time is always one of the cast!"}
    
    if director_name == "fincher":
        return {"director_name": director_name, "message": "Mystery is always one of the cast!"}
    
    return {"director_name": director_name, "message": "Have some residuals"}