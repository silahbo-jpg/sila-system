import os
import sys
import re
from datetime import datetime

# ✅ Credenciais únicas e válidas
USUARIO_VALIDO = 'postgres'
SENHA_VALIDO = 'Truman1_Marcelo1_1985'
DB_VALIDO = 'sila_db'
HOST_VALIDO = 'localhost'
PORT_VALIDO = '5432'
SCHEMA_VALIDO = 'public'

# 🔍 Diretório raiz do projeto
RAIZ = os.getcwd()
LOG = []
DRY_RUN = '--dry-run' in sys.argv

# 🔧 Variáveis alvo e seus valores corretos
VARIAVEIS_PADRAO = {
    'POSTGRES_USER': USUARIO_VALIDO,
    'POSTGRES_PASSWORD': SENHA_VALIDO,
    'DATABASE_URL': f'postgresql://{USUARIO_VALIDO}:{SENHA_VALIDO}@{HOST_VALIDO}:{PORT_VALIDO}/{DB_VALIDO}?schema={SCHEMA_VALIDO}',
    'TEST_DATABASE_URL': f'postgresql://{USUARIO_VALIDO}:{SENHA_VALIDO}@{HOST_VALIDO}:{PORT_VALIDO}/sila_test?schema={SCHEMA_VALIDO}'
}

# 🔐 Regex para detectar URLs PostgreSQL malformadas
URL_REGEX = re.compile(r'postgresql://([^:]+):([^@]+)@([^:/]+):(\d+)/([^?]+)\?schema=([^\s]+)')

def normalizar_linha(linha):
    chave_valor = linha.strip().split('=', 1)
    if len(chave_valor) != 2:
        return linha, False

    chave, valor = chave_valor
    valor = valor.strip().strip('"').strip("'")

    if chave in VARIAVEIS_PADRAO:
        valor_correto = VARIAVEIS_PADRAO[chave]
        if valor != valor_correto:
            nova_linha = f'{chave}="{valor_correto}"\n'
            return nova_linha, True

    # 🔄 Correção de URLs PostgreSQL malformadas
    if chave in ['DATABASE_URL', 'TEST_DATABASE_URL']:
        match = URL_REGEX.match(valor)
        if match:
            usuario, senha, host, port, dbname, schema = match.groups()
            if usuario != USUARIO_VALIDO or senha != SENHA_VALIDO:
                nova_linha = f'{chave}="{VARIAVEIS_PADRAO[chave]}"\n'
                return nova_linha, True

    return linha, False

def processar_env(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        novas_linhas = []
        alterado = False

        for linha in linhas:
            nova_linha, foi_modificado = normalizar_linha(linha)
            novas_linhas.append(nova_linha)
            if foi_modificado:
                alterado = True
                LOG.append(f"[{datetime.now()}] {'' if DRY_RUN else '✅'} {caminho_arquivo}: {linha.strip()} → {nova_linha.strip()}")

        if alterado and not DRY_RUN:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.writelines(novas_linhas)

        if not alterado:
            LOG.append(f"[{datetime.now()}] ⚠️ {caminho_arquivo}: nenhuma variável incompatível encontrada")

    except Exception as e:
        LOG.append(f"[{datetime.now()}] ❌ Erro em {caminho_arquivo}: {e}")

def buscar_envs(raiz):
    for dirpath, _, filenames in os.walk(raiz):
        for nome in filenames:
            if nome.startswith('.env'):
                caminho_completo = os.path.join(dirpath, nome)
                processar_env(caminho_completo)

if __name__ == '__main__':
    buscar_envs(RAIZ)

    log_file = f'env_uniformizacao_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG))

    status = 'Simulação concluída' if DRY_RUN else 'Processo concluído'
    print(f"{status} - log salvo em '{log_file}'")
