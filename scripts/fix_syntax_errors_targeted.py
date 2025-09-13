#!/usr/bin/env python
"""
Script para correção automatizada de erros de sintaxe específicos em arquivos Python.

Este script analisa e corrige erros de sintaxe em arquivos específicos do projeto,
focando nas linhas indicadas e aplicando correções conforme as instruções.
"""

import os
import re
import sys
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Diretório base do projeto
BASE_DIR = Path(os.getcwd()).parent if Path(os.getcwd()).name == "scripts" else Path(os.getcwd())

# Dicionário de arquivos com erros e suas respectivas correções
ARQUIVOS_COM_ERROS = {
    str(BASE_DIR / "backend/app/services/nnnotification_service.py"): {
        "linha": 174,
        "erro": "} não casa com (",
        "acao": "Verificar se há f-strings malformadas como f\"Texto {variável\" sem fechar com '}'"
    },
    str(BASE_DIR / "backend/app/services/user_service.py"): {
        "linha": 62,
        "erro": "unexpected indent",
        "acao": "Verificar se há espaços ou tabulação fora de bloco. Corrigir a indentação."
    },
    str(BASE_DIR / "backend/scripts/docs/generate_docs.py"): {
        "linha": 123,
        "erro": "f-string: expecting '}'",
        "acao": "Corrigir f-string incompleta. Certificar-se de que todas as expressões estão fechadas com '}'"
    },
    str(BASE_DIR / "scripts/setup_project_structure.py"): {
        "linha": 58,
        "erro": "\\ seguido de caractere inválido",
        "acao": "Verificar se há quebra de linha malformada. Usar \\n ou r\"string\" se necessário."
    },
    str(BASE_DIR / "backend/tests/conftest.py"): {
        "linha": 34,
        "erro": "expected indented block",
        "acao": "Adicionar indentação após def ou if na linha 31. Pode estar faltando um bloco de código."
    }
}

# Diretórios a serem pesquisados
DIRETORIOS_BUSCA = [
    "backend",
    "scripts",
    "tests"
]

# Função para encontrar o caminho completo de um arquivo
def encontrar_arquivo(caminho_arquivo):
    """Verifica se o arquivo existe no caminho especificado."""
    caminho = Path(caminho_arquivo)
    if caminho.exists():
        # Ignorar arquivos em .venv ou site-packages
        if ".venv" not in str(caminho) and "site-packages" not in str(caminho):
            logger.info(f"Arquivo encontrado: {caminho}")
            return [caminho]
    else:
        logger.warning(f"Arquivo não encontrado: {caminho}")
    
    return []

# Função para ler o conteúdo de um arquivo
def ler_arquivo(caminho):
    """Lê o conteúdo de um arquivo."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo {caminho}: {e}")
        return []

# Função para escrever o conteúdo em um arquivo
def escrever_arquivo(caminho, linhas):
    """Escreve o conteúdo em um arquivo."""
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.writelines(linhas)
        return True
    except Exception as e:
        logger.error(f"Erro ao escrever no arquivo {caminho}: {e}")
        return False

# Função para corrigir f-strings incompletas
def corrigir_fstring_incompleta(linha):
    """Corrige f-strings incompletas, adicionando o caractere } onde necessário."""
    # Padrão para encontrar f-strings com { sem }
    padrao = r'f["\'].*?\{[^\}]*?["\']'
    
    # Se encontrar o padrão, adiciona o } antes da última aspas
    if re.search(padrao, linha):
        ultima_aspas = max(linha.rfind('\''), linha.rfind('"'))
        if ultima_aspas > 0:
            return linha[:ultima_aspas] + "}" + linha[ultima_aspas:]
    
    return linha

# Função para corrigir indentação
def corrigir_indentacao(linhas, num_linha):
    """Corrige problemas de indentação."""
    # Verifica se a linha anterior tem um bloco que precisa de indentação
    if num_linha > 0 and num_linha < len(linhas):
        linha_anterior = linhas[num_linha - 1]
        linha_atual = linhas[num_linha]
        
        # Se a linha anterior termina com : e a atual não está indentada
        if linha_anterior.strip().endswith(":") and not linha_atual.startswith(" ") and not linha_atual.startswith("\t"):
            # Adiciona 4 espaços de indentação
            linhas[num_linha] = "    " + linha_atual
    
    return linhas

# Função para corrigir quebras de linha malformadas
def corrigir_quebra_linha(linha):
    """Corrige quebras de linha malformadas."""
    # Substitui \ seguido de caractere inválido por \n
    # Padrão para encontrar \ seguido de caractere que não seja n, r, t, etc.
    padrao = r'\\([^nrtbfv\'"\\])'
    
    # Substitui por \n
    return re.sub(padrao, r'\\n\1', linha)

# Função principal para corrigir erros
def corrigir_erros():
    """Função principal para corrigir erros nos arquivos."""
    arquivos_corrigidos = 0
    
    for nome_arquivo, info in ARQUIVOS_COM_ERROS.items():
        caminhos = encontrar_arquivo(nome_arquivo)
        
        if not caminhos:
            logger.warning(f"Arquivo {nome_arquivo} não encontrado.")
            continue
        
        for caminho in caminhos:
            logger.info(f"Processando {caminho}...")
            
            # Lê o conteúdo do arquivo
            linhas = ler_arquivo(caminho)
            if not linhas:
                continue
            
            # Obtém o número da linha com erro (ajustando para índice 0-based)
            num_linha = info["linha"] - 1
            if num_linha < 0 or num_linha >= len(linhas):
                logger.warning(f"Linha {info['linha']} fora dos limites do arquivo {caminho}.")
                continue
            
            # Obtém a linha com erro
            linha_original = linhas[num_linha]
            linha_modificada = linha_original
            
            # Aplica a correção adequada com base no tipo de erro
            if "} não casa com (" in info["erro"] or "f-string: expecting '}'" in info["erro"]:
                linha_modificada = corrigir_fstring_incompleta(linha_original)
            elif "unexpected indent" in info["erro"] or "expected indented block" in info["erro"]:
                linhas = corrigir_indentacao(linhas, num_linha)
                linha_modificada = linhas[num_linha]  # Atualiza a linha modificada
            elif "seguido de caractere inválido" in info["erro"]:
                linha_modificada = corrigir_quebra_linha(linha_original)
            
            # Se houve modificação, atualiza a linha no arquivo
            if linha_modificada != linha_original:
                linhas[num_linha] = linha_modificada
                
                # Escreve o conteúdo modificado de volta no arquivo
                if escrever_arquivo(caminho, linhas):
                    logger.info(f"✅ Arquivo {caminho} corrigido com sucesso!")
                    logger.info(f"   Linha {info['linha']}: {linha_original.strip()} -> {linha_modificada.strip()}")
                    arquivos_corrigidos += 1
            else:
                logger.info(f"⚠️ Nenhuma correção necessária para {caminho} na linha {info['linha']}.")
    
    return arquivos_corrigidos

# Função para validar a sintaxe de um arquivo Python
def validar_sintaxe(caminho):
    """Valida a sintaxe de um arquivo Python usando py_compile."""
    import py_compile
    try:
        py_compile.compile(caminho, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        logger.error(f"Erro de sintaxe em {caminho}: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro ao compilar {caminho}: {e}")
        return False

# Função para validar todos os arquivos corrigidos
def validar_arquivos_corrigidos():
    """Valida a sintaxe de todos os arquivos corrigidos."""
    arquivos_validados = 0
    
    for nome_arquivo in ARQUIVOS_COM_ERROS.keys():
        caminhos = encontrar_arquivo(nome_arquivo)
        
        for caminho in caminhos:
            if validar_sintaxe(caminho):
                logger.info(f"✅ Sintaxe válida: {caminho}")
                arquivos_validados += 1
            else:
                logger.error(f"❌ Sintaxe inválida: {caminho}")
    
    return arquivos_validados

# Função principal
def main():
    """Função principal do script."""
    logger.info("Iniciando correção de erros de sintaxe...")
    
    # Corrige os erros
    arquivos_corrigidos = corrigir_erros()
    logger.info(f"Total de arquivos corrigidos: {arquivos_corrigidos}")
    
    # Valida os arquivos corrigidos
    arquivos_validados = validar_arquivos_corrigidos()
    logger.info(f"Total de arquivos validados: {arquivos_validados}")
    
    if arquivos_corrigidos == arquivos_validados:
        logger.info("✅ Todos os arquivos foram corrigidos e validados com sucesso!")
        return 0
    else:
        logger.warning("⚠️ Alguns arquivos não puderam ser corrigidos ou validados.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
