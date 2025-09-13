#!/usr/bin/env python3
"""
Validação institucional de arquivos CSV para pre-commit.

Valida:
- Encoding UTF-8 (abrindo diretamente em UTF-8; chardet só auxilia)
- Delimitador permitido (vírgula, ponto e vírgula, tab)
- Cabeçalho presente e campos obrigatórios
- Consistência de colunas
- Log com timestamp em logs/csv_validation.log
- Suporte a --dry-run para simulação segura
"""

import csv
import sys
import os
from pathlib import Path
from typing import List, Set, Tuple
import chardet
from datetime import datetime

REQUIRED_ENCODING = "utf-8"
ALLOWED_DELIMITERS = {",", ";", "\t"}
REQUIRED_HEADERS: Set[str] = {"id", "nome", "email"}  # Ajustável conforme padrão institucional
LOG_FILE = "logs/csv_validation.log"


def detect_encoding(file_path: str) -> Tuple[str, float]:
    """Usa chardet apenas como informação auxiliar."""
    with open(file_path, "rb") as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result.get("encoding") or "desconhecido", result.get("confidence", 0.0)


def validate_csv(file_path: str) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if not os.path.exists(file_path):
        return False, [f"Arquivo não encontrado: {file_path}"]

    # 1. Testar UTF-8 real
    try:
        with open(file_path, "r", encoding=REQUIRED_ENCODING) as f:
            content_sample = f.read(2048)  # leitura parcial para validar
            f.seek(0)
    except UnicodeDecodeError as e:
        detected_encoding, confidence = detect_encoding(file_path)
        errors.append(
            f"Encoding inválido: esperado {REQUIRED_ENCODING}, "
            f"detectado {detected_encoding} (confiança: {confidence:.0%})"
        )
        return False, errors

    # 2. Detectar delimitador
    try:
        dialect = csv.Sniffer().sniff(content_sample)
    except csv.Error:
        dialect = csv.excel()
        errors.append("Falha ao detectar delimitador, usando padrão Excel")

    if dialect.delimiter not in ALLOWED_DELIMITERS:
        errors.append(
            f"Delimitador inválido: '{dialect.delimiter}'. "
            f"Permitidos: {', '.join(ALLOWED_DELIMITERS)}"
        )

    # 3. Validar cabeçalho e linhas
    with open(file_path, "r", encoding=REQUIRED_ENCODING, newline="") as f:
        reader = csv.reader(f, dialect)
        try:
            headers = next(reader)
            expected_columns = len(headers)

            missing = REQUIRED_HEADERS - set(headers)
            if missing:
                errors.append(f"Headers ausentes: {', '.join(sorted(missing))}")

            for i, row in enumerate(reader, start=2):
                if len(row) != expected_columns:
                    errors.append(
                        f"Linha {i}: esperado {expected_columns} colunas, "
                        f"encontrado {len(row)}"
                    )
        except StopIteration:
            errors.append("Arquivo CSV vazio")
        except csv.Error as e:
            errors.append(f"Erro ao ler CSV: {str(e)}")

    return len(errors) == 0, errors


def log_result(file_path: str, success: bool, errors: List[str]) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCESSO" if success else "FALHA"
    entry = [f"[{timestamp}] {status} {file_path}"]

    if success:
        entry.append("  - Validação concluída sem erros.")
    else:
        entry.extend([f"  - {e}" for e in errors])

    entry.append("")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(entry) + "\n")


def main() -> int:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    file_paths = [arg for arg in args if not arg.startswith("--")]

    if not file_paths:
        print("Uso: python validate_csv.py <arquivo1.csv> [<arquivo2.csv> ...] [--dry-run]")
        return 1

    all_valid = True
    for path in file_paths:
        valid, errors = validate_csv(path)
        if not valid:
            all_valid = False
            print(f"\nFalha na validação: {path}")
            for e in errors:
                print(f"  • {e}")
        else:
            print(f"\nValidação bem-sucedida ✅ {path}")

        if not dry_run:
            log_result(path, valid, errors)
        else:
            print(f"[DRY-RUN] Log não gerado para {path}")

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
