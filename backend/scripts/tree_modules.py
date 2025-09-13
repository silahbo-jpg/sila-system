import os

# 🧹 Padrões a ignorar
IGNORED_NAMES = {
    '__pycache__', '.git', '.vscode', '.idea', 'node_modules', 'dist', 'build',
    '.cache', '.pytest_cache', '.venv', 'env', 'venv', 'docs/_build', 'docgen',
    'Thumbs.db', '.DS_Store', 'desktop.ini'
}
IGNORED_EXTENSIONS = {
    '.log', '.tmp', '.bak', '.swp', '.db', '.pyc'
}
IGNORED_FILES = {
    '.env', '.env.local', '.env.test', '.gitignore', '.gitattributes'
}

def format_size(size_bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def should_ignore(name):
    if name in IGNORED_NAMES or name in IGNORED_FILES:
        return True
    _, ext = os.path.splitext(name)
    return ext in IGNORED_EXTENSIONS

# Modificado para aceitar o argumento `file`
def print_tree(path, prefix="", file=None):
    total_size = 0
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}⚠️ Permissão negada: {path}", file=file)
        return 0

    filtered = [e for e in entries if not should_ignore(e)]
    for i, entry in enumerate(filtered):
        full_path = os.path.join(path, entry)
        connector = "└── " if i == len(filtered) - 1 else "├── "
        if os.path.isdir(full_path):
            print(f"{prefix}{connector}{entry}/", file=file)
            # Passa o `file` para a chamada recursiva
            size = print_tree(full_path, prefix + ("    " if i == len(filtered) - 1 else "│   "), file=file)
            total_size += size
        else:
            try:
                size = os.path.getsize(full_path)
                print(f"{prefix}{connector}{entry} ({format_size(size)})", file=file)
                total_size += size
            except OSError:
                print(f"{prefix}{connector}{entry} ⚠️ [Erro ao obter tamanho]", file=file)
    return total_size

if __name__ == "__main__":
    root_folder = os.path.join("backend", "app", "modules")
    output_dir = "reports"
    output_file = os.path.join(output_dir, "modules_tree_report.txt")

    # Garante que o diretório 'reports' existe
    os.makedirs(output_dir, exist_ok=True)

    # Abre o arquivo para escrita, redirecionando a saída
    with open(output_file, 'w', encoding='utf-8') as f:
        print(f"\n📁 Estrutura de: {root_folder}/\n", file=f)
        total = print_tree(root_folder, file=f)
        print(f"\n📦 Tamanho total (curado): {format_size(total)}", file=f)

    print(f"✅ Árvore de diretórios gerada e salva em: {output_file}")