from pydantic import BaseModel

class Admin(BaseModel):
    Role: str
    Name: str 
    Password: str

    