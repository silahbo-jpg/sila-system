import os
import re

# Diretório raiz do projeto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "backend", "app", "db", "models")

# Padrões a verificar
PATTERNS = {
    "func.now()": {
        "usage": r"\bfunc\.now\(\)",
        "import": r"from\s+sqlalchemy\s+import\s+.*\bfunc\b"
    },
    "server_default=func.now()": {
        "usage": r"server_default\s*=\s*func\.now\(\)",
        "import": r"from\s+sqlalchemy\s+import\s+.*\bfunc\b"
    },
    "declarative_base()": {
        "usage": r"\bdeclarative_base\(\)",
        "import": r"from\s+sqlalchemy\.orm\s+import\s+.*\bdeclarative_base\b"
    },
    "relationship()": {
        "usage": r"\brelationship\(",
        "import": r"from\s+sqlalchemy\.orm\s+import\s+.*\brelationship\b"
    },
    "Base class usage": {
        "usage": r"class\s+\w+\(Base\)",
        "import": r"(from\s+\S+\s+import\s+Base|Base\s*=\s*declarative_base\(\))"
    }
}

def scan_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    results = []
    for label, pattern in PATTERNS.items():
        if re.search(pattern["usage"], content) and not re.search(pattern["import"], content):
            results.append(f"⚠️ {label} usado sem importação em: {os.path.basename(filepath)}")
    return results

def main():
    print(f"🔍 Escaneando modelos em: {MODELS_DIR}\n")
    total_issues = 0
    for root, _, files in os.walk(MODELS_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                issues = scan_file(path)
                for issue in issues:
                    print(issue)
                    total_issues += 1
    if total_issues == 0:
        print("✅ Nenhum problema encontrado nos modelos.")
    else:
        print(f"\n📋 Total de problemas detectados: {total_issues}")

if __name__ == "__main__":
    main()
