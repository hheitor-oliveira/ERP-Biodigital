from pydantic import BaseModel

# POST SCHEMA
class CreateUserSchema(BaseModel):
    
    user_name: str
    user_email: str
    user_password: str
    admin: bool = False
    
class LoginUserSchema(BaseModel):
    
    user_email: str
    user_password: str 
    
    class Config:
        from_attributes = True