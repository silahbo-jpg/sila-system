#!/usr/bin/env python3
"""
Logger institucional para execução de hooks pre-commit.

Registra:
- ID e tipo do hook
- Arquivos afetados
- Tempo de execução
- Saída e erros do comando
- Log com timestamp em logs/hooks_exec_YYYY-MM-DD_HH-MM-SS.log
"""

import os
import sys
import time
import logging
import subprocess
from datetime import datetime
from typing import Dict, Any

LOG_DIR = 'logs'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def setup_logger(log_file: str) -> logging.Logger:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger('hook_logger')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(console_handler)

    return logger


def get_context() -> Dict[str, Any]:
    return {
        'hook_id': os.environ.get('PRE_COMMIT_HOOK_ID', 'unknown'),
        'hook_type': os.environ.get('PRE_COMMIT_HOOK_TYPE', 'unknown'),
        'repo': os.environ.get('PRE_COMMIT_REPO', 'unknown'),
        'files': [f for f in os.environ.get('PRE_COMMIT_FILES', '').split() if f],
        'args': sys.argv[1:],
        'cwd': os.getcwd(),
        'user': os.environ.get('USER', os.environ.get('USERNAME', 'unknown')),
    }


def main() -> int:
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(LOG_DIR, f'hooks_exec_{timestamp}.log')
    logger = setup_logger(log_file)

    ctx = get_context()
    start = time.time()

    logger.info("Início do hook: %s (%s)", ctx['hook_id'], ctx['hook_type'])
    logger.info("Repositório: %s", ctx['repo'])
    logger.info("Usuário: %s", ctx['user'])
    logger.info("Diretório: %s", ctx['cwd'])
    logger.info("Arquivos afetados: %d", len(ctx['files']))
    for f in ctx['files']:
        logger.info("  • %s", f)

    try:
        if ctx['args']:
            result = subprocess.run(
                ctx['args'],
                capture_output=True,
                text=True,
                check=False
            )
            if result.stdout:
                logger.info("Saída do comando:")
                for line in result.stdout.splitlines():
                    logger.info("  | %s", line)
            if result.stderr:
                logger.error("Erros do comando:")
                for line in result.stderr.splitlines():
                    logger.error("  | %s", line)
            code = result.returncode
        else:
            logger.info("Nenhum comando executado — logger passivo")
            code = 0
    except Exception as e:
        logger.exception("Erro durante execução do hook")
        code = 1

    duration = time.time() - start
    status = "SUCESSO" if code == 0 else f"FALHA (código {code})"
    logger.info("Execução %s em %.2fs", status, duration)
    logger.info("=" * 80)

    return code


if __name__ == "__main__":
    sys.exit(main())
