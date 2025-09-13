import os
import csv
import psycopg2
from datetime import datetime
from dotenv import dotenv_values

# Diretório raiz do projeto
RAIZ = os.getcwd()

# Lista de resultados
RESULTADOS = []

# Nome do arquivo CSV com timestamp
CSV_SAIDA = f'env_conexao_status_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def testar_conexao(database_url):
    try:
        # Remove ?schema=... se presente (psycopg2 não aceita esse parâmetro)
        if '?schema=' in database_url:
            database_url = database_url.split('?')[0]

        conn = psycopg2.connect(database_url)
        conn.close()
        return '✅ sucesso', ''
    except Exception as e:
        return '❌ falha', str(e).replace('\n', ' ')

def extrair_database_url(env_path):
    config = dotenv_values(env_path)
    return config.get('DATABASE_URL')

def buscar_envs(raiz):
    for dirpath, _, filenames in os.walk(raiz):
        for nome in filenames:
            if nome.startswith('.env'):
                caminho_completo = os.path.join(dirpath, nome)
                db_url = extrair_database_url(caminho_completo)
                if db_url:
                    status, erro = testar_conexao(db_url)
                    RESULTADOS.append([caminho_completo, status, erro])
                else:
                    RESULTADOS.append([caminho_completo, '⚠️ sem DATABASE_URL', ''])

def salvar_csv():
    with open(CSV_SAIDA, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Arquivo .env', 'Status de conexão', 'Mensagem de erro'])
        writer.writerows(RESULTADOS)

if __name__ == '__main__':
    buscar_envs(RAIZ)
    salvar_csv()
    print(f"Validação concluída - relatório salvo em '{CSV_SAIDA}'")
