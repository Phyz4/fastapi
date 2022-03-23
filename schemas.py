"""from pydantic import BaseModel


# Create ToDo Schema (Pydantic Model)
class ToDoCreate(BaseModel):
    Task: str

# Complete ToDo Schema (Pydantic Model)
class ToDo(BaseModel):
    id: int
    Task: str

    #class Config:
       #orm_mode = True

       """