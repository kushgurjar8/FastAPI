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
