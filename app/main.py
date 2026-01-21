from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database, auth

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
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db), current_user: models.UserModel = Depends(auth.get_current_user)):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)

# 更新
@app.put("/todos/{todo_id}", response_model=schemas.TodoSchema)
def update_todo(todo_id: int, updated_todo: schemas.TodoCreate, db: Session = Depends(database.get_db)):
    db_todo = crud.update_todo(db, todo_id, updated_todo)
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
    
# -- ユーザ登録 --
@app.post("/signup", response_model=schemas.UserSchema)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# -- ログイン（トークン発行） --
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}