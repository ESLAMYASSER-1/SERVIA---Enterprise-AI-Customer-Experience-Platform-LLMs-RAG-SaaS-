from weaviate.classes.config import Configure, Property, DataType

weaviate_info_schema =[
    Property(name= "company_name", data_type = DataType.TEXT),
    Property(name= "text", data_type = DataType.TEXT),
]