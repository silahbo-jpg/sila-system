#!/usr/bin/env python3
"""
Translation Management CLI Tool

This script automates translation management for the SILA system:
- Convert CSV service definitions to i18n JSON files
- Generate translation keys for all 150 services
- Manage translation updates and synchronization
"""

import csv
import json
import argparse
from pathlib import Path
from typing import Dict, Any
import sys

class TranslationGenerator:
    """Generates and manages translations for SILA services"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.i18n_dir = base_dir / "backend" / "app" / "i18n"
        self.i18n_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_from_csv(self, csv_file: Path):
        """
        Generate translation files from the services CSV
        
        Creates structured JSON translations for all services in both
        Portuguese and English, following the directive requirements.
        """
        print(f"🌐 Generating translations from CSV: {csv_file}")
        
        # Initialize translation structures
        translations = {
            'pt': {
                'services': {},
                'modules': {},
                'common': {
                    'actions': {
                        'create': 'Criar',
                        'read': 'Ver',
                        'update': 'Atualizar', 
                        'delete': 'Excluir',
                        'list': 'Listar',
                        'search': 'Pesquisar'
                    },
                    'status': {
                        'active': 'Ativo',
                        'inactive': 'Inativo',
                        'pending': 'Pendente',
                        'approved': 'Aprovado',
                        'rejected': 'Rejeitado'
                    },
                    'messages': {
                        'success': 'Operação realizada com sucesso',
                        'error': 'Erro ao processar solicitação',
                        'not_found': 'Recurso não encontrado',
                        'unauthorized': 'Não autorizado',
                        'validation_error': 'Erro de validação'
                    }
                }
            },
            'en': {
                'services': {},
                'modules': {},
                'common': {
                    'actions': {
                        'create': 'Create',
                        'read': 'View',
                        'update': 'Update',
                        'delete': 'Delete', 
                        'list': 'List',
                        'search': 'Search'
                    },
                    'status': {
                        'active': 'Active',
                        'inactive': 'Inactive',
                        'pending': 'Pending',
                        'approved': 'Approved',
                        'rejected': 'Rejected'
                    },
                    'messages': {
                        'success': 'Operation completed successfully',
                        'error': 'Error processing request',
                        'not_found': 'Resource not found',
                        'unauthorized': 'Unauthorized',
                        'validation_error': 'Validation error'
                    }
                }
            }
        }
        
        # Module descriptions
        module_descriptions = {
            'health': ('Serviços de Saúde', 'Health Services'),
            'education': ('Serviços de Educação', 'Education Services'),
            'citizenship': ('Serviços de Cidadania', 'Citizenship Services'),
            'finance': ('Serviços Financeiros', 'Financial Services'),
            'urbanism': ('Serviços de Urbanismo', 'Urban Planning Services'),
            'justice': ('Serviços de Justiça', 'Justice Services'),
            'social': ('Serviços Sociais', 'Social Services'),
            'complaints': ('Ouvidoria e Reclamações', 'Complaints and Ombudsman'),
            'commercial': ('Serviços Comerciais', 'Commercial Services'),
            'sanitation': ('Serviços de Saneamento', 'Sanitation Services'),
            'registry': ('Serviços de Registro', 'Registry Services'),
            'service_hub': ('Centro de Serviços', 'Service Hub'),
            'auth': ('Autenticação', 'Authentication'),
            'common': ('Serviços Comuns', 'Common Services'),
            'governance': ('Governança', 'Governance'),
            'integration': ('Integração', 'Integration'),
            'internal': ('Serviços Internos', 'Internal Services'),
            'statistics': ('Estatísticas', 'Statistics'),
            'documents': ('Documentos', 'Documents'),
            'address': ('Endereços', 'Addresses')
        }
        
        # Add module translations
        for module, (pt_name, en_name) in module_descriptions.items():
            translations['pt']['modules'][module] = {
                'name': pt_name,
                'description': f'Módulo responsável por {pt_name.lower()}'
            }
            translations['en']['modules'][module] = {
                'name': en_name,
                'description': f'Module responsible for {en_name.lower()}'
            }
        
        # Parse CSV and generate service translations
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                services_count = {'citizen': 0, 'internal': 0}
                
                for row in reader:
                    # Skip comment lines
                    if row['module'].startswith('#'):
                        continue
                        
                    module = row['module'].strip()
                    service_key = row['service_key'].strip()
                    name_pt = row['service_name_pt'].strip()
                    name_en = row['service_name_en'].strip()
                    service_type = row.get('service_type', 'citizen').strip()
                    
                    # Count services
                    services_count[service_type] += 1
                    
                    # Generate service slug for URLs
                    service_slug = ''.join(['_'+c.lower() if c.isupper() else c for c in service_key]).lstrip('_')\n                    api_slug = service_slug.replace('_', '-')\n                    \n                    # Add to translations\n                    if module not in translations['pt']['services']:\n                        translations['pt']['services'][module] = {}\n                        translations['en']['services'][module] = {}\n                        \n                    translations['pt']['services'][module][service_key] = {\n                        'name': name_pt,\n                        'slug': api_slug,\n                        'type': service_type,\n                        'description': f'Serviço de {name_pt.lower()}',\n                        'endpoints': {\n                            'list': f'Listar {name_pt}',\n                            'create': f'Criar {name_pt}',\n                            'get': f'Obter {name_pt}',\n                            'update': f'Atualizar {name_pt}',\n                            'delete': f'Excluir {name_pt}'\n                        }\n                    }\n                    \n                    translations['en']['services'][module][service_key] = {\n                        'name': name_en,\n                        'slug': api_slug,\n                        'type': service_type,\n                        'description': f'{name_en} service',\n                        'endpoints': {\n                            'list': f'List {name_en}',\n                            'create': f'Create {name_en}',\n                            'get': f'Get {name_en}',\n                            'update': f'Update {name_en}',\n                            'delete': f'Delete {name_en}'\n                        }\n                    }\n                    \n        except Exception as e:\n            print(f\"❌ Error reading CSV: {str(e)}\")\n            return False\n            \n        # Save translation files\n        for lang, data in translations.items():\n            translation_file = self.i18n_dir / f\"{lang}.json\"\n            try:\n                with open(translation_file, 'w', encoding='utf-8') as f:\n                    json.dump(data, f, ensure_ascii=False, indent=2)\n                print(f\"✅ Generated {lang}.json with {len(data['services'])} modules\")\n            except Exception as e:\n                print(f\"❌ Error saving {lang}.json: {str(e)}\")\n                return False\n                \n        # Generate summary\n        print(f\"\\n📊 Translation Summary:\")\n        print(f\"   • Total modules: {len(translations['pt']['services'])}\")\n        print(f\"   • Citizen services: {services_count['citizen']}\")\n        print(f\"   • Internal services: {services_count['internal']}\")\n        print(f\"   • Total services: {services_count['citizen'] + services_count['internal']}\")\n        print(f\"   • Languages: Portuguese, English\")\n        print(f\"   • Output directory: {self.i18n_dir}\")\n        \n        return True\n        \n    def update_translation(self, lang: str, key: str, value: str):\n        \"\"\"Update a specific translation key\"\"\"\n        translation_file = self.i18n_dir / f\"{lang}.json\"\n        \n        # Load existing translations\n        translations = {}\n        if translation_file.exists():\n            with open(translation_file, 'r', encoding='utf-8') as f:\n                translations = json.load(f)\n                \n        # Update the key (supporting dot notation)\n        keys = key.split('.')\n        current = translations\n        for k in keys[:-1]:\n            current = current.setdefault(k, {})\n        current[keys[-1]] = value\n        \n        # Save updated translations\n        with open(translation_file, 'w', encoding='utf-8') as f:\n            json.dump(translations, f, ensure_ascii=False, indent=2)\n            \n        print(f\"✅ Updated {lang}.json: {key} = {value}\")\n        \n    def validate_translations(self):\n        \"\"\"Validate translation completeness and consistency\"\"\"\n        print(\"🔍 Validating translations...\")\n        \n        issues = []\n        \n        # Check if all language files exist\n        for lang in ['pt', 'en']:\n            translation_file = self.i18n_dir / f\"{lang}.json\"\n            if not translation_file.exists():\n                issues.append(f\"Missing translation file: {lang}.json\")\n                continue\n                \n            # Load and validate structure\n            try:\n                with open(translation_file, 'r', encoding='utf-8') as f:\n                    data = json.load(f)\n                    \n                # Check required sections\n                required_sections = ['services', 'modules', 'common']\n                for section in required_sections:\n                    if section not in data:\n                        issues.append(f\"{lang}.json missing section: {section}\")\n                        \n            except Exception as e:\n                issues.append(f\"Error reading {lang}.json: {str(e)}\")\n                \n        if issues:\n            print(f\"❌ Validation failed:\")\n            for issue in issues:\n                print(f\"   • {issue}\")\n            return False\n        else:\n            print(f\"✅ All translations valid\")\n            return True\n            \n    def export_for_translators(self, output_file: Path):\n        \"\"\"Export translations in a format suitable for translators\"\"\"\n        print(f\"📤 Exporting translations for translators: {output_file}\")\n        \n        # Load Portuguese (base) translations\n        pt_file = self.i18n_dir / \"pt.json\"\n        if not pt_file.exists():\n            print(f\"❌ Portuguese translations not found: {pt_file}\")\n            return False\n            \n        with open(pt_file, 'r', encoding='utf-8') as f:\n            pt_data = json.load(f)\n            \n        # Flatten translations for easier translation\n        flat_translations = []\n        \n        def flatten_dict(data, prefix=''):\n            for key, value in data.items():\n                new_key = f\"{prefix}.{key}\" if prefix else key\n                if isinstance(value, dict):\n                    flatten_dict(value, new_key)\n                else:\n                    flat_translations.append({\n                        'key': new_key,\n                        'portuguese': str(value),\n                        'english': '',  # To be filled by translator\n                        'context': prefix.split('.')[0] if '.' in prefix else 'general'\n                    })\n                    \n        flatten_dict(pt_data)\n        \n        # Save as CSV for translators\n        with open(output_file, 'w', newline='', encoding='utf-8') as f:\n            writer = csv.DictWriter(f, fieldnames=['key', 'context', 'portuguese', 'english'])\n            writer.writeheader()\n            writer.writerows(flat_translations)\n            \n        print(f\"✅ Exported {len(flat_translations)} translation keys\")\n        return True\n\ndef main():\n    parser = argparse.ArgumentParser(description=\"SILA Translation Management Tool\")\n    subparsers = parser.add_subparsers(dest='command', help='Available commands')\n    \n    # Generate from CSV\n    csv_parser = subparsers.add_parser('from-csv', help='Generate translations from services CSV')\n    csv_parser.add_argument('csv_file', help='Path to services CSV file')\n    \n    # Update single translation\n    update_parser = subparsers.add_parser('update', help='Update a single translation')\n    update_parser.add_argument('language', choices=['pt', 'en'], help='Language code')\n    update_parser.add_argument('key', help='Translation key (dot notation)')\n    update_parser.add_argument('value', help='Translation value')\n    \n    # Validate translations\n    validate_parser = subparsers.add_parser('validate', help='Validate translation completeness')\n    \n    # Export for translators\n    export_parser = subparsers.add_parser('export', help='Export translations for translators')\n    export_parser.add_argument('output_file', help='Output CSV file for translators')\n    \n    args = parser.parse_args()\n    \n    if not args.command:\n        parser.print_help()\n        return\n        \n    # Initialize generator\n    base_dir = Path(__file__).parent.parent\n    generator = TranslationGenerator(base_dir)\n    \n    try:\n        if args.command == 'from-csv':\n            csv_file = Path(args.csv_file)\n            if not csv_file.exists():\n                print(f\"❌ CSV file not found: {csv_file}\")\n                sys.exit(1)\n                \n            success = generator.generate_from_csv(csv_file)\n            sys.exit(0 if success else 1)\n            \n        elif args.command == 'update':\n            generator.update_translation(args.language, args.key, args.value)\n            \n        elif args.command == 'validate':\n            success = generator.validate_translations()\n            sys.exit(0 if success else 1)\n            \n        elif args.command == 'export':\n            output_file = Path(args.output_file)\n            success = generator.export_for_translators(output_file)\n            sys.exit(0 if success else 1)\n            \n    except Exception as e:\n        print(f\"❌ Error: {str(e)}\")\n        sys.exit(1)\n\nif __name__ == \"__main__\":\n    main()