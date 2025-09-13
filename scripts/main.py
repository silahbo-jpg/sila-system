import click

@click.group()
def cli():
    """SILA-System Tools"""
    pass

@cli.command()
def create_superuser():
    """Create a superuser for the system"""
    from scripts.dev.create_superuser import main
    main()

@cli.command()
def run_tests():
    """Run the test suite"""
    from scripts.ci.run_tests import run
    run()

@cli.command()
def tree_modules():
    """Show the modules tree structure"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "utils_new"))
    from tree_modules import show
    show()

@cli.command()
def setup_database():
    """Set up the database"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "db_new"))
    from setup_database import main
    main()

@cli.command()
def check_connection():
    """Check database connection"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "db_new"))
    from check_connection import main
    main()

@cli.command()
def audit_secrets():
    """Audit secrets and credentials"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "audit_new"))
    from audit_secrets import main
    main()

@cli.command()
def validate_env():
    """Validate environment configuration"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "audit_new"))
    from validate_env import main
    main()

@cli.command()
def fix_imports():
    """Fix and standardize imports"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "utils_new"))
    from fix_imports import main
    main()

@cli.command()
def diagnose_modules():
    """Identify modules with routers and check registration status"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "utils_new"))
    from diagnose_modules import main
    main()

@cli.command()
def auto_register_modules():
    """Automatically register missing modules in the API router"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "utils_new"))
    from auto_register_modules import main
    main()

@cli.command()
def validate_auth():
    """Validate authentication flow end-to-end"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "utils_new"))
    from validate_auth import main
    main()

@cli.command()
@click.option('--module', help='Module name')
@click.option('--service', help='Service name')
@click.option('--from-version', default='v1', help='Source version')
@click.option('--to-version', required=True, help='Target version')
@click.option('--list-only', is_flag=True, help='List services only')
@click.option('--generate-docs', help='Generate docs for version')
def version_service(module, service, from_version, to_version, list_only, generate_docs):
    """Version services and manage API versions"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    
    args = ['version_service.py']
    
    if list_only:
        args.append('list')
        if module:
            args.extend(['--module', module])
    elif generate_docs:
        args.extend(['docs', generate_docs])
    elif module and service:
        args.extend(['version', module, service])
        args.extend(['--from', from_version, '--to', to_version])
    elif module:
        args.extend(['version-module', module])
        args.extend(['--from', from_version, '--to', to_version])
    else:
        click.echo("❌ Please specify --module and optionally --service, or use --list-only")
        return
    
    # Execute version service script
    original_argv = sys.argv
    sys.argv = args
    
    try:
        from version_service import main
        main()
    finally:
        sys.argv = original_argv

@cli.command()
@click.option('--from-csv', 'csv_file', help='Generate translations from CSV file')
@click.option('--update', nargs=3, metavar='LANG KEY VALUE', help='Update single translation')
@click.option('--validate', is_flag=True, help='Validate translation completeness')
@click.option('--export', 'export_file', help='Export translations for translators')
def update_translations(csv_file, update, validate, export_file):
    """Manage i18n translations for all services"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    
    args = ['update_translations.py']
    
    if csv_file:
        args.extend(['from-csv', csv_file])
    elif update:
        lang, key, value = update
        args.extend(['update', lang, key, value])
    elif validate:
        args.append('validate')
    elif export_file:
        args.extend(['export', export_file])
    else:
        click.echo("❌ Please specify --from-csv, --update, --validate, or --export")
        return
    
    # Execute translation script
    original_argv = sys.argv
    sys.argv = args
    
    try:
        from update_translations import main
        main()
    finally:
        sys.argv = original_argv

@cli.command()
@click.option('--module', required=True, help='Module name')
@click.option('--service', required=True, help='Service name')
@click.option('--config', help='JSON file with approval configuration')
@click.option('--list', 'list_configs', is_flag=True, help='List all approval configurations')
@click.option('--remove', is_flag=True, help='Remove approval requirement')
@click.option('--create-presets', is_flag=True, help='Create preset configurations')
@click.option('--report', is_flag=True, help='Generate approval report')
def set_approval_level(module, service, config, list_configs, remove, create_presets, report):
    """Set approval levels for services"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    
    args = ['set_approval_level.py']
    
    if list_configs:
        args.append('list')
    elif create_presets:
        args.append('create-presets')
    elif report:
        args.append('report')
    elif remove:
        args.extend(['remove', module, service])
    elif config:
        args.extend(['set', module, service, '--config', config])
    else:
        click.echo("❌ Please specify --config, --list, --remove, --create-presets, or --report")
        return
    
    # Execute approval level script
    original_argv = sys.argv
    sys.argv = args
    
    try:
        from set_approval_level import main
        main()
    finally:
        sys.argv = original_argv

@cli.command()
@click.option('--email', help='Login email for testing')
@click.option('--password', help='Login password for testing')
@click.option('--skip-auth', is_flag=True, help='Skip authentication validation')
@click.option('--generate-ci', is_flag=True, help='Generate CI/CD integration script')
def production_fix(email, password, skip_auth, generate_ci):
    """Run complete production fix (diagnose + auto-register + validate)"""
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "utils_new"))
    
    # Prepare arguments
    args = ['production_fix']
    if email:
        args.extend(['--email', email])
    if password:
        args.extend(['--password', password])
    if skip_auth:
        args.append('--skip-auth')
    if generate_ci:
        args.append('--generate-ci')
    
    # Temporarily replace sys.argv
    original_argv = sys.argv
    sys.argv = args
    
    try:
        from production_fix import main
        main()
    finally:
        sys.argv = original_argv

if __name__ == "__main__":
    cli()