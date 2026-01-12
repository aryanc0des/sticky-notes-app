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
        
db_dependency = Annotated[LocalSession, Depends(get_db)]