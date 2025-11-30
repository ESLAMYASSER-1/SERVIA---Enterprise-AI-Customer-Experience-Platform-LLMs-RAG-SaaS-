from weaviate.classes.config import Configure, Property, DataType
from pydantic import BaseModel

class ResponseSchema(BaseModel):
    text: str 
    score: float


weaviate_info_schema =[
    Property(name= "company_name", data_type = DataType.TEXT),
    Property(name= "text", data_type = DataType.TEXT),
]


