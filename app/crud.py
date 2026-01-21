from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_todos(db: Session):
    return db.query(models.TodoModel).all()

def get_todo(db: Session, todo_id: int):
    return db.query(models.TodoModel).filter(models.TodoModel.id == todo_id).first()

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.TodoModel(**todo.model_dump(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.TodoCreate):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db_todo.title = todo.title
        db_todo.description = todo.description
        db_todo.completed = todo.completed
        db.commit()
        db.reflesh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # パスワードをハッシュ化して保存
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.UserModel(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user