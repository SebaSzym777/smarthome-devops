from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext


# Sekretny klucz do podpisu tokenów
# W praktyce powinieneś przechowywać go bezpiecznie, np. w zmiennych środowiskowych
SECRET_KEY = "supersekretnyklucz12345"  

# Algorytm szyfrowania JWT
ALGORITHM = "HS256"

# Czas ważności tokenu w minutach
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funkcja do tworzenia tokenu
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()  # kopiujemy dane, które chcemy umieścić w tokenie
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # dodajemy czas wygaśnięcia tokenu
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # generujemy token
    return encoded_jwt

# Funkcja do weryfikacji tokenu
def verify_token(token: str) -> Optional[dict]:
    try:
        # Dekodujemy token i sprawdzamy podpis
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Jeśli token jest nieprawidłowy lub wygasł, zwracamy None
        return None

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)