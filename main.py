from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    name: str
    address: str
    age: int
    birthday: str
    mobile: str

db = {}

@app.post("/person/")
def create_person(person: Person):
    if person.mobile in db:
        raise HTTPException(status_code=400, detail="Mobile already exists")
    db[person.mobile] = person
    return {"message": "Person created", "data": person}

@app.get("/person/{mobile}")
def read_person(mobile: str):
    if mobile not in db:
        raise HTTPException(status_code=404, detail="Person not found")
    return db[mobile]

@app.put("/person/{mobile}")
def update_person(mobile: str, person: Person):
    if mobile not in db:
        raise HTTPException(status_code=404, detail="Person not found")
    db[mobile] = person
    return {"message": "Person updated", "data": person}

@app.delete("/person/{mobile}")
def delete_person(mobile: str):
    if mobile not in db:
        raise HTTPException(status_code=404, detail="Person not found")
    del db[mobile]
    return {"message": "Person deleted"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ideally specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
