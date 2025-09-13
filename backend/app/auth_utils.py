from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY_PLACEHOLDER = "seusegredoseguroaqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(Truman1_Marcelo1_1985):
    return pwd_context.hash(Truman1_Marcelo1_1985)

def authenticate_user(username: str, Truman1_Marcelo1_1985: str):
    # Trocar por consulta real ao banco
    if username == "postgres" and Truman1_Marcelo1_1985 == "123456":
        return {"username": "postgres"}
    return None

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY_PLACEHOLDER, algorithm=ALGORITHM)

