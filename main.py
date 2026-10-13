from fastapi import FastAPI
from models import *

app = FastAPI()

@app.get('/')
def get_data():
    return " Welcome to FastAPI"

students = [
    student(id= 1, name= 'kush'),
    student(id= 2, name= 'kiran'),
    student(id= 3, name= 'gaurav'),
    ]

@app.get("/student/")
def get_students():
    return students

# get student by id :

@app.get("/student/{id}")
def get_student(id: int):
    for s in students:
        if s.id == id:
            return s
    return "Student not found"

# create a student:

@app.post("/student/")
def add_student(new_student: student):
    for s in students:
        if s.id == new_student.id:
            return "Student already exists"
    students.append(new_student)
    return new_student


# update a student :

@app.put("/student/{id}")
def update_student(id: int, updated_student: student):
    for i in range(len(students)):
        if students[i].id == id:
            students[i] = updated_student
            return updated_student
    return "Student not found"

# delete a student : 

@app.delete("/student/{id}")
def delete_student(id: int):
    for i in range(len(students)):
        if students[i].id == id:
            del students[i]
            return "Student deleted"
    return "Student not found"
