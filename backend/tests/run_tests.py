#!/usr/bin/env python3
"""
Script para execução automatizada de testes com cobertura.
Funciona em qualquer sistema operacional.
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def run_command(command, cwd=None):
    """Executa um comando no shell e retorna a saída."""
    print(f"\n\033[1m$ {' '.join(command)}\033[0m"
    result = subprocess.run(
        command,
        cwd=cwd or os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"\033[91m{result.stderr}\033[0m")
    
    return result.returncode == 0

def install_dependencies():
    """Instala as dependências necessárias para os testes."""
    print("\n\033[1;34m=== Instalando dependências ===\033[0m")
    # Atualiza o pip primeiro
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"]):
        return False
    
    # Instala as dependências base primeiro
    print("\n\033[1;34m=== Instalando dependências base ===\033[0m")
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements/base.txt"]):
        return False
    
    # Instala as dependências de desenvolvimento
    print("\n\033[1;34m=== Instalando dependências de desenvolvimento ===\033[0m")
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"]):
        return False
        
    return True

def run_tests():
    """Executa os testes com cobertura."""
    print("\n\033[1;34m=== Executando testes com cobertura ===\033[0m")
    success = run_command([
        sys.executable, "-m", "pytest",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "-v"
    ])
    
    if success:
        print("\n\033[1;32m✅ Testes concluídos com sucesso!\033[0m")
    else:
        print("\n\033[1;31m❌ Alguns testes falharam. Verifique os logs acima.\033[0m")
    
    return success

def open_coverage_report():
    """Abre o relatório de cobertura no navegador."""
    report_path = Path("htmlcov") / "index.html"
    if report_path.exists():
        print(f"\n\033[1;34m=== Abrindo relatório de cobertura ===\033[0m")
        webbrowser.open(f"file://{report_path.absolute()}")
    else:
        print("\n\033[93m⚠️ Relatório de cobertura não encontrado.\033[0m")

def check_coverage():
    """Verifica se a cobertura de código atinge o mínimo exigido."""
    print("\n\033[1;34m=== Verificando cobertura de código ===\033[0m")
    return run_command([
        sys.executable, "-m", "coverage", "report",
        "--fail-under=80"
    ])

def main():
    """Função principal."""
    try:
        # Instala dependências
        if not install_dependencies():
            return 1
        
        # Executa os testes
        if not run_tests():
            return 1
        
        # Verifica cobertura
        if not check_coverage():
            print("\n\033[93m⚠️ Cobertura de código abaixo do mínimo exigido (80%).\033[0m")
            return 1
        
        # Abre o relatório de cobertura
        open_coverage_report()
        
        return 0
    except KeyboardInterrupt:
        print("\n\033[93m⚠️ Execução interrompida pelo usuário.\033[0m")
        return 1
    except Exception as e:
        print(f"\n\033[91m❌ Erro inesperado: {e}\033[0m")
        return 1

if __name__ == "__main__":
    sys.exit(main())

