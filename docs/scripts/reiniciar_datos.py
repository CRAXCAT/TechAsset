"""Reinicia los datos de demostración de TechAsset conservando el administrador."""
import os
import subprocess
import sys
from pathlib import Path

PSQL = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
SQL = (
    'DELETE FROM "Movimientos"; '
    'DELETE FROM "Solicitudes"; '
    'DELETE FROM "Prestamos"; '
    'DELETE FROM "Equipos"; '
    'DELETE FROM "Usuarios" WHERE "Correo" <> \'admin@innovatech.pe\';'
)

BASE = Path(__file__).resolve().parent


def main():
    entorno = os.environ.copy()
    entorno["PGPASSWORD"] = "postgres"
    subprocess.run(
        [PSQL, "-U", "postgres", "-h", "localhost", "-d", "TechAssetDB", "-c", SQL],
        check=True,
        env=entorno,
    )
    subprocess.run([sys.executable, str(BASE / "seed.py")], check=True)


if __name__ == "__main__":
    main()
