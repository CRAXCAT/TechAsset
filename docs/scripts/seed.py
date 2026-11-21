"""Carga de datos de demostración de TechAsset."""
import json
import os
import subprocess
import urllib.error
import urllib.request
import uuid
from datetime import date, timedelta

BASE = "http://localhost:5143/api"
PSQL = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
ADMIN = ("admin@innovatech.pe", "Admin.2026*")

USUARIOS = [
    ("Kevin", "Ccente Garcia", "kevin.ccente@innovatech.pe", "Sistemas", "Administrador", "Tech.2026*"),
    ("Lucía", "Paredes Rojas", "lucia.paredes@innovatech.pe", "Sistemas", "Responsable", "Tech.2026*"),
    ("Pedro", "Ccahuana Flores", "pedro.ccahuana@innovatech.pe", "Soporte", "Responsable", "Tech.2026*"),
    ("Ana", "Torres Vega", "ana.torres@innovatech.pe", "Desarrollo", "Colaborador", "Tech.2026*"),
    ("Luis", "Ramírez Soto", "luis.ramirez@innovatech.pe", "Sistemas", "Colaborador", "Tech.2026*"),
    ("Carla", "Mendoza Ríos", "carla.mendoza@innovatech.pe", "Marketing", "Colaborador", "Tech.2026*"),
    ("Jorge", "Salazar Pinto", "jorge.salazar@innovatech.pe", "Soporte", "Colaborador", "Tech.2026*"),
    ("María", "López Huamán", "maria.lopez@innovatech.pe", "Contabilidad", "Colaborador", "Tech.2026*"),
    ("Rosa", "Quispe Huamán", "rosa.quispe@innovatech.pe", "Recursos Humanos", "Colaborador", "Tech.2026*"),
    ("Sandra", "Huanca Paredes", "sandra.huanca@innovatech.pe", "Desarrollo", "Colaborador", "Tech.2026*"),
    ("Miguel", "Rojas Campos", "miguel.rojas@innovatech.pe", "Contabilidad", "Colaborador", "Tech.2026*"),
    ("Diego", "Flores Ramos", "diego.flores@innovatech.pe", "Gerencia", "Colaborador", "Temporal.2026*"),
]

EQUIPOS = [
    ("TA-0001", "Laptop Dell Latitude 5440", "Laptop", "Dell", "Disponible"),
    ("TA-0002", "Laptop HP EliteBook 840", "Laptop", "HP", "Disponible"),
    ("TA-0003", "Laptop Lenovo ThinkPad T14", "Laptop", "Lenovo", "Disponible"),
    ("TA-0004", "MacBook Air M2", "Laptop", "Apple", "Disponible"),
    ("TA-0005", "Computadora HP ProDesk 400", "Computadora de escritorio", "HP", "Disponible"),
    ("TA-0006", "Computadora Dell OptiPlex 7010", "Computadora de escritorio", "Dell", "Disponible"),
    ("TA-0007", 'Monitor LG 24"', "Monitor", "LG", "Disponible"),
    ("TA-0008", 'Monitor Samsung 27"', "Monitor", "Samsung", "Disponible"),
    ("TA-0009", "Impresora HP LaserJet Pro", "Impresora", "HP", "Disponible"),
    ("TA-0010", "Impresora Epson EcoTank L3250", "Impresora", "Epson", "Disponible"),
    ("TA-0011", "Tablet iPad 10.ª generación", "Tablet", "Apple", "Disponible"),
    ("TA-0012", "Tablet Galaxy Tab S6", "Tablet", "Samsung", "Disponible"),
    ("TA-0013", "Proyector Epson PowerLite X49", "Proyector", "Epson", "Disponible"),
    ("TA-0014", "Proyector BenQ MX560", "Proyector", "BenQ", "Disponible"),
    ("TA-0015", "Switch Cisco Catalyst 2960", "Equipo de red", "Cisco", "Disponible"),
    ("TA-0016", "Router TP-Link Omada", "Equipo de red", "TP-Link", "Disponible"),
    ("TA-0017", "Laptop Asus ExpertBook", "Laptop", "Asus", "Mantenimiento"),
    ("TA-0018", "Monitor Dell P2422H", "Monitor", "Dell", "Baja"),
]

# (codigo equipo, correo colaborador, dias prestamo, dias devolucion, observacion, devolver, observacion_devolucion)
PRESTAMOS = [
    ("TA-0001", "ana.torres@innovatech.pe", 0, 5, "Trabajo remoto durante la semana de despliegue.", False, None),
    ("TA-0003", "luis.ramirez@innovatech.pe", 0, 3, "Soporte técnico en la sede del cliente.", False, None),
    ("TA-0005", "diego.flores@innovatech.pe", 0, 10, "Equipo para análisis de indicadores de Gerencia.", False, None),
    ("TA-0007", "carla.mendoza@innovatech.pe", 0, 10, "Diseño de campaña institucional en el área de Marketing.", False, None),
    ("TA-0009", "maria.lopez@innovatech.pe", 0, 7, "Impresión de documentos contables del cierre mensual.", False, None),
    ("TA-0011", "rosa.quispe@innovatech.pe", 0, 4, "Registro de asistencia en la feria de reclutamiento.", False, None),
    ("TA-0013", "jorge.salazar@innovatech.pe", 0, 2, "Presentación de soporte en la sala de capacitación.", False, None),
    ("TA-0015", "sandra.huanca@innovatech.pe", 0, 15, "Configuración de red para el nuevo laboratorio.", False, None),
    ("TA-0002", "carla.mendoza@innovatech.pe", -20, -15, "Campaña de lanzamiento de producto.", True, "Equipo devuelto completo y sin daños."),
    ("TA-0004", "ana.torres@innovatech.pe", -18, -10, "Desarrollo de prototipo móvil.", True, "MacBook devuelta con cargador original."),
    ("TA-0006", "luis.ramirez@innovatech.pe", -15, -12, "Migración de estaciones de trabajo.", True, "Equipo devuelto con configuración restaurada."),
    ("TA-0008", "jorge.salazar@innovatech.pe", -12, -8, "Monitoreo de red en el piso 3.", True, "Monitor devuelto sin observaciones."),
    ("TA-0010", "maria.lopez@innovatech.pe", -10, -9, "Impresión de contratos del periodo.", True, "Impresora devuelta con tóner al 40 %."),
    ("TA-0012", "rosa.quispe@innovatech.pe", -8, -4, "Entrevistas de selección de personal.", True, "Tablet devuelta con funda y cargador."),
    ("TA-0014", "sandra.huanca@innovatech.pe", -6, -2, "Capacitación de desarrollo web.", True, "Proyector devuelto con control remoto."),
    ("TA-0016", "luis.ramirez@innovatech.pe", -5, -1, "Pruebas de conectividad en la sede principal.", True, "Router devuelto con cables originales."),
    ("TA-0002", "jorge.salazar@innovatech.pe", -3, -1, "Soporte remoto a usuarios de Marketing.", True, "Laptop devuelta con batería al 85 %."),
]


def solicitar(ruta, metodo="GET", cuerpo=None, token=None):
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    cabeceras = {"Content-Type": "application/json"}
    if token:
        cabeceras["Authorization"] = f"Bearer {token}"
    peticion = urllib.request.Request(ruta, data=datos, method=metodo, headers=cabeceras)
    with urllib.request.urlopen(peticion, timeout=10) as respuesta:
        texto = respuesta.read().decode("utf-8-sig")
        return json.loads(texto) if texto else None


def token_de(correo, clave):
    return solicitar(f"{BASE}/auth/login", "POST", {"correo": correo, "clave": clave})["token"]



def main():
    token = solicitar(f"{BASE}/auth/login", "POST", {"correo": ADMIN[0], "clave": ADMIN[1]})["token"]

    usuarios = {}
    for nombres, apellidos, correo, area, rol, clave in USUARIOS:
        try:
            creado = solicitar(
                f"{BASE}/usuarios",
                "POST",
                {
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "correo": correo,
                    "area": area,
                    "rol": rol,
                    "claveTemporal": clave,
                },
                token,
            )
            usuarios[correo] = creado
            print(f"usuario {correo}")
        except urllib.error.HTTPError as error:
            print(f"usuario ERR {correo}: {error.read().decode('utf-8')[:120]}")

    equipos = {}
    for codigo, nombre, categoria, marca, estado in EQUIPOS:
        try:
            creado = solicitar(
                f"{BASE}/equipos",
                "POST",
                {
                    "codigoPatrimonial": codigo,
                    "nombre": nombre,
                    "categoria": categoria,
                    "marca": marca,
                    "estado": estado,
                },
                token,
            )
            equipos[codigo] = creado
            print(f"equipo {codigo}")
        except urllib.error.HTTPError as error:
            print(f"equipo ERR {codigo}: {error.read().decode('utf-8')[:120]}")

    hoy = date.today()
    for codigo, correo, dias_prestamo, dias_devolucion, observacion, devolver, obs_devolucion in PRESTAMOS:
        try:
            prestamo = solicitar(
                f"{BASE}/prestamos",
                "POST",
                {
                    "usuarioId": usuarios[correo]["id"],
                    "equipoId": equipos[codigo]["id"],
                    "fechaPrestamo": (hoy + timedelta(days=dias_prestamo)).isoformat(),
                    "fechaDevolucion": (hoy + timedelta(days=dias_devolucion)).isoformat(),
                    "observacion": observacion,
                },
                token,
            )

            if devolver:
                solicitar(
                    f"{BASE}/prestamos/{prestamo['id']}/devolver",
                    "PATCH",
                    {"observacionDevolucion": obs_devolucion},
                    token,
                )

            print(f"prestamo {prestamo['codigo']} {codigo}")
        except urllib.error.HTTPError as error:
            print(f"prestamo ERR {codigo}: {error.read().decode('utf-8')[:160]}")

    rosa = token_de("rosa.quispe@innovatech.pe", "Tech.2026*")
    sandra = token_de("sandra.huanca@innovatech.pe", "Tech.2026*")

    def crear_solicitud(token_colaborador, codigo, dias_prestamo, dias_devolucion, motivo):
        return solicitar(
            f"{BASE}/solicitudes",
            "POST",
            {
                "equipoId": equipos[codigo]["id"],
                "fechaPrestamo": (hoy + timedelta(days=dias_prestamo)).isoformat(),
                "fechaDevolucion": (hoy + timedelta(days=dias_devolucion)).isoformat(),
                "motivo": motivo,
            },
            token_colaborador,
        )

    pendiente_rosa = crear_solicitud(
        rosa,
        "TA-0002",
        1,
        6,
        "Equipo para la revisión de campañas del área de Recursos Humanos.",
    )
    print(f"solicitud {pendiente_rosa['codigo']} pendiente")

    pendiente_sandra = crear_solicitud(
        sandra,
        "TA-0012",
        2,
        5,
        "Tablet para el registro de asistencia en la feria de reclutamiento.",
    )
    print(f"solicitud {pendiente_sandra['codigo']} pendiente")

    rechazada = crear_solicitud(
        rosa,
        "TA-0004",
        3,
        8,
        "Equipo para una actividad académica externa.",
    )
    solicitar(
        f"{BASE}/solicitudes/{rechazada['id']}/rechazar",
        "PATCH",
        {"observacionRevision": "El equipo se reserva para el área de Desarrollo durante ese periodo."},
        token,
    )
    print(f"solicitud {rechazada['codigo']} rechazada")

    entorno = os.environ.copy()
    entorno["PGPASSWORD"] = "postgres"

    solicitud_aprobada_id = str(uuid.uuid4())
    sql_aprobada = f'''
INSERT INTO "Solicitudes" (
    "Id", "FechaPrestamo", "FechaDevolucion", "Motivo", "Estado", "ObservacionRevision",
    "UsuarioId", "EquipoId", "PrestamoId", "RevisadoPorId", "FechaRegistro", "FechaRevision"
)
SELECT '{solicitud_aprobada_id}'::uuid, p."FechaPrestamo", p."FechaDevolucion", p."Observacion", 'Aprobada',
       'Solicitud aprobada durante la carga de demostracion.',
       p."UsuarioId", p."EquipoId", p."Id",
       (SELECT "Id" FROM "Usuarios" WHERE "Correo" = 'kevin.ccente@innovatech.pe'),
       now(), now()
FROM "Prestamos" p
JOIN "Equipos" e ON e."Id" = p."EquipoId"
WHERE e."CodigoPatrimonial" = 'TA-0001' AND p."Estado" = 'Activo'
LIMIT 1;
'''
    subprocess.run(
        [PSQL, "-U", "postgres", "-h", "localhost", "-d", "TechAssetDB", "-c", sql_aprobada],
        check=True,
        env=entorno,
    )

    sql = (
        'UPDATE "Usuarios" SET "DebeCambiarPassword" = false '
        'WHERE "Correo" <> \'diego.flores@innovatech.pe\';'
    )
    subprocess.run(
        [PSQL, "-U", "postgres", "-h", "localhost", "-d", "TechAssetDB", "-c", sql],
        check=True,
        env=entorno,
    )

    resumen = solicitar(f"{BASE}/reportes/resumen", token=token)
    print("\nResumen:", json.dumps(resumen, ensure_ascii=False))


if __name__ == "__main__":
    main()
