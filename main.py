from fastapi import FastAPI
from models import *
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import database_models

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



# create a student
@app.post("/student_create/")
def add_student(new_student: student, db: Session = Depends(get_db)):
    exists = db.query(database_models.Student).filter(database_models.Student.id == new_student.id).first()
    if exists:
        return "Student already exists"
    db_student = database_models.Student(**new_student.model_dump())  # Pydantic → table row
    db.add(db_student)
    db.commit()               # save to PostgreSQL
    db.refresh(db_student)    # reload saved values
    return db_student