import os
import pathlib

def corrigir_strings_na_linha_1(base_dir):
    # Criar diretório de logs se não existir
    logs_dir = pathlib.Path("logs")
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / "correcoes_strings.txt"
    
    correcoes_count = 0
    
    for sila_dev-system, _, files in os.walk(base_dir):
        for file in files:
            if file == "__init__.py":
                path = os.path.join(sila_dev-system, file)
                
                # Ignorar arquivos em .venv ou site-packages
                if ".venv" in path or "site-packages" in path:
                    continue
                    
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    
                    # Validação melhorada de docstring real
                    if lines and lines[0].strip().startswith('"') and lines[0].count('"') == 1:
                        lines[0] = lines[0].strip() + '"\n'
                        with open(path, "w", encoding="utf-8") as f:
                            f.writelines(lines)
                        
                        # Registrar correção no log
                        with open(log_file, "a", encoding="utf-8") as log:
                            log.write(f"{path}\n")
                            
                        print(f"✅ Corrigido: {path}")
                        correcoes_count += 1
                except Exception as e:
                    print(f"⚠️ Erro em {path}: {e}")

    return correcoes_count

if __name__ == "__main__":
    print("Iniciando correção de strings não terminadas em arquivos __init__.py...")
    total_correcoes = corrigir_strings_na_linha_1("backend")
    print(f"Processo concluído! {total_correcoes} arquivo(s) corrigido(s).")
    print(f"Log de correções salvo em logs/correcoes_strings.txt")

