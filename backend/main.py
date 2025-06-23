from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import select, text
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import AsyncGenerator, Optional
import os

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from auth import create_access_token, verify_token, hash_password, verify_password  # importujemy funkcje z auth.py
from models import Base, Device, User  # Twój model ORM

app = FastAPI()

origins = [
    "http://localhost:5173",  # adres frontendu
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfiguracja bazy danych z env
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "smarthome")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Funkcja do tworzenia sesji dla requestu (dependency)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Modele Pydantic

class DeviceCreate(BaseModel):
    name: str
    location: str

class LoginData(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

# OAuth2PasswordBearer - ścieżka do endpointu logowania
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Funkcja do pobrania aktualnego użytkownika z tokena JWT
async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nieautoryzowany")
    return payload.get("sub")

# Tworzymy tabele przy starcie, jeśli nie istnieją
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Testowy endpoint sprawdzający połączenie z bazą
@app.get("/status")
async def read_status():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "Połączenie z bazą działa!"}
    except Exception as e:
        return {"status": "Błąd połączenia z bazą", "error": str(e)}

@app.post("/login")
async def login(data: LoginData, session: AsyncSession = Depends(get_session)):
    # Pobierz użytkownika z bazy po username
    result = await session.execute(select(User).where(User.username == data.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Niepoprawne dane logowania")

    # Sprawdź hasło (porównanie plaintext z hashem)
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Niepoprawne dane logowania")

    # Generuj token JWT z username w polu 'sub'
    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Sprawdź, czy użytkownik już istnieje
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Użytkownik już istnieje")

    # Hashuj hasło
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw)
    session.add(new_user)
    await session.commit()

    return {"message": "Użytkownik zarejestrowany"}

# Endpoint dodawania urządzenia - zabezpieczony JWT
@app.post("/devices")
async def add_device(
    device: DeviceCreate,
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_device = Device(name=device.name, location=device.location)
    session.add(new_device)
    await session.commit()
    return {"message": f"Urządzenie dodane przez {current_user}", "id": new_device.id}

# Endpoint listowania urządzeń - zabezpieczony JWT
@app.get("/devices")
async def list_devices(
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Device))
    devices = result.scalars().all()
    return [{"id": d.id, "name": d.name, "location": d.location} for d in devices]
