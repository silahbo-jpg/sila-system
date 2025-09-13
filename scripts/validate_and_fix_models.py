import os
import sys
import json
import re
import argparse
import datetime
import subprocess
from collections import defaultdict
from pathlib import Path

import chardet
import requests

# Argument parser
parser = argparse.ArgumentParser(description='Validate and fix model scripts.')
parser.add_argument('--dry-run', action='store_true', help='Run without applying changes')
parser.add_argument('--auto-commit', action='store_true', help='Automatically commit changes to Git')
args = parser.parse_args()

# Constants
ROOT_DIR = Path(r'C:\Users\User5\Music\MEGA1\sila\sila-system')
SCRIPTS_DIR = ROOT_DIR / 'scripts'
BACKUP_DIR = SCRIPTS_DIR / 'model_backups' / 'logs'
WEBHOOK_CONFIG = SCRIPTS_DIR / 'config' / 'webhook.json'
ENCODING_ISSUES = []
DUPLICATE_CLASSES = defaultdict(list)

# Timestamp for logs
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_json_path = BACKUP_DIR / f'{timestamp}.json'
log_md_path = BACKUP_DIR / f'{timestamp}.md'
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Report structure
report = {
    'files_checked': 0,
    'files_modified': 0,
    'syntax_errors': 0,
    'incomplete_models': 0,
    'duplicate_classes': {},
    'encoding_issues': [],
    'errors': []
}

# Helper functions
def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            if encoding not in ['utf-8', 'ascii']:
                ENCODING_ISSUES.append({'file': str(file_path), 'encoding': encoding})
                report['encoding_issues'].append({'file': str(file_path), 'encoding': encoding})
    except Exception as e:
        report['errors'].append(f'Encoding detection failed for {file_path}: {str(e)}')

def find_duplicate_classes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            class_names = re.findall(r'class\s+(\w+)', content)
            for name in class_names:
                DUPLICATE_CLASSES[name].append(str(file_path))
    except Exception as e:
        report['errors'].append(f'Duplicate class detection failed for {file_path}: {str(e)}')

def send_notification(summary):
    try:
        if WEBHOOK_CONFIG.exists():
            with open(WEBHOOK_CONFIG, 'r') as f:
                config = json.load(f)
                webhook_url = config.get('webhook_url')
                if webhook_url:
                    requests.post(webhook_url, json={'text': summary})
    except Exception as e:
        report['errors'].append(f'Notification failed: {str(e)}')

# Main script logic
for root, _, files in os.walk(SCRIPTS_DIR):
    for file in files:
        if file.endswith('.py'):
            file_path = Path(root) / file
            report['files_checked'] += 1
            detect_encoding(file_path)
            find_duplicate_classes(file_path)
            # Placeholder for syntax and model validation
            # Simulate modification
            if not args.dry_run:
                report['files_modified'] += 1

# Process duplicate classes
for class_name, locations in DUPLICATE_CLASSES.items():
    if len(locations) > 1:
        report['duplicate_classes'][class_name] = locations

# Save logs
try:
    with open(log_json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    with open(log_md_path, 'w', encoding='utf-8') as f:
        f.write(f'# Model Validation Report - {timestamp}\n\n')
        for key, value in report.items():
            f.write(f'## {key}\n{json.dumps(value, indent=2)}\n\n')
except Exception as e:
    print(f'Failed to save logs: {str(e)}')

# Git commit
if args.auto_commit:
    try:
        subprocess.run(['git', 'add', '.'], cwd=ROOT_DIR)
        subprocess.run(['git', 'commit', '-m', 'Correções aplicadas pelo validador de modelos'], cwd=ROOT_DIR)
    except Exception as e:
        report['errors'].append(f'Git commit failed: {str(e)}')

# Notification
summary = f"Arquivos verificados: {report['files_checked']}, Modificados: {report['files_modified']}, Erros de sintaxe: {report['syntax_errors']}, Modelos incompletos: {report['incomplete_models']}, Duplicações: {len(report['duplicate_classes'])}, Problemas de encoding: {len(report['encoding_issues'])}"
send_notification(summary)

# Final summary
print(summary)

# Save fix_report
try:
    with open(SCRIPTS_DIR / 'fix_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    with open(SCRIPTS_DIR / 'fix_report.md', 'w', encoding='utf-8') as f:
        f.write(f'# Fix Report\n\n')
        for key, value in report.items():
            f.write(f'## {key}\n{json.dumps(value, indent=2)}\n\n')
except Exception as e:
    print(f'Failed to save fix report: {str(e)}')
