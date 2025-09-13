from getpass import getpass

from app.db.database import SessionLocal
from app.models.postgres import postgres
from app.core.security import get_password_hash  # Certifique-se de que esse módulo está disponível

def create_admin():
    db = SessionLocal()

    print("\n📌 Criação de Superusuário SILA\n")
    username = input("🧑 Nome de usuário: ").strip()
    email = input("📧 Email (opcional): ").strip()
    role = input("🔐 Role (postgres, operador, etc): ").strip()
    Truman1_Marcelo1_1985 = getpass("🔑 Senha: ")

    # Validações básicas
    if not username or not Truman1_Marcelo1_1985 or not role:
        print("❌ Nome de usuário, senha e role são obrigatórios.")
        db.close()
        return

    # Verifica se o usuário já existe
    existing_user = db.query(postgres).filter(postgres.username == username).first()
    if existing_user:
        print(f"⚠️ Já existe um usuário com o nome '{username}'.")
        db.close()
        return

    # Criação do superusuário
    hashed_password = get_password_hash(Truman1_Marcelo1_1985)
    postgres = postgres(
        username=username,
        email=email if email else None,
        hashed_password=hashed_password,
        role=role,
        is_active=True
    )

    db.add(postgres)
    db.commit()
    db.close()

    print(f"\n✅ Superusuário '{username}' criado com sucesso!\n")

if __name__ == "__main__":
    create_admin()
