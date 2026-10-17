from fastapi import FastAPI, Depends
from models import *
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import database_models
import secrets
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import FastAPI, Depends, HTTPException
import bcrypt

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


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

@app.get("/student/",tags=["Students"])
def get_students(db: Session = Depends(get_db)):
    return db.query(database_models.Student).all()

# read one

@app.get("/student_id/{id}",tags=["Students"])
def get_student(id: int, db: Session = Depends(get_db)):
    s = db.get(database_models.Student, id)
    if s:
        return s
    return "Student not found"

# create a student

# @app.post("/student_create/",tags=["Students"])
# def add_student(new_student: student, db: Session = Depends(get_db)):
#     if db.get(database_models.Student, new_student.id):
#         return "Student already exists"
#     db.add(database_models.Student(**new_student.model_dump()))
#     db.commit()
#     return new_student

# one more method to create if we dont want to use **new_student.modeldump()

# @app.post("/student_create/",tags=["Students"])
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

# -------------------create with password hashing--------------

@app.post("/student_create/",tags=["Students"])
def add_student(new_student: student, db: Session = Depends(get_db)):
    if db.get(database_models.Student, new_student.id):
        return "Student already exists"

    email_taken = db.query(database_models.Student).filter(
        database_models.Student.email == new_student.email
    ).first()
    if email_taken:
        return "Email already registered"

    data = new_student.model_dump()
    data["password"] = hash_password(new_student.password)     # ← replace with hash
    db.add(database_models.Student(**data))
    db.commit()
    return "Student created"


# update a student

# @app.put("/student_update/{id}",tags=["Students"])
# def update_student(id: int, updated_student: student, db: Session = Depends(get_db)):
#     s = db.get(database_models.Student, id)
#     if s:
#         s.name = updated_student.name
#         s.password = updated_student.password     
#         db.commit()
#         db.refresh(s)                             
#         return s                                  
#     return "Student not found"

# -------------------update with password hashing--------------

@app.put("/student_update/{id}",tags=["Students"])
def update_student(id: int, updated_student: student, db: Session = Depends(get_db)):
    s = db.get(database_models.Student, id)
    if s:
        s.name = updated_student.name
        s.email = updated_student.email
        s.password = hash_password(updated_student.password)   # ← hash
        db.commit()
        return "Student updated"
    return "Student not found"

# delete
@app.delete("/student_delete/{id}",tags=["Students"])
def delete_student(id: int, db: Session = Depends(get_db)):
    s = db.get(database_models.Student, id)
    if s:
        db.delete(s)
        db.commit()
        return "Student deleted"
    return "Student not found"






# --------------------------------------login using JWT---------------------------------------------------------------------------

# SECURITY_KEY = secrets.token_hex(32)
SECURITY_KEY = "6f0c09a23978b0b2a0338769fb0953a888ff25708160331dc8c0fa4b8c796469"
ALGORITHM = "HS256"


# login JWT

# @app.post("/login", tags=["Login"])
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

@app.post("/login", tags=["Students Login"])
def login(data: Login, db: Session = Depends(get_db)):
    student = db.query(database_models.Student).filter(
        database_models.Student.email == data.email  
    ).first()

    # -------------------without password hashing-----------------

    # if student is None or student.password != data.password:
    #     raise HTTPException(status_code=404, detail="Invalid email or password")

    # ----------------------with password hashing--------------------

    if student is None or not verify_password(data.password, student.password):
        raise HTTPException(status_code=404, detail="Invalid email or password")

    payload = {
        "id": student.id,
        "name": student.name,
        "email": student.email,                             
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(payload, SECURITY_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "access_token": token}


# --------------------------------------Password Hashing---------------------------------------------

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:     
        return False



# ---------------------------------Role Based Access Control (Employees)---------------------------------

bearer = HTTPBearer()     # reads the token from the "Authorization: Bearer <token>" header


# check the token and the role (only admin and manager pass)
def admin_or_manager(creds = Depends(bearer)):
    try:
        payload = jwt.decode(creds.credentials, SECURITY_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Only admin and manager are allowed")

    return payload


# login (open to everyone)

@app.post("/emp_login",tags=["Employees Login"])
def emp_login(data: EmpLogin, db: Session = Depends(get_db)):
    emp = db.query(database_models.Employee).filter(database_models.Employee.email == data.email).first()
    if emp is None or not verify_password(data.password, emp.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    payload = {
        "id": emp.id,
        "role": emp.role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    token = jwt.encode(payload, SECURITY_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "role": emp.role, "access_token": token}


# ---------------------------------CRUD (only admin and manager)---------------------------------

# create

@app.post("/emp_create/", tags=["Employees"])
def emp_create(new_emp: employee, db: Session = Depends(get_db), user = Depends(admin_or_manager)):
    if db.get(database_models.Employee, new_emp.id):
        return "Employee already exists"
    data = new_emp.model_dump()
    data["password"] = hash_password(new_emp.password)
    db.add(database_models.Employee(**data))
    db.commit()
    return "Employee created"


# read all

@app.get("/emp_all/", tags=["Employees"])
def emp_all(db: Session = Depends(get_db), user = Depends(admin_or_manager)):
    return db.query(database_models.Employee).all()


# read one

@app.get("/emp_id/{id}", tags=["Employees"])
def emp_get(id: int, db: Session = Depends(get_db), user = Depends(admin_or_manager)):
    e = db.get(database_models.Employee, id)
    if e:
        return e
    return "Employee not found"


# update

@app.put("/emp_update/{id}", tags=["Employees"])
def emp_update(id: int, updated: employee, db: Session = Depends(get_db), user = Depends(admin_or_manager)):
    e = db.get(database_models.Employee, id)
    if e:
        e.name = updated.name
        e.email = updated.email
        e.password = hash_password(updated.password)
        e.phone = updated.phone
        e.role = updated.role
        e.branch = updated.branch
        db.commit()
        return "Employee updated"
    return "Employee not found"


# delete

@app.delete("/emp_delete/{id}", tags=["Employees"])
def emp_delete(id: int, db: Session = Depends(get_db), user = Depends(admin_or_manager)):
    e = db.get(database_models.Employee, id)
    if e:
        db.delete(e)
        db.commit()
        return "Employee deleted"
    return "Employee not found"
 