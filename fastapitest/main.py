"""from webbrowser import get
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"Data": "Testing"}

@app.get("/about")
def about():
    return{"Data":"About"}



"""
from fastapi import FastAPI
from pydantic import BaseModel
import databases
from typing import List

database = databases.Database('sqlite+aiosqlite:///./test.db')


class Task(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/tasks/", response_model=List[Task])
async def read_notes():
    query = "SELECT id, text, completed FROM tasks"
    return await database.fetch_all(query)
"""
"""
import databases
import schemas
import models
import databases
from typing import List
from fastapi import Depends, FastAPI, status, HTTPException
from database import Base, engine
from pydantic import BaseModel
from typing import List
from database import SessionLocal


database = databases.Database('sqlite+aiosqlite:///./todooo.db')

# Initialize app
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDo):

    # create a new database session
    session = SessionLocal(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    tododb = models.ToDo(Task = todo.Task)

    # add it to the session and commit it
    session.add(tododb)
    session.commit()

    # grab the id given to the object from the database
    id = tododb.id

    # close the session
    session.close()

    return tododb


# <other imports not shown here>


@app.get("/todo", response_model=List[schemas.ToDo])
def read_todo_list():
    # create a new database session
    session = SessionLocal()

    # get all todo items
    todo_list = session.query(models.ToDo).all()

    # close the session
    session.close()

    return todo_list


@app.put("/todo/{id}")
def update_todo(id: int, Task: str):

    # create a new database session
    session = SessionLocal()
    # get the todo item with the given id
    todo = session.query(models.ToDo).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if todo:
        todo.Task = Task
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(
            status_code=404, detail=f"todo item with id {id} not found")

    return todo


@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    # create a new database session
    session = SessionLocal()
    # get the todo item with the given id
    todo = session.query(models.ToDo).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"todo item with id {id} not found")

    return None


@app.get("/todo")
def read_todo_list():
    # create a new database session
    session = SessionLocal()
    # get all todo items
    todo_list = session.query(models.ToDo).all()

    # close the session
    session.close()

    return todo_list
    
