from fastapi import FastAPI, Depends
from models import *
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import database_models
import secrets
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import FastAPI, Depends, HTTPException


app = FastAPI()

Base.metadata.create_all(bind=engine)     # creates the table if it doesn't exist

# Opens a DB session for each request and closes it afterwards

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get('/')
# def get_data():
#     return " Welcome to FastAPI"

# students = [
#     student(id= 1, name= 'kush'),
#     student(id= 2, name= 'kiran'),
#     student(id= 3, name= 'gaurav'),
#     ]

# @app.get("/student/")
# def get_students():
#     return students

# get student by id(crud without db) :

# @app.get("/student_id/{id}")
# def get_student(id: int):
#     for s in students:
#         if s.id == id:
#             return s
#     return "Student not found"

# create a student(crud without db):

# @app.post("/student_create/")
# def add_student(new_student: student):
#     for s in students:
#         if s.id == new_student.id:
#             return "Student already exists"
#     students.append(new_student)
#     return new_student


# update a student(crud without db) :

# @app.put("/student_update/{id}")
# def update_student(id: int, updated_student: student):
#     for i in range(len(students)):
#         if students[i].id == id:
#             students[i] = updated_student
#             return updated_student
#     return "Student not found"

# delete a student(crud without db) : 

# @app.delete("/student_delete/{id}")
# def delete_student(id: int):
#     for i in range(len(students)):
#         if students[i].id == id:
#             del students[i]
#             return "Student deleted"
#     return "Student not found"

# _____________________________crud with database______________________________________________________________

@app.get("/")
def get_data():
    return "Welcome to FastAPI"


# read all students
@app.get("/student/")
def get_students(db: Session = Depends(get_db)):
    return db.query(database_models.Student).all()

# read one
@app.get("/student_id/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    s = db.get(database_models.Student, id)
    if s:
        return s
    return "Student not found"

# create a student
@app.post("/student_create/")
def add_student(new_student: student, db: Session = Depends(get_db)):
    if db.get(database_models.Student, new_student.id):
        return "Student already exists"
    db.add(database_models.Student(**new_student.model_dump()))
    db.commit()
    return new_student

# one more method to create if we dont want to use **new_student.modeldump()

# @app.post("/student_create/")
# def add_student(new_student: student, db: Session = Depends(get_db)):
#     if db.get(database_models.Student, new_student.id):
#         return "Student already exists"

#     db_student = database_models.Student(
#         id=new_student.id,
#         name=new_student.name
#     )
#     db.add(db_student)
#     db.commit()
#     return new_student


# update a student
@app.put("/student_update/{id}")
def update_student(id: int, updated_student: student, db: Session = Depends(get_db)):
    s = db.get(database_models.Student, id)
    if s:
        s.name = updated_student.name
        s.password = updated_student.password     
        db.commit()
        db.refresh(s)                             
        return s                                  
    return "Student not found"

# delete
@app.delete("/student_delete/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    s = db.get(database_models.Student, id)
    if s:
        db.delete(s)
        db.commit()
        return "Student deleted"
    return "Student not found"



# --------------------------------------login using JWT---------------------------------------------------------------------------

SECURITY_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"


# login JWT

# @app.post("/login")
# def login(data: Login, db: Session = Depends(get_db)):
#     student = db.query(database_models.Student).filter(
#         database_models.Student.name == data.username
#     ).first()

#     if student is None or student.password != data.password:
#         raise HTTPException(status_code=404, detail="Invalid username or password")

#     payload = {
#         "id": student.id,
#         "name": student.name,
#         "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
#     }

#     token = jwt.encode(payload, SECURITY_KEY, algorithm=ALGORITHM)

#     return {"message": "Login successful", "access_token": token}

# ---------------------------------------------login by email verification-------------------------------------

@app.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    student = db.query(database_models.Student).filter(
        database_models.Student.email == data.email  
    ).first()

    if student is None or student.password != data.password:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    payload = {
        "id": student.id,
        "name": student.name,
        "email": student.email,                             
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(payload, SECURITY_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "access_token": token}