from fastapi import *
from pydantic import *
from starlette import *
from database import *
import models
from models import *
from sqlalchemy.orm import *
from typing import *

app = FastAPI()

models.Base.metadata.create_all(bind=db_engine)

class addNewNote(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/', status_code=status.HTTP_200_OK)
async def home():
    return {"message":"ok, server working"}

@app.get('/notes', status_code=status.HTTP_200_OK)
async def get_all_notes(db: db_dependency):
    notes_to_return = db.query(Notes).all() 
    return notes_to_return

@app.post('/notes/new_note', status_code=status.HTTP_201_CREATED)
async def create_new_note(db: db_dependency, new_note: addNewNote):
    note_to_add = Notes(**new_note.model_dump())
    
    db.add(note_to_add)
    db.commit()
    
    raise HTTPException(status_code=201, detail='new note created sucessfully')

@app.get('/notes/detailed_note/{id}', status_code=status.HTTP_200_OK)
async def get_note_by_id(db: db_dependency, id: int):
    note_to_return = db.query(Notes).filter_by(id=id).first()
    if note_to_return is not None:
        return note_to_return
    else:
        raise HTTPException(status_code=404, detail='note not found')
