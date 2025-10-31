from pydantic import BaseModel, Field
from datetime import datetime
from bson.objectid import ObjectId

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        # tells Pydantic how to validate this custom type
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        schema.update(type="string")
        return schema

class Company(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Name: str = Field(..., description="Company name")
    CreatedAt: datetime = Field(default_factory=datetime.now)
    IsActive: bool = True

    class ConfigDict:
        json_encoders = {ObjectId: str}
        validate_by_name = True