from sqlalchemy import Column, Integer, String, Boolean
from database import Base
from sqlalchemy import Enum


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)  # First name
    last_name = Column(String)   # Last name
    phone_number = Column(String)  # Phone number (international code + free number text)
    company = Column(String)  # Company (free text)
    geography_of_hq = Column(String)  # Geography of HQ
    company_size = Column(String)  # Company size (drop down menu)
    company_address = Column(String)  # Company address
    company_number = Column(String)  # Company number
    terms_and_conditions_accepted = Column(Boolean, default=False)  # T&Cs acceptance tick box
    is_active = Column(Boolean, default=True) 
