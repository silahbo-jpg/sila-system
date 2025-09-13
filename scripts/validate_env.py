import os
import re
from dotenv import load_dotenv

REQUIRED_KEYS = [
    "ENVIRONMENT", "DEBUG", "LOG_LEVEL",
    "DATABASE_URL", "TEST_DATABASE_URL",
    "SECRET_KEY", "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES", "REFRESH_TOKEN_EXPIRE_DAYS",
    "PROJECT_NAME", "SILA_SYSTEM_ID"
]

def validate_url(url):
    return re.match(r"^postgresql:\/\/.+:.+@.+:\d+\/.+\?schema=.+$", url)

def validate_env():
    load_dotenv()

    missing = []
    invalid = []

    for key in REQUIRED_KEYS:
        value = os.getenv(key)
        if value is None:
            missing.append(key)
        elif key.endswith("URL") and not validate_url(value):
            invalid.append(f"{key} → formato inválido")
        elif key == "DEBUG" and value not in ["True", "False"]:
            invalid.append(f"{key} → deve ser 'True' ou 'False'")
        elif key == "ACCESS_TOKEN_EXPIRE_MINUTES" and not value.isdigit():
            invalid.append(f"{key} → deve ser número inteiro")
        elif key == "REFRESH_TOKEN_EXPIRE_DAYS" and not value.isdigit():
            invalid.append(f"{key} → deve ser número inteiro")

    if missing:
        print("❌ Variáveis ausentes:")
        for k in missing:
            print(f"  - {k}")

    if invalid:
        print("\n⚠️ Variáveis com formato inválido:")
        for k in invalid:
            print(f"  - {k}")

    if not missing and not invalid:
        print("✅ .env validado com sucesso.")

if __name__ == "__main__":
    validate_env()
