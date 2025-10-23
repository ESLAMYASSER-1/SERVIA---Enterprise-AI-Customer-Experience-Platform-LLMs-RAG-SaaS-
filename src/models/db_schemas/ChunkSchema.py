from pydantic import BaseModel, Field
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

class Chunk(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    company_name: str = Field(..., description="Company name reference")
    company_id: str = Field(..., description="Company ID")
    chunk_id: int = Field(..., description="chunk ID")
    text: str = Field(..., description="Actual chunk content")

    class Config:
        json_encoders = {ObjectId: str}
        validate_by_name = True

    