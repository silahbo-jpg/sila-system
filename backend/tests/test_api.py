# test_api.py
import asyncio
import httpx
import json
from datetime import datetime

# URL base da sua API
BASE_URL = "http://127.0.0.1:8000/api"

async def run_tests():
    print("Iniciando testes de API...")

    # --- 1. Registrar um novo superusuário ---
    print("/n--- Teste: Registro de Superusuário ---")
    register_data = {
        "username": "test_truman",
        "email": "test_truman@example.com",
        "Truman1_Marcelo1_1985": "secure_password_123", # Altere para uma senha forte
        "is_superuser": True
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/auth/register", json=register_data)
            response.raise_for_status() # Levanta exceção para status de erro (4xx ou 5xx)
            registered_user = response.json()
            print(f"Usuário registrado com sucesso: {registered_user['username']} (ID: {registered_user['id']})")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400 and "Username or email already registered" in e.response.text:
            print("Usuário 'test_admin' já existe. Prosseguindo para o login.")
        else:
            print(f"Erro ao registrar usuário: {e.response.status_code} - {e.response.text}")
            return # Parar se o registro falhar por outro motivo
    except httpx.RequestError as e:
        print(f"Erro de rede ao registrar usuário: {e}")
        return

    # --- 2. Login e Obter Token ---
    print("/n--- Teste: Login de Superusuário ---")
    login_data = {
        "username": "test_truman",
        "Truman1_Marcelo1_1985": "secure_password_123" # Use a mesma senha do registro
    }
    access_token = None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/auth/login", data=login_data)
            response.raise_for_status()
            login_response = response.json()
            access_token = login_response.get("access_token")
            print(f"Login bem-sucedido. Token obtido (truncado): {access_token[:20]}...")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao fazer login: {e.response.status_code} - {e.response.text}")
        return
    except httpx.RequestError as e:
        print(f"Erro de rede ao fazer login: {e}")
        return

    if not access_token:
        print("Falha ao obter token de acesso. Encerrando testes.")
        return

    headers = {"Authorization": f"Bearer {access_token}"}

    # --- 3. Teste: Listar Usuários (Rota Debug) ---
    print("/n--- Teste: GET /debug/users ---")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/debug/users", headers=headers)
            response.raise_for_status()
            users = response.json()
            print(f"Lista de usuários obtida com sucesso. Total: {len(users)} usuários.")
            # print(json.dumps(users, indent=2)) # Descomente para ver a lista completa
    except httpx.HTTPStatusError as e:
        print(f"Erro ao listar usuários: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao listar usuários: {e}")

    # --- 4. Teste: Resumo do Dashboard ---
    print("/n--- Teste: GET /dashboard/resumo ---")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/dashboard/resumo", headers=headers)
            response.raise_for_status()
            summary = response.json()
            print(f"Resumo do Dashboard obtido: {json.dumps(summary, indent=2)}")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao obter resumo do dashboard: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao obter resumo do dashboard: {e}")

    # --- 5. Teste: Relatório Mensal (Estatísticas) ---
    print("/n--- Teste: GET /statistics/relatorio-mensal ---")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/statistics/relatorio-mensal", headers=headers)
            response.raise_for_status()
            report = response.json()
            print(f"Relatório Mensal obtido. Total de entradas: {len(report)}")
            # print(json.dumps(report, indent=2)) # Descomente para ver o relatório completo
    except httpx.HTTPStatusError as e:
        print(f"Erro ao obter relatório mensal: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao obter relatório mensal: {e}")

    # --- 6. Criar um Cidadão (Pré-requisito para Justice e Atestado) ---
    print("/n--- Teste: Criar Cidadão ---")
    unique_bi = f"BI{datetime.now().strftime('%Y%m%d%H%M%S%f')}" # Garante BI único
    citizen_data = {
        "nomeCompleto": "Cidadão Teste Justice",
        "numeroBi": unique_bi,
        "naturalidade": "Luanda",
        "residencia": "Bairro Teste"
    }
    citizen_id_for_justice = None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/citizenship/citizen/", headers=headers, json=citizen_data)
            response.raise_for_status()
            created_citizen = response.json()
            citizen_id_for_justice = created_citizen.get("id")
            print(f"Cidadão criado com sucesso. ID: {citizen_id_for_justice}")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400 and "Cidadão com este número de BI já existe." in e.response.text:
            print("Cidadão já existe. Tentando obter ID do cidadão existente.")
            try:
                # Tenta obter o cidadão existente pelo BI (assumindo que há uma rota para isso)
                # Se não houver, esta parte precisará ser adaptada ou a criação de cidadão deve ser sempre única.
                # Como não temos uma rota GET /citizen/ por BI, vamos gerar um BI sempre único.
                print("Não foi possível obter cidadão existente por BI. Por favor, remova o cidadão manualmente ou use um BI sempre único.")
                return # Encerrar se não puder criar ou obter um cidadão válido
            except Exception as get_e:
                print(f"Erro ao obter cidadão existente: {get_e}")
                return
        else:
            print(f"Erro ao criar cidadão: {e.response.status_code} - {e.response.text}")
            return
    except httpx.RequestError as e:
        print(f"Erro de rede ao criar cidadão: {e}")
        return
    
    if not citizen_id_for_justice:
        print("Falha ao obter ID do cidadão. Encerrando testes.")
        return

    # --- 7. Teste: Criar Atestado de Residência ---
    print("/n--- Teste: POST /citizenship/atestado/ ---")
    atestado_data = {
        "nomeCompleto": "Cidadão Teste Atestado",
        "numeroBi": unique_bi, # <-- USANDO O BI DO CIDADÃO CRIADO
        "morada": "Rua do Atestado, 10",
        "finalidade": "Comprovante de morada",
        "estado": "pendente",
        "data": "2025-07-22" # Este campo é uma string no schema.prisma
    }
    atestado_id = None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/citizenship/atestado/", headers=headers, json=atestado_data)
            response.raise_for_status()
            created_atestado = response.json()
            atestado_id = created_atestado.get("id")
            print(f"Atestado criado com sucesso. ID: {atestado_id}")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao criar atestado: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao criar atestado: {e}")

    # --- 8. Teste: Criar Licença Comercial ---
    print("/n--- Teste: POST /commercial/licenca/ ---")
    licenca_data = {
        "nome_empresa": "Empresa Teste Licença",
        "nif": "NIF987654321",
        "atividade": "Comércio",
        "endereco": "Av. da Licença, 20",
        "validade": "2026-12-31",
        "estado": "ativo"
    }
    licenca_id = None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/commercial/licenca/", headers=headers, json=licenca_data)
            response.raise_for_status()
            created_licenca = response.json()
            licenca_id = created_licenca.get("id")
            print(f"Licença criada com sucesso. ID: {licenca_id}")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao criar licença: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao criar licença: {e}")

    # --- 9. Teste: Criar Certidão Sanitária ---
    print("/n--- Teste: POST /sanitation/ ---")
    certidao_data = {
        "titular": "Estabelecimento Teste",
        "localAtividade": "Rua da Higiene, 30", # <-- Corrigido para camelCase
        "finalidade": "Inspeção de rotina"
    }
    certidao_id = None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/sanitation/", headers=headers, json=certidao_data)
            response.raise_for_status()
            created_certidao = response.json()
            certidao_id = created_certidao.get("id")
            print(f"Certidão sanitária criada com sucesso. ID: {certidao_id}")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao criar certidão sanitária: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao criar certidão sanitária: {e}")

    # --- Testes de Justice (Usando o citizen_id criado/existente) ---
    print(f"/n--- Testes de Justice (usando citizen_id={citizen_id_for_justice}) ---")

    # --- 10. Teste: Emitir Certificado Judicial ---
    print("/n--- Teste: POST /justice/certificates/ ---")
    cert_judicial_data = {
        "citizenId": citizen_id_for_justice, # <-- Corrigido para camelCase
        "type": "antecedentes",
        "status": "Issued",
        "details": "Nenhum antecedente criminal",
        "documentPath": None # <-- Corrigido para camelCase
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/justice/certificates/", headers=headers, json=cert_judicial_data)
            response.raise_for_status()
            created_cert_judicial = response.json()
            print(f"Certificado Judicial criado com sucesso. ID: {created_cert_judicial.get('id')}")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao criar Certificado Judicial: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao criar Certificado Judicial: {e}")

    # --- 11. Teste: Solicitar Mediação ---
    print("/n--- Teste: POST /justice/mediation/ ---")
    mediation_data = {
        "citizenId": citizen_id_for_justice, # <-- Corrigido para camelCase
        "type": "Disputa",
        "status": "Open",
        "description": "Disputa de terras"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/justice/mediation/", headers=headers, json=mediation_data)
            response.raise_for_status()
            created_mediation = response.json()
            print(f"Solicitação de Mediação criada com sucesso. ID: {created_mediation.get('id')}")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao criar Solicitação de Mediação: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao criar Solicitação de Mediação: {e}")

    # --- 12. Teste: Registrar Processo Judicial ---
    print("/n--- Teste: POST /justice/processes/ ---")
    unique_process_number = f"PROC-{datetime.now().strftime('%Y%m%d%H%M%S%f')}" # Garante número único
    process_data = {
        "citizenId": citizen_id_for_justice, # <-- Corrigido para camelCase
        "processNumber": unique_process_number, # <-- AGORA É DINÂMICO
        "court": "Tribunal Supremo",
        "status": "Active"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/justice/processes/", headers=headers, json=process_data)
            response.raise_for_status()
            created_process = response.json()
            print(f"Processo Judicial criado com sucesso. ID: {created_process.get('id')}")
    except httpx.HTTPStatusError as e:
        print(f"Erro ao criar Processo Judicial: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de rede ao criar Processo Judicial: {e}")

    print("/nTestes de API concluídos.")

if __name__ == "__main__":
    asyncio.run(run_tests())

