import os
import csv
from datetime import datetime
from dotenv import dotenv_values

RAIZ = os.getcwd()
VARIAVEIS_PADRAO = {
    'TEST_DATABASE_URL': 'postgres://usuario:senha@localhost:5432/test_db',
    'READONLY_DATABASE_URL': 'postgres://usuario:senha@localhost:5432/readonly_db'
}
LOG_ALTERACOES = []
CSV_LOG = f'env_padronizacao_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def padronizar_env(env_path):
    config = dotenv_values(env_path)
    alterado = False
    novas_linhas = []

    # Carrega conteúdo original
    with open(env_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    # Mapeia variáveis já presentes
    presentes = {linha.split('=')[0].strip() for linha in linhas if '=' in linha}

    # Insere variáveis ausentes
    for var, valor_padrao in VARIAVEIS_PADRAO.items():
        if var not in presentes:
            novas_linhas.append(f'{var}={valor_padrao}\n')
            LOG_ALTERACOES.append([env_path, var, '✅ inserido', valor_padrao])
            alterado = True
        else:
            LOG_ALTERACOES.append([env_path, var, '⏸️ já presente', ''])

    # Se houve alteração, salva novo conteúdo
    if alterado:
        with open(env_path, 'a', encoding='utf-8') as f:
            f.writelines(novas_linhas)

def buscar_envs(raiz):
    for dirpath, _, filenames in os.walk(raiz):
        for nome in filenames:
            if nome.startswith('.env'):
                caminho_completo = os.path.join(dirpath, nome)
                padronizar_env(caminho_completo)

def salvar_log():
    with open(CSV_LOG, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Arquivo .env', 'Variável', 'Status', 'Valor inserido'])
        writer.writerows(LOG_ALTERACOES)

if __name__ == '__main__':
    buscar_envs(RAIZ)
    salvar_log()
    print(f"Padronização concluída - log salvo em '{CSV_LOG}'")
