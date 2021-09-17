from typing import final
from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import false
from .schemas import Blog
from .database import SessionLocal, engine
from . import models


app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create data Methods
@app.post('/blog')
def get_data(request:Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#read Data Method
@app.get('/blog')
def show_data(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

#read Pertular Data Based On id
@app.get('/blog/{id}')
def show_Perticular_data_on_id(id,db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
    return blogs

@app.delete('/blog/{id}')
def show_Perticular_data_on_id(id,db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return "Done"
