from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from schemas import UserCreate, UserOut, Token,UserLogin
from authentication import verify_password, get_password_hash, create_access_token
from database import SessionLocal, get_db
from datetime import timedelta
from jose import JWTError, jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User registration endpoint
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    
    # Create and save new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        company=user.company,
        geography_of_hq=user.geography_of_hq,
        company_size=user.company_size,
        company_address=user.company_address,
        company_number=user.company_number,
        terms_and_conditions_accepted=user.terms_and_conditions_accepted,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username, "email": new_user.email}

# JWT Token endpoint (login)
@app.post("/token", response_model=Token)
def login_for_access_token(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_login.username).first()
    
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


