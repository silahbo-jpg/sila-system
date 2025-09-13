#!/usr/bin/env python3
"""
Create Training Module CLI Tool for SILA System

This CLI tool creates and manages training modules for the SILA system.
It allows creation of safe training environments with fake data for learning purposes.

Usage:
    python create_training_module.py justice.mediation
    python create_training_module.py health.consultation --difficulty advanced
    python create_training_module.py --list-available
    python create_training_module.py --status
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import os

class TrainingModuleManager:
    """Manages SILA training modules"""
    
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.backend_dir = self.base_dir / "backend"
        self.training_dir = self.backend_dir / "app" / "modules" / "training"
        
        # Available modules and their configurations
        self.available_modules = {
            "health.consultation": {
                "display_name": "Agendamento de Consulta Médica",
                "description": "Aprenda a agendar consultas médicas no sistema de saúde",
                "difficulty_levels": ["beginner", "intermediate", "advanced"],
                "estimated_duration": 15,
                "learning_objectives": [
                    "Navegar no módulo de saúde",
                    "Preencher formulário de agendamento", 
                    "Confirmar consulta médica",
                    "Verificar disponibilidade de médicos"
                ],
                "real_services": ["agendamento_consulta", "consulta_medica"],
                "fake_data_types": ["citizen", "appointment", "medical"]
            },
            "citizenship.identity_card": {
                "display_name": "Solicitação de Carteira de Identidade",
                "description": "Pratique o processo de solicitação de documentos de identidade",
                "difficulty_levels": ["beginner", "intermediate", "advanced"],
                "estimated_duration": 25,
                "learning_objectives": [
                    "Compreender requisitos documentais",
                    "Preencher formulário de solicitação",
                    "Acompanhar status do pedido",
                    "Agendar recolha de documento"
                ],
                "real_services": ["carteira_identidade", "documentos_cidadania"],
                "fake_data_types": ["citizen", "document", "address"]
            },
            "finance.tax_consultation": {
                "display_name": "Consulta de Impostos e Taxas",
                "description": "Aprenda a consultar e pagar impostos municipais",
                "difficulty_levels": ["intermediate", "advanced"],
                "estimated_duration": 20,
                "learning_objectives": [
                    "Consultar impostos em atraso",
                    "Calcular multas e juros",
                    "Efetuar pagamentos",
                    "Obter comprovatives"
                ],
                "real_services": ["consulta_impostos", "pagamento_taxas"],
                "fake_data_types": ["citizen", "financial", "business"]
            },
            "education.enrollment": {
                "display_name": "Matrícula Escolar",
                "description": "Sistema de matrícula e transferência escolar",
                "difficulty_levels": ["beginner", "intermediate"],
                "estimated_duration": 18,
                "learning_objectives": [
                    "Pesquisar escolas disponíveis",
                    "Preencher formulário de matrícula",
                    "Anexar documentos necessários",
                    "Confirmar vaga"
                ],
                "real_services": ["matricula_escolar", "transferencia_escolar"],
                "fake_data_types": ["citizen", "student", "family"]
            },
            "justice.mediation": {
                "display_name": "Solicitação de Mediação",
                "description": "Processo de mediação de conflitos comunitários",
                "difficulty_levels": ["intermediate", "advanced"],
                "estimated_duration": 30,
                "learning_objectives": [
                    "Identificar casos para mediação",
                    "Preencher formulário detalhado",
                    "Entender processo de mediação",
                    "Agendar sessões"
                ],
                "real_services": ["solicitacao_mediacao", "agendamento_mediacao"],
                "fake_data_types": ["citizen", "conflict", "contact"]
            },
            "urbanism.building_permit": {
                "display_name": "Licenciamento de Obras",
                "description": "Processo de licenciamento para construção e obras",
                "difficulty_levels": ["advanced"],
                "estimated_duration": 35,
                "learning_objectives": [
                    "Compreender tipos de licenças",
                    "Preparar documentação técnica",
                    "Submeter pedido",
                    "Acompanhar processo de aprovação"
                ],
                "real_services": ["licenciamento_obras", "aprovacao_projetos"],
                "fake_data_types": ["citizen", "business", "technical"]
            }
        }
        
    def create_training_module(
        self,
        module_name: str,
        difficulty: str = "beginner",
        duration: int = None,
        custom_objectives: List[str] = None
    ):
        """Create a new training module"""
        
        print(f"🎓 Creating Training Module: {module_name}")
        
        # Validate module
        if module_name not in self.available_modules:
            print(f"❌ Unknown module: {module_name}")
            print(f"Available modules: {list(self.available_modules.keys())}")
            return False
            
        module_config = self.available_modules[module_name]
        
        # Validate difficulty
        if difficulty not in module_config["difficulty_levels"]:
            print(f"❌ Invalid difficulty '{difficulty}' for module {module_name}")
            print(f"Available difficulties: {module_config['difficulty_levels']}")
            return False
            
        # Create training service replicas
        print(f"📋 Creating service replicas for {module_name}...")
        self._create_service_replicas(module_name, module_config)
        
        # Generate training scenarios
        print(f"🎭 Generating training scenarios...")
        scenarios = self._generate_training_scenarios(module_name, difficulty)
        
        # Create training routes
        print(f"🛤️  Creating training routes...")
        self._create_training_routes(module_name, module_config, difficulty)
        
        # Setup fake data generators
        print(f"🤖 Configuring fake data generators...")
        self._setup_fake_data_generators(module_name, module_config["fake_data_types"])
        
        # Create training documentation
        print(f"📚 Generating training documentation...")
        self._create_training_docs(module_name, module_config, scenarios)
        
        print(f"✅ Training module '{module_name}' created successfully!")
        print(f"🎯 Difficulty: {difficulty}")
        print(f"⏱️  Duration: {duration or module_config['estimated_duration']} minutes")
        print(f"🔗 Access via: /training/{module_name.replace('.', '/')}")
        
        return True
        
    def _create_service_replicas(self, module_name: str, config: Dict):
        """Create safe replicas of real services for training"""
        
        module_parts = module_name.split('.')
        base_module = module_parts[0]  # health, citizenship, etc.
        service_name = module_parts[1]  # consultation, identity_card, etc.
        
        # Create training service directory
        training_service_dir = self.training_dir / "services" / base_module
        training_service_dir.mkdir(parents=True, exist_ok=True)
        
        # Create training service file
        service_content = self._generate_training_service_code(module_name, config)
        service_file = training_service_dir / f"{service_name}.py"
        
        with open(service_file, 'w', encoding='utf-8') as f:
            f.write(service_content)
            
        print(f"  ✓ Created training service: {service_file}")
        
    def _create_training_routes(self, module_name: str, config: Dict, difficulty: str):
        """Create training-specific API routes"""
        
        module_parts = module_name.split('.')
        base_module = module_parts[0]
        service_name = module_parts[1]
        
        # Create training routes directory
        routes_dir = self.training_dir / "routes" / base_module
        routes_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate route content
        route_content = self._generate_training_route_code(module_name, config, difficulty)
        route_file = routes_dir / f"{service_name}.py"
        
        with open(route_file, 'w', encoding='utf-8') as f:
            f.write(route_content)
            
        print(f"  ✓ Created training routes: {route_file}")
        
    def _generate_training_scenarios(self, module_name: str, difficulty: str) -> List[Dict]:
        """Generate training scenarios for the module"""
        
        scenarios = []
        
        if module_name == "health.consultation":
            scenarios = [
                {
                    "name": "Consulta de Rotina",
                    "difficulty": "beginner",
                    "description": "Agendar uma consulta médica de rotina",
                    "citizen_profile": {"age_group": "adult", "health_status": "healthy"},
                    "expected_outcome": "Consulta agendada com sucesso"
                },
                {
                    "name": "Consulta Urgente",
                    "difficulty": "intermediate", 
                    "description": "Agendar consulta urgente com sintomas",
                    "citizen_profile": {"age_group": "elderly", "health_status": "symptomatic"},
                    "expected_outcome": "Consulta urgente agendada"
                }
            ]
        elif module_name == "citizenship.identity_card":
            scenarios = [
                {
                    "name": "Primeira Via BI",
                    "difficulty": "beginner",
                    "description": "Solicitar primeira via do Bilhete de Identidade",
                    "citizen_profile": {"age_group": "young_adult", "document_status": "first_time"},
                    "expected_outcome": "Pedido de BI submetido"
                },
                {
                    "name": "Renovação BI Expirado",
                    "difficulty": "intermediate",
                    "description": "Renovar BI que expirou há mais de 6 meses",
                    "citizen_profile": {"age_group": "adult", "document_status": "expired"},
                    "expected_outcome": "Renovação processada"
                }
            ]
        # Add more scenarios for other modules...
        
        # Filter by difficulty
        return [s for s in scenarios if s["difficulty"] == difficulty or difficulty == "advanced"]
        
    def _generate_training_service_code(self, module_name: str, config: Dict) -> str:
        """Generate Python code for training service"""
        
        module_parts = module_name.split('.')
        service_name = module_parts[1].replace('_', ' ').title().replace(' ', '')
        
        return f'''"""
Training Service: {config['display_name']}

This is a SAFE training replica of the {module_name} service.
All operations use fake data and do not affect real system data.

⚠️ TRAINING MODE - Safe Environment
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List, Any
from datetime import datetime
from app.db.session import get_db
from app.modules.training.fake_data import FakeDataGenerator, generate_training_scenario
from app.modules.training.models import TrainingSession
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/training/{module_parts[0]}/{module_parts[1]}",
    tags=["Training - {config['display_name']}"]
)

# Fake data generator for this module
fake_generator = FakeDataGenerator()

@router.get("/")
async def get_training_module_info():
    """Get information about this training module"""
    return {{
        "module_name": "{module_name}",
        "display_name": "{config['display_name']}",
        "description": "{config['description']}",
        "status": "training_mode",
        "warning": "⚠️ TRAINING MODE - All data is fake and safe",
        "learning_objectives": {config['learning_objectives']},
        "estimated_duration": {config['estimated_duration']},
        "real_services_taught": {config['real_services']}
    }}

@router.post("/start-session")
async def start_training_session(
    user_name: str,
    difficulty: str = "beginner",
    db: Session = Depends(get_db)
):
    """Start a new training session for this module"""
    
    # Generate fake scenario data
    scenario_data = generate_training_scenario("{module_name}")
    
    # Create training session record
    session = TrainingSession(
        user_name=user_name,
        training_module="{module_name}",
        difficulty_level=difficulty,
        fake_citizen_data=scenario_data,
        status="active"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    logger.info(f"Training session started: {{session.id}} for {module_name}")
    
    return {{
        "status": "success",
        "session_id": session.id,
        "message": "Training session started - using fake data",
        "scenario_data": scenario_data,
        "next_steps": [
            "Review the citizen information provided",
            "Follow the step-by-step process",
            "Complete all required fields",
            "Submit the request"
        ]
    }}

@router.post("/simulate-action")
async def simulate_service_action(
    session_id: int,
    action: str,
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Simulate a service action with fake data"""
    
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")
        
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Training session is not active")
    
    # Simulate the action
    result = {{
        "action": action,
        "status": "success",
        "message": f"Training action '{{action}}' completed successfully",
        "fake_data_used": True,
        "simulation_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat()
    }}
    
    # Update session progress
    session.steps_completed += 1
    db.commit()
    
    return result

@router.get("/practice-scenarios")
async def get_practice_scenarios():
    """Get available practice scenarios for this module"""
    
    return {{
        "module": "{module_name}",
        "available_scenarios": [
            {{
                "id": 1,
                "name": "Cenário Básico",
                "difficulty": "beginner",
                "description": "Processo padrão sem complicações",
                "estimated_time": "10 minutos"
            }},
            {{
                "id": 2,
                "name": "Cenário com Complicações", 
                "difficulty": "intermediate",
                "description": "Processo com documentos em falta",
                "estimated_time": "15 minutos"
            }},
            {{
                "id": 3,
                "name": "Cenário Complexo",
                "difficulty": "advanced", 
                "description": "Caso especial com múltiplas validações",
                "estimated_time": "20 minutos"
            }}
        ]
    }}

@router.get("/fake-data/generate")
async def generate_training_data(data_type: str = "citizen"):
    """Generate fresh fake data for practice"""
    
    generators = {{
        "citizen": fake_generator.generate_citizen_data,
        "appointment": fake_generator.generate_appointment_data,
        "document": fake_generator.generate_document_data,
        "business": fake_generator.generate_business_data,
        "financial": fake_generator.generate_financial_data
    }}
    
    if data_type not in generators:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid data type. Available: {{list(generators.keys())}}"
        )
    
    return {{
        "status": "success",
        "data_type": data_type,
        "warning": "🤖 This is fake data for training only",
        "data": generators[data_type]()
    }}
'''
        
    def _generate_training_route_code(self, module_name: str, config: Dict, difficulty: str) -> str:
        """Generate training route code"""
        
        return f'''"""
Training Routes for {config['display_name']}

Safe training environment routes that replicate real service functionality
using fake data.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from app.db.session import get_db
from app.modules.training.schemas import TrainingSessionRead, TrainingResponse
from app.modules.training.fake_data import FakeDataGenerator
from datetime import datetime

router = APIRouter()

@router.get("/tutorial")
async def get_tutorial_steps():
    """Get step-by-step tutorial for this module"""
    
    tutorial_steps = {config['learning_objectives']}
    
    return {{
        "module": "{module_name}",
        "tutorial_steps": tutorial_steps,
        "estimated_duration": "{config['estimated_duration']} minutes",
        "difficulty": "{difficulty}"
    }}

@router.post("/validate-input")
async def validate_training_input(data: Dict[str, Any]):
    """Validate user input during training (with helpful feedback)"""
    
    validation_results = []
    
    # Simulate input validation with educational feedback
    for field, value in data.items():
        if not value or (isinstance(value, str) and len(value.strip()) == 0):
            validation_results.append({{
                "field": field,
                "status": "error",
                "message": f"O campo {{field}} é obrigatório",
                "tip": "Certifique-se de preencher todos os campos obrigatórios"
            }})
        else:
            validation_results.append({{
                "field": field,
                "status": "success",
                "message": "Campo válido"
            }})
    
    return {{
        "status": "validation_complete",
        "results": validation_results,
        "overall_valid": all(r["status"] == "success" for r in validation_results)
    }}

@router.get("/help/{{topic}}")
async def get_contextual_help(topic: str):
    """Get contextual help for specific topics"""
    
    help_content = {{
        "documents": "Lista de documentos necessários e onde obtê-los",
        "process": "Explicação passo-a-passo do processo completo", 
        "requirements": "Requisitos e critérios de elegibilidade",
        "fees": "Informações sobre taxas e formas de pagamento",
        "timeline": "Prazos típicos para processamento"
    }}
    
    return {{
        "topic": topic,
        "content": help_content.get(topic, "Tópico de ajuda não encontrado"),
        "related_topics": list(help_content.keys())
    }}
'''

    def _setup_fake_data_generators(self, module_name: str, data_types: List[str]):
        """Setup fake data generators for the module"""
        
        # Create generator configuration file
        generator_config = {
            "module_name": module_name,
            "data_types": data_types,
            "locale": "pt",
            "generation_rules": {
                "citizen": {"include_family": True, "include_employment": True},
                "appointment": {"future_dates_only": True, "business_hours": True},
                "document": {"valid_types_only": True, "include_fees": True}
            }
        }
        
        config_file = self.training_dir / "config" / f"{module_name.replace('.', '_')}_generator.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(generator_config, f, indent=2, ensure_ascii=False)
            
        print(f"  ✓ Configured fake data generators: {config_file}")
        
    def _create_training_docs(self, module_name: str, config: Dict, scenarios: List[Dict]):
        """Create training documentation"""
        
        docs_content = f"""# Training Module: {config['display_name']}

## Overview
{config['description']}

**⚠️ TRAINING MODE**: This module uses fake data and safe operations. No real data will be modified.

## Learning Objectives
{chr(10).join(f'- {obj}' for obj in config['learning_objectives'])}

## Duration
Estimated: {config['estimated_duration']} minutes

## Available Scenarios
{chr(10).join(f'### {scenario["name"]}' + chr(10) + f'**Difficulty**: {scenario["difficulty"]}' + chr(10) + f'{scenario["description"]}' + chr(10) for scenario in scenarios)}

## How to Use
1. Start a training session: `POST /training/{module_name.replace('.', '/')}/start-session`
2. Follow the step-by-step tutorial
3. Practice with different scenarios
4. Get contextual help when needed
5. Complete the session for feedback

## API Endpoints
- `GET /training/{module_name.replace('.', '/')}/` - Module information
- `POST /training/{module_name.replace('.', '/')}/start-session` - Start training
- `POST /training/{module_name.replace('.', '/')}/simulate-action` - Simulate actions
- `GET /training/{module_name.replace('.', '/')}/tutorial` - Get tutorial steps
- `GET /training/{module_name.replace('.', '/')}/fake-data/generate` - Generate test data

## Safety Features
- All data is fake and clearly marked
- No connection to real databases
- Safe sandbox environment
- Progress tracking and feedback
- Educational tips and guidance

## Related Services
This training module teaches: {', '.join(config['real_services'])}
"""

        docs_dir = self.training_dir / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        docs_file = docs_dir / f"{module_name.replace('.', '_')}.md"
        with open(docs_file, 'w', encoding='utf-8') as f:
            f.write(docs_content)
            
        print(f"  ✓ Created training documentation: {docs_file}")
        
    def list_available_modules(self):
        """List all available training modules"""
        
        print("📚 Available Training Modules:")
        print("")
        
        for module_name, config in self.available_modules.items():
            print(f"🎓 {module_name}")
            print(f"   📝 {config['display_name']}")
            print(f"   📖 {config['description']}")
            print(f"   ⏱️  Duration: {config['estimated_duration']} minutes")
            print(f"   📊 Difficulties: {', '.join(config['difficulty_levels'])}")
            print(f"   🎯 Objectives: {len(config['learning_objectives'])} learning goals")
            print("")
            
    def get_status(self):
        """Get training system status"""
        
        print("🎓 SILA Training System Status")
        print("")
        
        # Check if training directory exists
        training_exists = self.training_dir.exists()
        print(f"Training Directory: {'✅ Available' if training_exists else '❌ Not Found'}")
        
        # Check created modules
        if training_exists:
            services_dir = self.training_dir / "services"
            routes_dir = self.training_dir / "routes"
            
            created_services = []
            if services_dir.exists():
                for module_dir in services_dir.iterdir():
                    if module_dir.is_dir():
                        services = list(module_dir.glob("*.py"))
                        created_services.extend([f"{module_dir.name}.{s.stem}" for s in services])
                        
            print(f"Created Training Modules: {len(created_services)}")
            for service in created_services:
                print(f"  ✅ {service}")
                
        print(f"")
        print(f"Available Modules: {len(self.available_modules)}")
        print(f"Training API: /training/*")
        print(f"Documentation: /training/docs/")

def main():
    parser = argparse.ArgumentParser(description="SILA Training Module Creator")
    
    parser.add_argument(
        "module_name",
        nargs="?",
        help="Training module to create (e.g., justice.mediation)"
    )
    
    parser.add_argument(
        "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        default="beginner",
        help="Training difficulty level"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        help="Custom duration in minutes"
    )
    
    parser.add_argument(
        "--list-available",
        action="store_true",
        help="List all available training modules"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check training system status"
    )
    
    args = parser.parse_args()
    
    manager = TrainingModuleManager()
    
    if args.list_available:
        manager.list_available_modules()
    elif args.status:
        manager.get_status()
    elif args.module_name:
        success = manager.create_training_module(
            module_name=args.module_name,
            difficulty=args.difficulty,
            duration=args.duration
        )
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()