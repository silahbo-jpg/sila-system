import os

# Define the path to the script
script_path = r"C:\\Users\\User5\\Music\\MEGA1\\sila\\sila-system\\scripts\\validate_and_fix_models.py"

try:
    # Read the original script
    with open(script_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Replace the emoji line and remove any other emojis or special characters
    sanitized_lines = []
    for line in lines:
        if "\U0001f4cb" in line:
            sanitized_lines.append("print(\"[Resumo] Validação e correção de modelos:\")\n")
        else:
            # Remove any non-ASCII characters to ensure cp1252 compatibility
            sanitized_line = ''.join(char for char in line if ord(char) < 128)
            sanitized_lines.append(sanitized_line)

    # Write the sanitized script back
    with open(script_path, "w", encoding="utf-8") as file:
        file.writelines(sanitized_lines)

    print("Script sanitized successfully: validate_and_fix_models.py")
except Exception as e:
    print(f"Error sanitizing script: {e}")
