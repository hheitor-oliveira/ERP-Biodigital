from pydantic import BaseModel

# POST SCHEMA
class CreateUserSchema(BaseModel):
    
    name: str
    email: str
    password: str

# GET SCHEMA