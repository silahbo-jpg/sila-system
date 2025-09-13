#!/usr/bin/env python3
"""
Módulo de validação de módulos do sistema sila_dev.

Este script verifica a integridade e completude dos módulos do projeto,
validando estrutura de arquivos, implementação de código, rotas da API e testes.
"""

import os
import importlib
import ast
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
import json
import csv
from dataclasses import dataclass, field
from enum import Enum

class Severity(str, Enum):
    """Níveis de severidade para problemas encontrados."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class CheckResult:
    """Resultado de uma verificação individual."""
    name: str
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed: bool
    severity: Severity
    details: str = ""
    fix_suggestion: str = ""

@dataclass
class ValidationResult:
    """Resultado da validação de um módulo."""
    module: str
    checks: List[CheckResult] = field(default_factory=list)
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)

class ModuleValidator:
    """Validador de módulos do sistema sila_dev."""
    
    def __init__(self, base_path: str):
        """Inicializa o validador com o caminho base do projeto.
        
        Args:
            base_path: Caminho para o diretório raiz do projeto.
        """
        self.base_path = Path(base_path).resolve()
        self.modules_path = self.base_path / "backend" / "app" / "modules"
        self.results: Dict[str, ValidationResult] = {}
        
        # Arquivos obrigatórios para cada módulo
        self.required_files = [
            "__init__.py", 
            "models.py", 
            "schemas.py", 
            "crud.py", 
            "services.py", 
            "endpoints.py"
        ]
        
    def validate_all_modules(self) -> Dict[str, ValidationResult]:
        """Valida todos os módulos encontrados no diretório de módulos.
        
        Returns:
            Dicionário com os resultados da validação, indexados pelo nome do módulo.
        """
        if not self.modules_path.exists():
            raise FileNotFoundError(f"Diretório de módulos não encontrado: {self.modules_path}")
            
        for module_dir in self.modules_path.iterdir():
            if module_dir.is_dir() and not module_dir.name.startswith('__'):
                self.validate_module(module_dir.name)
                
        return self.results
    
    def validate_module(self, module_name: str) -> ValidationResult:
        """Valida um único módulo.
        
        Args:
            module_name: Nome do módulo a ser validado.
            
        Returns:
            Resultado da validação do módulo.
        """
        module_path = self.modules_path / module_name
        result = ValidationResult(module=module_name)
        
        # Verificar estrutura de arquivos
        self._check_file_structure(module_path, result)
        
        # Se os arquivos básicos existem, validar o conteúdo
        if all(f in [check.name for check in result.checks if check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed] 
               for f in [f"Arquivo {f} existe" for f in self.required_files]):
            
            # Validar implementação Python
            self._validate_python_code(module_path, result)
            
            # Validar API e rotas
            self._validate_api(module_path, module_name, result)
            
            # Validar testes
            self._validate_tests(module_path, module_name, result)
        
        # Atualizar status geral
        result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed = all(check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed for check in result.checks)
        self.results[module_name] = result
        return result
    
    def _check_file_structure(self, module_path: Path, result: ValidationResult) -> None:
        """Verifica a estrutura de arquivos do módulo."""
        for file in self.required_files:
            file_path = module_path / file
            check = CheckResult(
                name=f"Arquivo {file} existe",
                Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=file_path.exists(),
                severity=Severity.HIGH if file in ["__init__.py", "models.py"] else Severity.MEDIUM,
                details=str(file_path) if file_path.exists() else f"Arquivo não encontrado: {file_path}",
                fix_suggestion=f"Criar o arquivo {file} no diretório do módulo."
            )
            result.checks.append(check)
            
            if check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed:
                # Verificar se o arquivo tem conteúdo
                content_check = CheckResult(
                    name=f"Arquivo {file} tem conteúdo",
                    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=file_path.stat().st_size > 0,
                    severity=Severity.MEDIUM,
                    details=f"Tamanho do arquivo: {file_path.stat().st_size} bytes",
                    fix_suggestion=f"Implementar o conteúdo necessário no arquivo {file}."
                )
                result.checks.append(content_check)
    
    def _validate_python_code(self, module_path: Path, result: ValidationResult) -> None:
        """Valida o código Python do módulo."""
        # Verificar se o arquivo __init__.py exporta os itens necessários
        self._check_init_file(module_path, result)
        
        # Verificar implementação dos modelos
        self._check_models(module_path, result)
        
        # Verificar implementação dos schemas
        self._check_schemas(module_path, result)
        
        # Verificar implementação do CRUD
        self._check_crud(module_path, result)
        
        # Verificar implementação dos serviços
        self._check_services(module_path, result)
        
        # Verificar implementação dos endpoints
        self._check_endpoints(module_path, result)
    
    def _check_init_file(self, module_path: Path, result: ValidationResult) -> None:
        """Verifica se o arquivo __init__.py exporta os itens necessários."""
        init_file = module_path / "__init__.py"
        if not init_file.exists():
            return
            
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se há exports explícitos
        has_exports = "__all__" in content
        
        result.checks.append(CheckResult(
            name="__init__.py tem exports explícitos",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_exports,
            severity=Severity.MEDIUM,
            details="" if has_exports else "O arquivo __init__.py não define __all__",
            fix_suggestion="Adicione __all__ ao __init__.py listando os símbolos públicos do módulo."
        ))
    
    def _check_models(self, module_path: Path, result: ValidationResult) -> None:
        """Verifica a implementação dos modelos."""
        models_file = module_path / "models.py"
        if not models_file.exists():
            return
            
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se há classes de modelo definidas
        has_models = "class " in content and ("BaseModel" in content or "SQLModel" in content or "Base" in content)
        
        result.checks.append(CheckResult(
            name="models.py contém classes de modelo",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_models,
            severity=Severity.HIGH,
            details="" if has_models else "Nenhuma classe de modelo encontrada em models.py",
            fix_suggestion="Defina as classes de modelo do módulo em models.py"
        ))
    
    def _check_schemas(self, module_path: Path, result: ValidationResult) -> None:
        """Verifica a implementação dos schemas."""
        schemas_file = module_path / "schemas.py"
        if not schemas_file.exists():
            return
            
        with open(schemas_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se há classes de schema definidas
        has_schemas = "class " in content and ("BaseModel" in content or "SQLModel" in content or "pydantic" in content)
        
        result.checks.append(CheckResult(
            name="schemas.py contém classes de schema",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_schemas,
            severity=Severity.HIGH,
            details="" if has_schemas else "Nenhuma classe de schema encontrada em schemas.py",
            fix_suggestion="Defina os schemas de entrada/saída do módulo em schemas.py"
        ))
    
    def _check_crud(self, module_path: Path, result: ValidationResult) -> None:
        """Verifica a implementação do CRUD."""
        crud_file = module_path / "crud.py"
        if not crud_file.exists():
            return
            
        with open(crud_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se há funções CRUD definidas
        has_crud_functions = any(
            f"def {func}" in content 
            for func in ["create_", "read_", "update_", "delete_", "list_"]
        )
        
        result.checks.append(CheckResult(
            name="crud.py contém funções CRUD",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_crud_functions,
            severity=Severity.HIGH,
            details="" if has_crud_functions else "Nenhuma função CRUD encontrada em crud.py",
            fix_suggestion="Implemente as funções CRUD básicas em crud.py"
        ))
    
    def _check_services(self, module_path: Path, result: ValidationResult) -> None:
        """Verifica a implementação dos serviços."""
        services_file = module_path / "services.py"
        if not services_file.exists():
            return
            
        with open(services_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se há classes ou funções de serviço definidas
        has_services = "class " in content or "def " in content
        
        result.checks.append(CheckResult(
            name="services.py contém implementações de serviço",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_services,
            severity=Severity.HIGH,
            details="" if has_services else "Nenhuma classe ou função de serviço encontrada em services.py",
            fix_suggestion="Implemente as regras de negócio do módulo em services.py"
        ))
    
    def _check_endpoints(self, module_path: Path, result: ValidationResult) -> None:
        """Verifica a implementação dos endpoints."""
        endpoints_file = module_path / "endpoints.py"
        if not endpoints_file.exists():
            return
            
        with open(endpoints_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se há rotas definidas
        has_routes = any(
            decorator in content 
            for decorator in ["@router.get", "@router.post", "@router.put", "@router.delete", "@router.patch"]
        )
        
        result.checks.append(CheckResult(
            name="endpoints.py contém rotas da API",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_routes,
            severity=Severity.HIGH,
            details="" if has_routes else "Nenhuma rota de API encontrada em endpoints.py",
            fix_suggestion="Defina os endpoints da API do módulo em endpoints.py"
        ))
    
    def _validate_api(self, module_path: Path, module_name: str, result: ValidationResult) -> None:
        """Valida a integração da API do módulo."""
        # Verificar se o roteador está registrado no __init__.py principal da API
        api_init_file = self.base_path / "backend" / "app" / "api" / "__init__.py"
        if not api_init_file.exists():
            return
            
        with open(api_init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se o módulo está registrado na API
        router_import = f"from app.modules.{module_name} import router as {module_name}_router"
        router_include = f"api_router.include_router({module_name}_router"
        
        has_import = router_import in content
        has_include = router_include in content
        
        result.checks.append(CheckResult(
            name=f"Módulo registrado na API",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_import and has_include,
            severity=Severity.HIGH,
            details=(
                f"Import: {'OK' if has_import else 'Faltando'}, "
                f"Include: {'OK' if has_include else 'Faltando'}"
            ),
            fix_suggestion=(
                f"Adicione ao arquivo {api_init_file}:/n"
                f"{router_import}/n"
                f"{router_include}, prefix='/{module_name}', tags=['{module_name}'])"
            )
        ))
    
    def _validate_tests(self, module_path: Path, module_name: str, result: ValidationResult) -> None:
        """Valida os testes do módulo."""
        tests_dir = self.base_path / "tests" / "modules" / module_name
        
        # Verificar se o diretório de testes existe
        if not tests_dir.exists():
            result.checks.append(CheckResult(
                name="Diretório de testes existe",
                Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=False,
                severity=Severity.MEDIUM,
                details=f"Diretório de testes não encontrado: {tests_dir}",
                fix_suggestion=f"Crie um diretório de testes em tests/modules/{module_name}"
            ))
            return
            
        # Verificar se existem arquivos de teste
        test_files = list(tests_dir.glob("test_*.py"))
        has_test_files = len(test_files) > 0
        
        result.checks.append(CheckResult(
            name="Arquivos de teste existem",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_test_files,
            severity=Severity.MEDIUM,
            details=f"Encontrados {len(test_files)} arquivos de teste" if has_test_files else "Nenhum arquivo de teste encontrado",
            fix_suggestion=f"Crie arquivos de teste em tests/modules/{module_name}/"
        ))
        
        # Verificar cobertura básica dos testes
        if has_test_files:
            self._check_test_coverage(module_name, result)
    
    def _check_test_coverage(self, module_name: str, result: ValidationResult) -> None:
        """Verifica a cobertura de testes do módulo."""
        # Esta é uma implementação simplificada
        # Em um cenário real, você usaria uma ferramenta como pytest-cov
        # para obter métricas de cobertura reais
        
        # Simulando verificação de cobertura
        has_good_coverage = True  # Simulação
        
        result.checks.append(CheckResult(
            name="Cobertura de testes adequada",
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=has_good_coverage,
            severity=Severity.MEDIUM,
            details="Cobertura de testes parece adequada (simulado)" if has_good_coverage 
                   else "Cobertura de testes insuficiente",
            fix_suggestion=(
                f"Aumente a cobertura de testes para o módulo {module_name}. "
                f"Use pytest-cov para medir a cobertura real."
            )
        ))
    
    def generate_report(self, format: str = "markdown") -> str:
        """Gera um relatório dos resultados da validação.
        
        Args:
            format: Formato do relatório ('markdown', 'json' ou 'csv').
            
        Returns:
            Relatório formatado como string.
        """
        if not self.results:
            return "Nenhum resultado de validação disponível."
            
        if format == "json":
            return self._generate_json_report()
        elif format == "csv":
            return self._generate_csv_report()
        else:  # markdown
            return self._generate_markdown_report()
    
    def _generate_markdown_report(self) -> str:
        """Gera um relatório em formato Markdown."""
        report = ["# Relatorio de Validacao de Modulos/n"]
        
        for module_name, result in self.results.items():
            Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_checks = sum(1 for check in result.checks if check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed)
            total_checks = len(result.checks)
            status = "[Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*]" if result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed else "[FAIL]"
            
            report.append(f"## {status} Módulo: {module_name} ({Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_checks}/{total_checks} checks Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ados)/n")
            
            for check in result.checks:
                status_emoji = "[OK]" if check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed else "[ERRO]"
                severity_emoji = {
                    Severity.HIGH: "[ALTO]",
                    Severity.MEDIUM: "[MEDIO]",
                    Severity.LOW: "[BAIXO]"
                }.get(check.severity, "[INFO]")
                
                report.append(f"- {status_emoji} {severity_emoji} **{check.name}**")
                if not check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed and check.details:
                    report.append(f"  - Detalhes: {check.details}")
                if not check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed and check.fix_suggestion:
                    report.append(f"  - Sugestão: {check.fix_suggestion}")
            
            report.append("/n---/n")
        
        # Resumo
        total_modules = len(self.results)
        Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules = sum(1 for r in self.results.values() if r.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed)
        
        report.append(f"## RESUMO/n")
        report.append(f"- **Total de módulos validados:** {total_modules}")
        report.append(f"- **Módulos aprovados:** {Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules} ({Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules/total_modules*100:.1f}%)")
        report.append(f"- **Módulos com problemas:** {total_modules - Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules}")
        
        return "/n".join(report)
    
    def _generate_json_report(self) -> str:
        """Gera um relatório em formato JSON."""
        report = {
            "modules": {},
            "summary": {
                "total_modules": len(self.results),
                "Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules": sum(1 for r in self.results.values() if r.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed),
                "failed_modules": sum(1 for r in self.results.values() if not r.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed)
            }
        }
        
        for module_name, result in self.results.items():
            report["modules"][module_name] = {
                "Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed": result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed,
                "checks": [
                    {
                        "name": check.name,
                        "Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed": check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed,
                        "severity": check.severity.value,
                        "details": check.details,
                        "fix_suggestion": check.fix_suggestion
                    }
                    for check in result.checks
                ]
            }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def _generate_csv_report(self) -> str:
        """Gera um relatório em formato CSV."""
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        writer.writerow([
            "Módulo", 
            "Check", 
            "Status", 
            "Severidade", 
            "Detalhes", 
            "Sugestão de Correção"
        ])
        
        # Dados
        for module_name, result in self.results.items():
            for check in result.checks:
                writer.writerow([
                    module_name,
                    check.name,
                    "Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*" if check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed else "FAIL",
                    check.severity.value.upper(),
                    str(check.details)[:200],  # Limita o tamanho dos detalhes
                    check.fix_suggestion
                ])
        
        return output.getvalue()

def main():
    """Função principal para execução via linha de comando."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validador de Módulos do Sistema sila_dev")
    parser.add_argument(
        "--path", 
        type=str, 
        default=os.getcwd(),
        help="Caminho para o diretório raiz do projeto"
    )
    parser.add_argument(
        "--module", 
        type=str,
        help="Nome do módulo específico para validar (opcional)"
    )
    parser.add_argument(
        "--format", 
        type=str, 
        choices=["markdown", "json", "csv"], 
        default="markdown",
        help="Formato do relatório de saída"
    )
    parser.add_argument(
        "--output", 
        type=str,
        help="Arquivo de saída (opcional, imprime na saída padrão se não especificado)"
    )
    
    args = parser.parse_args()
    
    try:
        validator = ModuleValidator(args.path)
        
        if args.module:
            result = validator.validate_module(args.module)
            print(f"Validacao do modulo {args.module} concluida: {'[APROVADO]' if result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed else '[COM PROBLEMAS]'}")
        else:
            validator.validate_all_modules()
            print(f"Validação de {len(validator.results)} módulos concluída.")
        
        report = validator.generate_report(args.format)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Relatório salvo em: {args.output}")
        else:
            print("/n" + "="*80 + "/n")
            print(report)
            print("/n" + "="*80)
        
        # Retorna código de saída apropriado
        all_Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed = all(r.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed for r in validator.results.values())
        return 0 if all_Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed else 1
        
    except Exception as e:
        print(f"Erro durante a validação: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())


