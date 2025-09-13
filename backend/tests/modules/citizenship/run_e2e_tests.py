"""
Script para executar testes de ponta a ponta (E2E) no módulo de cidadania.

Este script pode ser executado de forma independente e inclui um servidor mock para testes.
"""
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from urllib.parse import urlparse, parse_qs

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, "/home/truman/SGI/sila/postgres/backend")

# Dados de teste
MOCK_DB = {
    "citizens": {},
    "users": {
        "admin_test": {
            "username": "admin_test",
            "Truman1_Marcelo1_1985": "testpassword123",
            "permissions": ["citizenship:full_access"]
        },
        "operator": {
            "username": "operator",
            "Truman1_Marcelo1_1985": "operator123",
            "permissions": ["citizenship:read"]
        }
    },
    "tokens": {}
}

class MockServer(BaseHTTPRequestHandler):
    """Servidor mock para testes de API."""
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
    
    def _parse_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            return json.loads(self.rfile.read(content_length).decode('utf-8'))
        return {}
    
    def do_GET(self):
        """Lida com requisições GET."""
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # Rota de health check
        if self.path == '/api/v1/health':
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return
        
        # Rota para obter cidadão por ID
        if len(path_parts) >= 4 and path_parts[-2] == 'citizens':
            citizen_id = path_parts[-1]
            if citizen_id in MOCK_DB["citizens"]:
                self._set_headers(200)
                self.wfile.write(json.dumps(MOCK_DB["citizens"][citizen_id]).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"detail": "Cidadão não encontrado"}).encode())
            return
        
        self._set_headers(404)
        self.wfile.write(json.dumps({"detail": "Rota não encontrada"}).encode())
    
    def do_POST(self):
        """Lida com requisições POST."""
        # Rota de login
        if self.path == '/api/v1/auth/login':
            body = self._parse_body()
            username = body.get('username')
            Truman1_Marcelo1_1985 = body.get('Truman1_Marcelo1_1985')
            
            if username in MOCK_DB["users"] and MOCK_DB["users"][username]["Truman1_Marcelo1_1985"] == Truman1_Marcelo1_1985:
                token = f"mock_token_{username}"
                MOCK_DB["tokens"][token] = {
                    "username": username,
                    "permissions": MOCK_DB["users"][username]["permissions"]
                }
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "access_token": token,
                    "token_type": "bearer"
                }).encode())
            else:
                self._set_headers(401)
                self.wfile.write(json.dumps({"detail": "Credenciais inválidas"}).encode())
            return
        
        # Rota para criar cidadão
        if self.path == '/api/v1/citizenship/citizens/':
            # Verifica autenticação
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self._set_headers(401)
                self.wfile.write(json.dumps({"detail": "Não autenticado"}).encode())
                return
            
            token = auth_header.split(' ')[1]
            if token not in MOCK_DB["tokens"]:
                self._set_headers(401)
                self.wfile.write(json.dumps({"detail": "Token inválido"}).encode())
                return
            
            # Verifica permissões
            user_permissions = MOCK_DB["tokens"][token]["permissions"]
            if "citizenship:full_access" not in user_permissions and "citizenship:write" not in user_permissions:
                self._set_headers(403)
                self.wfile.write(json.dumps({"detail": "Permissão negada"}).encode())
                return
            
            # Cria o cidadão
            citizen_data = self._parse_body()
            citizen_id = f"citizen_{len(MOCK_DB['citizens']) + 1}"
            citizen = {"id": citizen_id, **citizen_data}
            MOCK_DB["citizens"][citizen_id] = citizen
            
            self._set_headers(201)
            self.wfile.write(json.dumps(citizen).encode())
            return
        
        # Rota de busca de cidadãos
        if self.path == '/api/v1/citizenship/citizens/search/':
            # Implementação simplificada da busca
            query = self._parse_body()
            items = list(MOCK_DB["citizens"].values())
            
            # Filtra por nome se fornecido
            if "nome_completo" in query:
                search_term = query["nome_completo"].lower()
                items = [c for c in items if search_term in c.get("nome_completo", "").lower()]
            
            # Paginação simplificada
            page = int(query.get("page", 1))
            page_size = int(query.get("page_size", 10))
            start = (page - 1) * page_size
            end = start + page_size
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "items": items[start:end],
                "total": len(items),
                "page": page,
                "page_size": page_size,
                "total_pages": (len(items) + page_size - 1) // page_size
            }).encode())
            return
        
        self._set_headers(404)
        self.wfile.write(json.dumps({"detail": "Rota não encontrada"}).encode())
    
    def do_PUT(self):
        """Lida com requisições PUT."""
        # Rota para atualizar cidadão
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) >= 4 and path_parts[-2] == 'citizens':
            citizen_id = path_parts[-1]
            
            # Verifica autenticação
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self._set_headers(401)
                self.wfile.write(json.dumps({"detail": "Não autenticado"}).encode())
                return
            
            token = auth_header.split(' ')[1]
            if token not in MOCK_DB["tokens"]:
                self._set_headers(401)
                self.wfile.write(json.dumps({"detail": "Token inválido"}).encode())
                return
            
            # Verifica permissões
            user_permissions = MOCK_DB["tokens"][token]["permissions"]
            if "citizenship:full_access" not in user_permissions and "citizenship:write" not in user_permissions:
                self._set_headers(403)
                self.wfile.write(json.dumps({"detail": "Permissão negada"}).encode())
                return
            
            # Atualiza o cidadão
            if citizen_id not in MOCK_DB["citizens"]:
                self._set_headers(404)
                self.wfile.write(json.dumps({"detail": "Cidadão não encontrado"}).encode())
                return
            
            update_data = self._parse_body()
            MOCK_DB["citizens"][citizen_id].update(update_data)
            
            self._set_headers(200)
            self.wfile.write(json.dumps(MOCK_DB["citizens"][citizen_id]).encode())
            return
        
        self._set_headers(404)
        self.wfile.write(json.dumps({"detail": "Rota não encontrada"}).encode())
    
    def do_DELETE(self):
        """Lida com requisições DELETE."""
        # Rota para excluir cidadão
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) >= 4 and path_parts[-2] == 'citizens':
            citizen_id = path_parts[-1]
            
            # Verifica autenticação
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self._set_headers(401)
                self.wfile.write(json.dumps({"detail": "Não autenticado"}).encode())
                return
            
            token = auth_header.split(' ')[1]
            if token not in MOCK_DB["tokens"]:
                self._set_headers(401)
                self.wfile.write(json.dumps({"detail": "Token inválido"}).encode())
                return
            
            # Verifica permissões
            user_permissions = MOCK_DB["tokens"][token]["permissions"]
            if "citizenship:full_access" not in user_permissions:
                self._set_headers(403)
                self.wfile.write(json.dumps({"detail": "Permissão negada"}).encode())
                return
            
            # Remove o cidadão
            if citizen_id in MOCK_DB["citizens"]:
                del MOCK_DB["citizens"][citizen_id]
                self._set_headers(200)
                self.wfile.write(json.dumps({"status": "Cidadão excluído com sucesso"}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"detail": "Cidadão não encontrado"}).encode())
            return
        
        self._set_headers(404)
        self.wfile.write(json.dumps({"detail": "Rota não encontrada"}).encode())

def run_mock_server(port=8000):
    """Inicia o servidor mock em uma thread separada."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockServer)
    print(f"🚀 Servidor mock rodando na porta {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    # Inicia o servidor mock em uma thread separada
    server_thread = Thread(target=run_mock_server, daemon=True)
    server_thread.start()
    
    # Aguarda o usuário pressionar Enter para encerrar
    try:
        input("Pressione Enter para encerrar o servidor mock...\n")
    except KeyboardInterrupt:
        pass
    finally:
        print("\nEncerrando servidor mock...")
        sys.exit(0)

