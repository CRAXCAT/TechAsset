"""Comprueba restricciones físicas de PostgreSQL con transacciones revertidas."""
import json
import os
import subprocess
from pathlib import Path

PSQL = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
BASE = Path(__file__).resolve().parents[1]
SALIDA = BASE / "pruebas-integridad.json"

CHECKS = [
    (
        "DB-01",
        "Segundo préstamo activo para el mismo equipo",
        """
        INSERT INTO "Prestamos" ("Id","FechaPrestamo","FechaDevolucion","Observacion","Estado","UsuarioId","EquipoId","ResponsableId","FechaRegistro")
        SELECT gen_random_uuid(), CURRENT_DATE + 1, CURRENT_DATE + 3, 'Duplicado de prueba', 'Activo',
               (SELECT "Id" FROM "Usuarios" WHERE "Correo"='ana.torres@innovatech.pe'),
               e."Id",
               (SELECT "Id" FROM "Usuarios" WHERE "Correo"='admin@innovatech.pe'),
               now()
        FROM "Equipos" e
        WHERE e."CodigoPatrimonial"='TA-0001';
        """,
        "IX_Prestamos_EquipoActivo",
    ),
    (
        "DB-02",
        "Estado de equipo fuera del catálogo",
        """UPDATE "Equipos" SET "Estado"='Roto' WHERE "CodigoPatrimonial"='TA-0002';""",
        "CK_Equipos_Estado",
    ),
    (
        "DB-03",
        "Rol de usuario fuera del catálogo",
        """UPDATE "Usuarios" SET "Rol"='Superusuario' WHERE "Correo"='rosa.quispe@innovatech.pe';""",
        "CK_Usuarios_Rol",
    ),
    (
        "DB-04",
        "Préstamo con devolución anterior al préstamo",
        """
        INSERT INTO "Prestamos" ("Id","FechaPrestamo","FechaDevolucion","Observacion","Estado","UsuarioId","EquipoId","ResponsableId","FechaRegistro")
        SELECT gen_random_uuid(), CURRENT_DATE + 2, CURRENT_DATE + 2, 'Fechas invalidas de prueba', 'Activo',
               (SELECT "Id" FROM "Usuarios" WHERE "Correo"='ana.torres@innovatech.pe'),
               e."Id",
               (SELECT "Id" FROM "Usuarios" WHERE "Correo"='admin@innovatech.pe'),
               now()
        FROM "Equipos" e
        WHERE e."CodigoPatrimonial"='TA-0002';
        """,
        "CK_Prestamos_Fechas",
    ),
    (
        "DB-05",
        "Solicitud aprobada sin préstamo vinculado",
        """
        INSERT INTO "Solicitudes" ("Id","FechaPrestamo","FechaDevolucion","Motivo","Estado","UsuarioId","EquipoId","FechaRegistro")
        SELECT gen_random_uuid(), CURRENT_DATE + 1, CURRENT_DATE + 4, 'Aprobacion invalida de prueba', 'Aprobada',
               (SELECT "Id" FROM "Usuarios" WHERE "Correo"='ana.torres@innovatech.pe'),
               e."Id", now()
        FROM "Equipos" e
        WHERE e."CodigoPatrimonial"='TA-0002';
        """,
        "CK_Solicitudes_Aprobacion",
    ),
    (
        "DB-06",
        "Solicitud pendiente con préstamo vinculado",
        """
        INSERT INTO "Solicitudes" ("Id","FechaPrestamo","FechaDevolucion","Motivo","Estado","UsuarioId","EquipoId","PrestamoId","FechaRegistro")
        SELECT gen_random_uuid(), CURRENT_DATE + 1, CURRENT_DATE + 4, 'Pendiente con prestamo de prueba', 'Pendiente',
               (SELECT "Id" FROM "Usuarios" WHERE "Correo"='ana.torres@innovatech.pe'),
               e."Id",
               (SELECT p."Id" FROM "Prestamos" p WHERE p."Estado"='Activo' LIMIT 1),
               now()
        FROM "Equipos" e
        WHERE e."CodigoPatrimonial"='TA-0004';
        """,
        "CK_Solicitudes_Aprobacion",
    ),
    (
        "DB-07",
        "Segunda solicitud pendiente para el mismo equipo",
        """
        INSERT INTO "Solicitudes" ("Id","FechaPrestamo","FechaDevolucion","Motivo","Estado","UsuarioId","EquipoId","FechaRegistro")
        SELECT gen_random_uuid(), CURRENT_DATE + 1, CURRENT_DATE + 4, 'Solicitud duplicada de prueba', 'Pendiente',
               (SELECT "Id" FROM "Usuarios" WHERE "Correo"='ana.torres@innovatech.pe'),
               e."Id", now()
        FROM "Equipos" e
        WHERE e."CodigoPatrimonial"='TA-0002';
        """,
        "IX_Solicitudes_EquipoPendiente",
    ),
    (
        "DB-08",
        "Estado de solicitud fuera del catálogo",
        """
        UPDATE "Solicitudes" SET "Estado"='EnRevision'
        WHERE "Id"=(SELECT "Id" FROM "Solicitudes" WHERE "Estado"='Pendiente' LIMIT 1);
        """,
        "CK_Solicitudes_Estado",
    ),
    (
        "DB-09",
        "Eliminar un equipo con préstamo activo",
        """DELETE FROM "Equipos" WHERE "CodigoPatrimonial"='TA-0001';""",
        "FK_Prestamos_Equipos_EquipoId",
    ),
    (
        "DB-10",
        "Eliminar un usuario con préstamos",
        """DELETE FROM "Usuarios" WHERE "Correo"='ana.torres@innovatech.pe';""",
        "FK_Prestamos_Usuarios_UsuarioId",
    ),
    (
        "DB-11",
        "Eliminar un usuario con solicitudes",
        """DELETE FROM "Usuarios" WHERE "Correo"='rosa.quispe@innovatech.pe';""",
        "FK_Solicitudes_Usuarios_UsuarioId",
    ),
    (
        "DB-12",
        "Eliminar un equipo con solicitudes",
        """DELETE FROM "Equipos" WHERE "CodigoPatrimonial"='TA-0002';""",
        "FK_Solicitudes_Equipos_EquipoId",
    ),
]


def main():
    entorno = os.environ.copy()
    entorno["PGPASSWORD"] = "postgres"
    entorno["PGCLIENTENCODING"] = "UTF8"

    resultados = []
    for codigo, escenario, sql, restriccion in CHECKS:
        script = "BEGIN;\n" + sql + "\nROLLBACK;\n"
        proceso = subprocess.run(
            [PSQL, "-U", "postgres", "-h", "localhost", "-d", "TechAssetDB", "-v", "ON_ERROR_STOP=1", "-c", script],
            env=entorno,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        salida = (proceso.stdout + "\n" + proceso.stderr).strip()
        rechazado = proceso.returncode != 0
        detalle = next((linea.strip() for linea in salida.splitlines() if "ERROR" in linea or "error" in linea), salida.splitlines()[0] if salida else "")
        resultados.append(
            {
                "codigo": codigo,
                "escenario": escenario,
                "restriccion": restriccion,
                "rechazado": rechazado,
                "detalle": detalle[:220],
            }
        )
        print(f"{'OK ' if rechazado else 'FALLA'} {codigo} · {restriccion} · {detalle[:100]}")

    conformes = sum(1 for r in resultados if r["rechazado"])
    SALIDA.write_text(
        json.dumps({"resultados": resultados, "conformes": conformes, "total": len(resultados)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nResultado: {conformes}/{len(resultados)} restricciones rechazaron la operación inválida")


if __name__ == "__main__":
    main()
