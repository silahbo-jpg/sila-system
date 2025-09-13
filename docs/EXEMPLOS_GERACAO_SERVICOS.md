# Exemplos de Geração de Serviços no SILA

Este documento fornece exemplos práticos de como utilizar os scripts de geração de serviços no SILA.

## Gerando um Serviço Individual

Para gerar um serviço individual em um módulo existente, utilize o script `generate_service.py`:

```bash
python scripts/generate_service.py health AgendamentoTeleconsulta
```

Resultado:
- Cria o arquivo de modelo: `backend/app/modules/health/models/agendamento_teleconsulta.py`
- Cria o arquivo de esquema: `backend/app/modules/health/schemas/agendamento_teleconsulta.py`
- Cria o arquivo de rota: `backend/app/modules/health/routes/agendamento_teleconsulta.py`
- Registra o serviço no `service_hub` através do decorator `@register_service`
- Adiciona a rota ao router do módulo

O serviço estará disponível em: `/api/agendamento-teleconsulta/`

## Gerando Múltiplos Serviços em Lote

### Usando a Lista Padrão

```bash
python scripts/batch_generate_services.py --default
```

Este comando gerará os seguintes serviços:
- `citizenship`: EmissaoBI, AtualizacaoEndereco
- `health`: AgendamentoConsulta, SolicitacaoExame
- `education`: MatriculaEscolar
- `commercial`: AberturaProcesso
- `urbanism`: LicencaConstrucao

### Usando um Arquivo CSV Personalizado

```bash
python scripts/batch_generate_services.py --csv scripts/service_catalog.csv
```

Este comando gerará todos os serviços listados no arquivo CSV, que contém mais de 100 serviços pré-definidos para diferentes módulos.

### Criando um Arquivo CSV Personalizado

```bash
python scripts/batch_generate_services.py --create-csv meus_servicos.csv
```

Este comando criará um arquivo CSV de exemplo que você pode editar para incluir seus próprios serviços.

## Estrutura dos Serviços Gerados

Cada serviço gerado inclui:

### Modelo (models/nome_servico.py)

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class NomeServico(Base):
    __tablename__ = "modulo_nome_servico"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(String(500))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    municipe_id = Column(Integer, nullable=False)
```

### Esquema (schemas/nome_servico.py)

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NomeServicoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None

class NomeServicoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

class NomeServicoRead(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    ativo: bool
    data_criacao: datetime

    class Config:
        from_attributes = True
```

### Rota (routes/nome_servico.py)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.modulo.models.nome_servico import NomeServico
from app.modules.modulo.schemas.nome_servico import NomeServicoCreate, NomeServicoRead, NomeServicoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/nome-servico", tags=["Nome Servico"])

@router.post("/", response_model=NomeServicoRead)
def criar_nome_servico(data: NomeServicoCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # Implementação
    pass

@router.get("/{id}", response_model=NomeServicoRead)
def obter_nome_servico(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # Implementação
    pass

@router.get("/", response_model=list[NomeServicoRead])
def listar_nome_servico(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # Implementação
    pass

@router.put("/{id}", response_model=NomeServicoRead)
def atualizar_nome_servico(id: int, data: NomeServicoUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # Implementação
    pass
```

### Registro no Service Hub

```python
@register_service(
    slug="nome-servico",
    nome="Nome Servico",
    descricao="Serviço para nome servico",
    departamento="modulo",
    categoria="modulo"
)
def nome_servico_handler(data):
    # Implementação do serviço
    return {"status": "success"}
```

## Próximos Passos

Após gerar os serviços:

1. Implemente a lógica de negócio nos handlers de serviço
2. Adicione validações específicas nos esquemas
3. Expanda os modelos com campos adicionais conforme necessário
4. Implemente testes para os novos serviços
5. Atualize a documentação da API

Para mais informações, consulte o documento [ADICIONAR_NOVOS_SERVICOS.md](ADICIONAR_NOVOS_SERVICOS.md).
