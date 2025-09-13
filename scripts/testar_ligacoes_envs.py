import os
import csv
import psycopg2
from datetime import datetime
from dotenv import dotenv_values

RAIZ = os.getcwd()
VARIAVEIS_CONEXAO = ['DATABASE_URL', 'TEST_DATABASE_URL', 'READONLY_DATABASE_URL']
RESULTADOS = []
CSV_SAIDA = f'env_ligacoes_status_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def testar_conexao(database_url):
    try:
        if '?schema=' in database_url:
            database_url = database_url.split('?')[0]
        conn = psycopg2.connect(database_url)
        conn.close()
        return '✅ sucesso', ''
    except Exception as e:
        return '❌ falha', str(e).replace('\n', ' ')

def validar_env(env_path):
    config = dotenv_values(env_path)
    for var in VARIAVEIS_CONEXAO:
        db_url = config.get(var)
        if db_url:
            status, erro = testar_conexao(db_url)
            RESULTADOS.append([env_path, var, status, erro])
        else:
            RESULTADOS.append([env_path, var, '⚠️ ausente', ''])

def buscar_envs(raiz):
    for dirpath, _, filenames in os.walk(raiz):
        for nome in filenames:
            if nome.startswith('.env'):
                caminho_completo = os.path.join(dirpath, nome)
                validar_env(caminho_completo)

def salvar_csv():
    with open(CSV_SAIDA, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Arquivo .env', 'Variável', 'Status de conexão', 'Mensagem de erro'])
        writer.writerows(RESULTADOS)

if __name__ == '__main__':
    buscar_envs(RAIZ)
    salvar_csv()
    print(f"Testes concluídos - relatório salvo em '{CSV_SAIDA}'")
