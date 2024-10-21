from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # Assuming password is required
    first_name: str
    last_name: str
    phone_number: str
    company: str
    geography_of_hq: str
    company_size: str  # Can be validated or constrained as necessary
    company_address: str
    company_number: str
    terms_and_conditions_accepted: bool

class UserOut(BaseModel):
    username: str
    email: str
class UserLogin(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
