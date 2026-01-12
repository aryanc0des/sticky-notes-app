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
