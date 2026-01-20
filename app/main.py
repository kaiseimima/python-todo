from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database

# テーブルの作成
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 一覧取得
@app.get("/todos", response_model=List[schemas.TodoSchema])
def read_todos(db: Session = Depends(database.get_db)):
    return crud.get_todos(db)

# 個別取得
@app.get("/todos/{todo_id}", response_model=schemas.TodoSchema)
def read_todo(todo_id: int, db: Session = Depends(database.get_db)):
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# 作成
@app.post("/todos", response_model=schemas.TodoSchema)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db)):
    return crud.create_todo(db, todo)

# 更新
@app.put("/todos/{todo_id}", response_model=schemas.TodoSchema)
def update_todo(todo_id: int, updated_todo: schemas.TodoCreate, db: Session = Depends(database.get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# 削除
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    success = crud.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Successfully deleted"}
    
