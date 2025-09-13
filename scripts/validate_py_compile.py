#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para validar todos os arquivos Python do projeto usando py_compile
e gerar um log detalhado de sucesso ou erro, além de um relatório de validação.
"""

import os
import sys
import py_compile
import logging
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração de logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_dir, f"py_compile_validation_{timestamp}.log")

# Arquivo de relatório
report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
os.makedirs(report_dir, exist_ok=True)
report_file = os.path.join(report_dir, f"validation_report_{timestamp}.txt")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def validate_file(file_path):
    """
    Valida um arquivo Python usando py_compile.
    
    Args:
        file_path: Caminho do arquivo a ser validado
        
    Returns:
        tuple: (file_path, success, error_message)
    """
    try:
        py_compile.compile(file_path, doraise=True)
        return file_path, True, None
    except Exception as e:
        return file_path, False, str(e)


def find_python_files(sila_dev-system_dir, ignore_dirs=None):
    """
    Encontra todos os arquivos Python em um diretório recursivamente,
    ignorando diretórios específicos.
    
    Args:
        sila_dev-system_dir: Diretório raiz para iniciar a busca
        ignore_dirs: Lista de diretórios a serem ignorados
        
    Returns:
        list: Lista de caminhos de arquivos Python
    """
    if ignore_dirs is None:
        ignore_dirs = ['archived', 'venv', '.venv', 'env', '.env', '__pycache__', 'node_modules', '.git']
    
    python_files = []
    
    for sila_dev-system, dirs, files in os.walk(sila_dev-system_dir):
        # Remove diretórios a serem ignorados
        for ignore_dir in ignore_dirs:
            if ignore_dir in dirs:
                dirs.remove(ignore_dir)
        
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(sila_dev-system, file))
                
    return python_files


def parse_args():
    """
    Processa argumentos de linha de comando.
    
    Returns:
        argparse.Namespace: Argumentos processados
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Validador de sintaxe Python usando py_compile")
    parser.add_argument(
        "paths", nargs="*", default=[],
        help="Caminhos específicos para validar (arquivos ou diretórios)"
    )
    parser.add_argument(
        "--ignore-dirs", nargs="+", default=None,
        help="Diretórios a serem ignorados durante a validação"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Exibe informações detalhadas durante a validação"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Exibe apenas erros e resumo final"
    )
    
    return parser.parse_args()


def generate_validation_report(total_files, valid_count, invalid_count, invalid_files, execution_time, report_file):
    """
    Gera um relatório de validação em formato .txt
    
    Args:
        total_files: Total de arquivos validados
        valid_count: Número de arquivos válidos
        invalid_count: Número de arquivos com erro
        invalid_files: Lista de tuplas (arquivo, erro) com os arquivos que falharam
        execution_time: Tempo de execução em segundos
        report_file: Caminho do arquivo de relatório
    """
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO DE VALIDAÇÃO DE SINTAXE PYTHON\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Data e hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tempo total de execução: {execution_time:.2f} segundos\n\n")
        
        f.write("RESUMO:\n")
        f.write(f"Total de arquivos validados: {total_files}\n")
        f.write(f"Arquivos com sintaxe válida: {valid_count}\n")
        f.write(f"Arquivos com erro de sintaxe: {invalid_count}\n\n")
        
        if invalid_count > 0:
            f.write("ARQUIVOS COM ERRO:\n")
            for file_path, error in invalid_files:
                f.write(f"- {file_path}\n  Erro: {error}\n")
        else:
            f.write("✅ TODOS OS ARQUIVOS Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ARAM NA VALIDAÇÃO!\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("Relatório gerado automaticamente pelo validate_py_compile.py\n")
    
    logger.info(f"Relatório de validação gerado em: {report_file}")


def main():
    """
    Função principal que valida arquivos Python do projeto.
    """
    start_time = time.time()
    args = parse_args()
    
    # Configura o nível de log com base nos argumentos
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Obtém o diretório raiz do projeto (dois níveis acima do script)
    project_sila_dev-system = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Determina quais arquivos validar
    python_files = []
    
    if args.paths:
        # Valida apenas os caminhos especificados
        for path in args.paths:
            # Converte para caminho absoluto se for relativo
            if not os.path.isabs(path):
                # Tenta resolver o caminho relativo ao diretório atual
                abs_path = os.path.abspath(path)
                if os.path.exists(abs_path):
                    path = abs_path
                else:
                    # Tenta resolver o caminho relativo ao diretório raiz do projeto
                    path = os.path.abspath(os.path.join(project_sila_dev-system, path))
                    
                logger.debug(f"Caminho convertido para: {path}")
            
            if os.path.isfile(path) and path.endswith(".py"):
                python_files.append(path)
            elif os.path.isdir(path):
                python_files.extend(find_python_files(path, args.ignore_dirs))
            else:
                logger.warning(f"Caminho ignorado (não existe ou não é um arquivo Python): {path}")
    else:
        # Valida todos os arquivos do projeto
        logger.info(f"Iniciando validação de arquivos Python em: {project_sila_dev-system}")
        python_files = find_python_files(project_sila_dev-system, args.ignore_dirs)
    
    logger.info(f"Encontrados {len(python_files)} arquivos Python para validar")
    
    if not python_files:
        logger.warning("Nenhum arquivo Python encontrado para validação!")
        return 0
    
    # Contadores para estatísticas
    valid_count = 0
    invalid_count = 0
    invalid_files = []
    
    # Valida os arquivos em paralelo
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_to_file = {executor.submit(validate_file, file): file for file in python_files}
        
        for future in as_completed(future_to_file):
            file_path, success, error_message = future.result()
            rel_path = os.path.relpath(file_path, project_sila_dev-system)
            
            if success:
                logger.info(f"✅ Sintaxe válida: {rel_path}")
                valid_count += 1
            else:
                logger.error(f"❌ Erro de sintaxe em {rel_path}: {error_message}")
                invalid_count += 1
                invalid_files.append((rel_path, error_message))
    
    # Calcula o tempo de execução
    execution_time = time.time() - start_time
    
    # Gera o relatório de validação
    generate_validation_report(
        total_files=valid_count + invalid_count,
        valid_count=valid_count,
        invalid_count=invalid_count,
        invalid_files=invalid_files,
        execution_time=execution_time,
        report_file=report_file
    )
    
    # Resumo final
    logger.info("="*80)
    logger.info(f"RESUMO DA VALIDAÇÃO:")
    logger.info(f"Total de arquivos validados: {valid_count + invalid_count}")
    logger.info(f"Arquivos válidos: {valid_count}")
    logger.info(f"Arquivos com erro: {invalid_count}")
    logger.info(f"Tempo total de execução: {execution_time:.2f} segundos")
    logger.info(f"Relatório gerado em: {report_file}")
    
    if invalid_count > 0:
        logger.info("\nLista de arquivos com erro:")
        for file_path, error in invalid_files:
            logger.info(f"- {file_path}: {error}")
        
        logger.error("\n❌ Validação falhou! Existem arquivos com erros de sintaxe.")
        return 1
    else:
        logger.info("\n✅ Validação concluída com sucesso! Todos os arquivos estão com sintaxe válida.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

