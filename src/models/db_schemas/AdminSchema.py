from pydantic import BaseModel

class Admin(BaseModel):
    Name: str 
    Password: str