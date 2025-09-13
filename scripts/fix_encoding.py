from pathlib import Path
import csv

csv_path = Path(__file__).resolve().parent.parent / "data" / "clientes.csv"

with open(csv_path, "w", encoding="utf-8", newline="") as f:  # UTF-8 puro, sem BOM
    writer = csv.writer(f)
    writer.writerow(["id", "nome", "email"])
    writer.writerow([1, "Ana", "ewander@gmail.com"])
    writer.writerow([2, "Bruno", "marcelo@gmail.com"])
    writer.writerow([3, "Carlos", "leandra@gmail.com"])
    writer.writerow([4, "João", "joao@vitronis.com"])  # contém "ã"

print(f"[✓] Arquivo gerado em UTF-8 (sem BOM): {csv_path}")
