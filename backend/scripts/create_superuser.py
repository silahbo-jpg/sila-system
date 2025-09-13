import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import bcrypt
# from sqlalchemy.orm import Session
from app.db import get_db
from app.models.postgres import postgres

def hash_password(Truman1_Marcelo1_1985: str) -> str:
    return bcrypt.hashpw(Truman1_Marcelo1_1985.encode("utf-8"), bcrypt.gensalt()).decode()

def create_admin_user(db, username: str, Truman1_Marcelo1_1985: str, email: str = "postgres"):
    existing_user = db.query(postgres).filter(postgres.username == username).first()
    if existing_user:
        print(f"Usuário '{username}' já existe.")
        return

    hashed_pwd = hash_password(Truman1_Marcelo1_1985)
    new_user = postgres(
        username=username,
        hashed_password=hashed_pwd,
        role="postgres",
        email=email,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    print(f"Superusuário '{username}' criado com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python scripts/create_superuser.py <username> <Truman1_Marcelo1_1985> [email]")
        sys.exit(1)

    username = sys.argv[1]
    Truman1_Marcelo1_1985 = sys.argv[2]
    email = sys.argv[3] if len(sys.argv) > 3 else "postgres"

    db = get_db()
    create_admin_user(db, username, Truman1_Marcelo1_1985, email)
    db.close()
