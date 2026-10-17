from datetime import date
from pathlib import Path
import requests
from sources import SEMANAL_URL, SOURCES

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

for nome, url in SOURCES.items():
    destino = RAW_DIR / f"{nome}.csv"

    if destino.exists():
        print(f"já existe, pulando: {destino}")
        continue

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    destino.write_bytes(response.content)
    print(f"baixado: {destino} ({len(response.content) / 1_000_000:.1f} MB)")

destino_semanal = RAW_DIR / f"ultimas-4-semanas_{date.today().isoformat()}.csv"

if destino_semanal.exists():
    print(f"já existe, pulando: {destino_semanal}")
else:
    response = requests.get(SEMANAL_URL, timeout=60)
    response.raise_for_status()
    destino_semanal.write_bytes(response.content)
    print(f"baixado: {destino_semanal} ({len(response.content) / 1_000_000:.1f} MB)")