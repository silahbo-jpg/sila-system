#!/usr/bin/env python3
# scripts/batch_generate_services.py
# Gera múltiplos serviços em lote para diferentes módulos

import subprocess
import argparse
import csv
import os
from pathlib import Path

# Lista padrão de serviços para geração em lote
DEFAULT_SERVICES = [
    ("citizenship", "EmissaoBI"),
    ("citizenship", "AtualizacaoEndereco"),
    ("health", "AgendamentoConsulta"),
    ("health", "SolicitacaoExame"),
    ("education", "MatriculaEscolar"),
    ("commercial", "AberturaProcesso"),
    ("urbanism", "LicencaConstrucao"),
]

def generate_from_list(services_list):
    """Gera serviços a partir de uma lista de tuplas (módulo, serviço)"""
    print(f"[INICIO] Iniciando geração em lote de {len(services_list)} serviços...\n")
    
    success_count = 0
    failed_count = 0
    failed_services = []
    
    for i, (module, service) in enumerate(services_list, 1):
        print(f"[{i}/{len(services_list)}] Gerando {service} no módulo {module}...")
        
        result = subprocess.run(
            ["python", "scripts/generate_service.py", module, service],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[OK] {service} gerado com sucesso!")
            success_count += 1
        else:
            print(f"[ERRO] Falha ao gerar {service}: {result.stderr.strip()}")
            failed_count += 1
            failed_services.append((module, service))
        
        print("-" * 50)
    
    print(f"\n[RESUMO] Resumo da geração em lote:")
    print(f"   [OK] {success_count} serviços gerados com sucesso")
    print(f"   [ERRO] {failed_count} serviços falharam")
    
    if failed_services:
        print("\n[AVISO] Serviços que falharam:")
        for module, service in failed_services:
            print(f"   - {module}: {service}")
    
    print("\n[SUCESSO] Processo de geração em lote concluído!")

def generate_from_csv(csv_file):
    """Gera serviços a partir de um arquivo CSV"""
    services_list = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Pular cabeçalho
            for row in reader:
                if len(row) >= 2:
                    module, service = row[0].strip(), row[1].strip()
                    services_list.append((module, service))
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo CSV: {str(e)}")
        return
    
    if not services_list:
        print("❌ Nenhum serviço encontrado no arquivo CSV.")
        return
    
    print(f"[INFO] Carregados {len(services_list)} serviços do arquivo CSV.")
    generate_from_list(services_list)

def create_sample_csv(output_file):
    """Cria um arquivo CSV de exemplo com serviços"""
    services = [
        ["Module", "Service", "Description"],
        ["citizenship", "EmissaoBI", "Emissão de Bilhete de Identidade"],
        ["citizenship", "AtualizacaoEndereco", "Atualização de Endereço"],
        ["health", "AgendamentoConsulta", "Agendamento de Consulta Médica"],
        ["health", "SolicitacaoExame", "Solicitação de Exame Laboratorial"],
        ["education", "MatriculaEscolar", "Matrícula Escolar"],
        ["commercial", "AberturaProcesso", "Abertura de Processo Comercial"],
        ["urbanism", "LicencaConstrucao", "Licença de Construção"],
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(services)
        print(f"[OK] Arquivo CSV de exemplo criado em: {output_file}")
    except Exception as e:
        print(f"[ERRO] Erro ao criar arquivo CSV de exemplo: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Gera múltiplos serviços em lote para diferentes módulos")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--default", action="store_true", help="Usar lista padrão de serviços")
    group.add_argument("--csv", type=str, help="Caminho para um arquivo CSV com lista de serviços")
    group.add_argument("--create-csv", type=str, help="Criar um arquivo CSV de exemplo")
    
    args = parser.parse_args()
    
    if args.create_csv:
        create_sample_csv(args.create_csv)
    elif args.csv:
        generate_from_csv(args.csv)
    else:  # default ou nenhum argumento
        generate_from_list(DEFAULT_SERVICES)

if __name__ == "__main__":
    main()
