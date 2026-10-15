from pydantic import BaseModel

# ----------------------------model for login with username----------------------
# class student(BaseModel):
#     id: int
#     name: str
#     password: str

# class Login(BaseModel):
#     username: str
#     password: str

# --------------------------------model for login with email-----------------------

class student(BaseModel):
    id: int
    name: str
    email: str    
    password: str

class Login(BaseModel):
    email: str           
    password: str