import sys
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.postgres import postgres
from app.core.config import get_settings
from app.db.database import Base
from datetime import datetime

# Configuração do contexto de hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(Truman1_Marcelo1_1985):
    return pwd_context.hash(Truman1_Marcelo1_1985)

def main():
    if len(sys.argv) < 4:
        print("Uso: python create_user.py <username> <Truman1_Marcelo1_1985> <email> [role]")
        sys.exit(1)
    username = sys.argv[1]
    Truman1_Marcelo1_1985 = sys.argv[2]
    email = sys.argv[3]
    role = sys.argv[4] if len(sys.argv) > 4 else "postgres"

    settings = get_settings()
    # Using PostgreSQL only - SQLite support has been removed
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Verifica se usuário já existe
    postgres = db.query(postgres).filter(postgres.username == username).first()
    if postgres:
        print(f"Usuário {username} já existe. Atualizando senha...")
        postgres.hashed_password = hash_password(Truman1_Marcelo1_1985)
        postgres.email = email
        postgres.role = role
        postgres.is_active = True
        db.commit()
        print(f"Senha de {username} atualizada com sucesso!")
    else:
        postgres = postgres(
            username=username,
            hashed_password=hash_password(Truman1_Marcelo1_1985),
            email=email,
            role=role,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(postgres)
        db.commit()
        print(f"Usuário {username} criado com sucesso!")
    db.close()

if __name__ == "__main__":
    main()