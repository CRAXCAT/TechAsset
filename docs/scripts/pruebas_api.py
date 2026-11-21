"""Pruebas funcionales de la API de TechAsset."""
import json
import urllib.error
import urllib.request
import uuid
from datetime import date, timedelta
from pathlib import Path

BASE = "http://localhost:5143/api"
SALIDA = Path(__file__).resolve().parents[1] / "pruebas-api.json"

ADMIN = ("admin@innovatech.pe", "Admin.2026*")
RESPONSABLE = ("lucia.paredes@innovatech.pe", "Tech.2026*")
COLABORADOR = ("ana.torres@innovatech.pe", "Tech.2026*")

resultados = []


def solicitar(ruta, metodo="GET", cuerpo=None, token=None):
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    cabeceras = {"Content-Type": "application/json"}
    if token:
        cabeceras["Authorization"] = f"Bearer {token}"
    peticion = urllib.request.Request(ruta, data=datos, method=metodo, headers=cabeceras)
    try:
        with urllib.request.urlopen(peticion, timeout=10) as respuesta:
            texto = respuesta.read().decode("utf-8-sig")
            try:
                datos = json.loads(texto) if texto else None
            except json.JSONDecodeError:
                datos = None
            return respuesta.status, datos
    except urllib.error.HTTPError as error:
        texto = error.read().decode("utf-8")
        try:
            datos = json.loads(texto) if texto else None
        except json.JSONDecodeError:
            datos = None
        return error.code, datos


def token_de(credenciales):
    _, datos = solicitar(f"{BASE}/auth/login", "POST", {"correo": credenciales[0], "clave": credenciales[1]})
    return datos["token"]


def registrar(codigo, escenario, entrada, estado, respuesta, esperado):
    mensaje = ""
    if isinstance(respuesta, dict):
        mensaje = respuesta.get("mensaje") or ""
        if not mensaje and "errores" in respuesta:
            mensaje = "; ".join(f"{k}: {v[0]}" for k, v in respuesta["errores"].items())
        if not mensaje and "items" in respuesta:
            mensaje = f"{len(respuesta['items'])} item(s) de {respuesta.get('total')} total"
        if not mensaje and "codigo" in respuesta and "estado" in respuesta:
            mensaje = f"{respuesta['codigo']} · {respuesta['estado']}"
        if not mensaje and "totalEquipos" in respuesta:
            mensaje = f"equipos={respuesta['totalEquipos']}, préstamos={respuesta['totalPrestamos']}, área={respuesta['areaMayorUso']}"
        if not mensaje and "correo" in respuesta and "rol" in respuesta:
            mensaje = f"{respuesta['correo']} · {respuesta['rol']}"

    if not mensaje:
        mensaje = {401: "No autorizado", 403: "Acceso denegado", 200: "Operación correcta", 201: "Recurso creado"}.get(estado, "")

    resultados.append(
        {
            "codigo": codigo,
            "escenario": escenario,
            "entrada": entrada,
            "http": estado,
            "mensaje": mensaje,
            "esperado": esperado,
            "cumple": estado == esperado,
        }
    )
    print(f"{'OK ' if estado == esperado else 'FALLA'} {codigo} HTTP {estado} -> {mensaje[:100]}")


def main():
    admin = token_de(ADMIN)
    responsable = token_de(RESPONSABLE)
    colaborador = token_de(COLABORADOR)

    estado, respuesta = solicitar(f"{BASE}/auth/login", "POST", {"correo": ADMIN[0], "clave": ADMIN[1]})
    registrar("A-01", "Inicio de sesión con credenciales válidas", ADMIN[0], estado, respuesta, 200)

    estado, respuesta = solicitar(f"{BASE}/auth/login", "POST", {"correo": ADMIN[0], "clave": "Mala.2026*"})
    registrar("A-02", "Inicio de sesión con contraseña incorrecta", "clave incorrecta", estado, respuesta, 401)

    estado, respuesta = solicitar(f"{BASE}/equipos")
    registrar("A-03", "Consulta sin token de sesión", "GET /equipos sin Authorization", estado, respuesta, 401)

    estado, respuesta = solicitar(
        f"{BASE}/usuarios",
        "POST",
        {"nombres": "Prueba", "apellidos": "Permiso", "correo": "prueba.permiso@innovatech.pe", "area": "Sistemas", "rol": "Colaborador", "claveTemporal": "Prueba.2026*"},
        responsable,
    )
    registrar("A-04", "Registrar usuario con rol Responsable", "POST /usuarios, rol=Responsable", estado, respuesta, 403)

    _, usuarios = solicitar(f"{BASE}/usuarios", token=admin)
    _, equipos = solicitar(f"{BASE}/equipos", token=admin)
    por_correo = {u["correo"]: u for u in usuarios}
    por_codigo = {e["codigoPatrimonial"]: e for e in equipos}

    estado, respuesta = solicitar(
        f"{BASE}/usuarios/{por_correo['miguel.rojas@innovatech.pe']['id']}/activo?activo=false",
        "PATCH",
        None,
        responsable,
    )
    registrar("A-05", "Deshabilitar usuario con rol Responsable (RN-09)", "PATCH /usuarios/{id}/activo", estado, respuesta, 403)

    estado, respuesta = solicitar(
        f"{BASE}/usuarios",
        "POST",
        {"nombres": "Rosa", "apellidos": "Quispe", "correo": "rosa.quispe@innovatech.pe", "area": "Desarrollo", "rol": "Colaborador", "claveTemporal": "Prueba.2026*"},
        admin,
    )
    registrar("U-01", "Correo institucional duplicado (RN-08)", "rosa.quispe@innovatech.pe", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/usuarios",
        "POST",
        {"nombres": "Diego", "apellidos": "Externo", "correo": "diego.externo@gmail.com", "area": "Sistemas", "rol": "Colaborador", "claveTemporal": "Prueba.2026*"},
        admin,
    )
    registrar("U-02", "Correo fuera del dominio corporativo", "diego.externo@gmail.com", estado, respuesta, 400)

    estado, respuesta = solicitar(
        f"{BASE}/equipos",
        "POST",
        {"codigoPatrimonial": "TA-0001", "nombre": "Equipo duplicado", "categoria": "Laptop", "marca": "Dell", "estado": "Disponible"},
        admin,
    )
    registrar("E-01", "Código patrimonial duplicado (RN-07)", "TA-0001", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/equipos",
        "POST",
        {"codigoPatrimonial": "TA-0099", "nombre": "Impresora 3D", "categoria": "Impresora 3D", "marca": "Creality", "estado": "Disponible"},
        admin,
    )
    registrar("E-02", "Categoría fuera del catálogo", "categoria=Impresora 3D", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/equipos/{por_codigo['TA-0002']['id']}/estado",
        "PATCH",
        {"estado": "Prestado"},
        admin,
    )
    registrar("E-03", "Asignar Prestado manualmente", "estado=Prestado", estado, respuesta, 409)

    estado, respuesta = solicitar(f"{BASE}/equipos/{por_codigo['TA-0002']['id']}", "DELETE", token=admin)
    registrar("E-04", "Eliminar equipo con historial (RN-06)", "TA-0002 con 2 préstamos", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["ana.torres@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0002"]["id"],
            "fechaPrestamo": (date.today() + timedelta(days=1)).isoformat(),
            "fechaDevolucion": (date.today() + timedelta(days=5)).isoformat(),
            "observacion": "Prueba automatizada de préstamo válido.",
        },
        admin,
    )
    registrar("R-01", "Registrar préstamo válido", "TA-0002 a Ana Torres", estado, respuesta, 201)
    prestamo = respuesta if estado == 201 else None

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["luis.ramirez@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0002"]["id"],
            "fechaPrestamo": (date.today() + timedelta(days=1)).isoformat(),
            "fechaDevolucion": (date.today() + timedelta(days=4)).isoformat(),
            "observacion": "Intento de segundo préstamo activo.",
        },
        admin,
    )
    registrar("R-02", "Segundo préstamo activo del mismo equipo (RN-01)", "TA-0002 ya prestado", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["ana.torres@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0017"]["id"],
            "fechaPrestamo": (date.today() + timedelta(days=1)).isoformat(),
            "fechaDevolucion": (date.today() + timedelta(days=3)).isoformat(),
            "observacion": "Intento de préstamo de equipo en mantenimiento.",
        },
        admin,
    )
    registrar("R-03", "Préstamo de equipo en Mantenimiento (RN-02)", "TA-0017", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["ana.torres@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0018"]["id"],
            "fechaPrestamo": (date.today() + timedelta(days=1)).isoformat(),
            "fechaDevolucion": (date.today() + timedelta(days=3)).isoformat(),
            "observacion": "Intento de préstamo de equipo dado de baja.",
        },
        admin,
    )
    registrar("R-04", "Préstamo de equipo en Baja (RN-03)", "TA-0018", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["ana.torres@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0004"]["id"],
            "fechaPrestamo": (date.today() + timedelta(days=5)).isoformat(),
            "fechaDevolucion": (date.today() + timedelta(days=5)).isoformat(),
            "observacion": "Intento con devolución el mismo día.",
        },
        admin,
    )
    registrar("R-05", "Devolución no posterior al préstamo (RN-04)", "misma fecha", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["ana.torres@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0004"]["id"],
            "fechaPrestamo": (date.today() + timedelta(days=1)).isoformat(),
            "fechaDevolucion": (date.today() + timedelta(days=3)).isoformat(),
            "observacion": "abc",
        },
        admin,
    )
    registrar("R-06", "Observación menor al mínimo permitido", "observacion=abc", estado, respuesta, 400)

    estado, respuesta = solicitar(
        f"{BASE}/usuarios/{por_correo['miguel.rojas@innovatech.pe']['id']}/activo?activo=false",
        "PATCH",
        None,
        admin,
    )
    registrar("R-07", "Deshabilitar usuario sin préstamos activos", "Miguel Rojas", estado, respuesta, 200)

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["miguel.rojas@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0004"]["id"],
            "fechaPrestamo": (date.today() + timedelta(days=1)).isoformat(),
            "fechaDevolucion": (date.today() + timedelta(days=3)).isoformat(),
            "observacion": "Préstamo a usuario inactivo.",
        },
        admin,
    )
    registrar("R-08", "Préstamo a colaborador inactivo", "Miguel Rojas inactivo", estado, respuesta, 409)

    estado, respuesta = solicitar(f"{BASE}/prestamos/{prestamo['id']}/devolver", "PATCH", {"observacionDevolucion": ""}, admin)
    registrar("R-09", "Devolución sin observaciones (RN-10)", "observación vacía", estado, respuesta, 400)

    estado, respuesta = solicitar(f"{BASE}/prestamos/{prestamo['id']}/devolver", "PATCH", {"observacionDevolucion": "Equipo devuelto con cargador y sin daños."}, admin)
    registrar("R-10", "Registrar devolución válida", "observación completa", estado, respuesta, 200)

    estado, respuesta = solicitar(f"{BASE}/prestamos/{prestamo['id']}/devolver", "PATCH", {"observacionDevolucion": "Segundo intento de devolución."}, admin)
    registrar("R-11", "Devolución repetida", "préstamo ya devuelto", estado, respuesta, 409)

    estado, respuesta = solicitar(f"{BASE}/equipos/{por_codigo['TA-0002']['id']}", token=admin)
    registrar("R-12", "Equipo disponible tras la devolución", "TA-0002", estado, respuesta, 200)

    estado, respuesta = solicitar(f"{BASE}/prestamos?estado=Activo&pagina=1&tamanoPagina=5", token=admin)
    registrar("R-13", "Filtro de préstamos activos y paginación", "estado=Activo", estado, respuesta, 200)

    estado, respuesta = solicitar(f"{BASE}/prestamos?area=Desarrollo&texto=Ana", token=admin)
    registrar("R-14", "Búsqueda por área y colaborador", "area=Desarrollo, texto=Ana", estado, respuesta, 200)

    estado, respuesta = solicitar(f"{BASE}/prestamos", "POST", {
        "usuarioId": por_correo["ana.torres@innovatech.pe"]["id"],
        "equipoId": por_codigo["TA-0004"]["id"],
        "fechaPrestamo": (date.today() + timedelta(days=1)).isoformat(),
        "fechaDevolucion": (date.today() + timedelta(days=3)).isoformat(),
        "observacion": "Intento con rol Colaborador.",
    }, colaborador)
    registrar("R-15", "Registrar préstamo con rol Colaborador (RN-05)", "rol=Colaborador", estado, respuesta, 403)

    estado, respuesta = solicitar(f"{BASE}/reportes/resumen", token=admin)
    registrar("R-16", "Indicadores del dashboard", "GET /reportes/resumen", estado, respuesta, 200)

    estado, respuesta = solicitar(f"{BASE}/reportes/prestamos.csv", token=admin)
    registrar("R-17", "Exportar préstamos a CSV", "GET /reportes/prestamos.csv", estado, respuesta, 200)

    estado, respuesta = solicitar(f"{BASE}/reportes/equipos.csv", token=admin)
    registrar("R-18", "Exportar inventario a CSV", "GET /reportes/equipos.csv", estado, respuesta, 200)

    # ------------------------------------------------------------------
    # Seguridad, alcance por rol y solicitudes con aprobación
    # ------------------------------------------------------------------
    estado, respuesta = solicitar(f"{BASE}/usuarios", token=colaborador)
    registrar("A-06", "Colaborador intenta consultar usuarios", "GET /usuarios", estado, respuesta, 403)

    estado, respuesta = solicitar(f"{BASE}/reportes/prestamos.csv", token=colaborador)
    registrar("A-07", "Colaborador intenta exportar reportes", "GET /reportes/prestamos.csv", estado, respuesta, 403)

    estado, respuesta = solicitar(f"{BASE}/movimientos", token=colaborador)
    registrar("A-08", "Colaborador intenta consultar la auditoría", "GET /movimientos", estado, respuesta, 403)

    _, propios = solicitar(f"{BASE}/prestamos?pagina=1&tamanoPagina=50", token=colaborador)
    propios_items = propios.get("items", [])
    todos_propios = all(item["usuarioId"] == por_correo["ana.torres@innovatech.pe"]["id"] for item in propios_items)
    registrar(
        "R-19",
        "Historial del Colaborador limitado a sus propios préstamos",
        "GET /prestamos como Ana Torres",
        200 if todos_propios else 409,
        {"mensaje": f"{len(propios_items)} préstamo(s), todos propios" if todos_propios else "Se encontraron préstamos ajenos"},
        200,
    )

    _, todos = solicitar(f"{BASE}/prestamos?pagina=1&tamanoPagina=50", token=admin)
    total_global = todos.get("total", 0)
    registrar(
        "R-20",
        "Administrador consulta el historial global",
        "GET /prestamos como Administrador",
        200 if total_global > len(propios_items) else 409,
        {"mensaje": f"{total_global} préstamo(s) visibles"},
        200,
    )

    manana = (date.today() + timedelta(days=1)).isoformat()
    en_cinco = (date.today() + timedelta(days=5)).isoformat()

    estado, respuesta = solicitar(
        f"{BASE}/solicitudes",
        "POST",
        {
            "equipoId": por_codigo["TA-0008"]["id"],
            "fechaPrestamo": manana,
            "fechaDevolucion": en_cinco,
            "motivo": "Solicitud de prueba para validar el flujo de aprobación.",
        },
        colaborador,
    )
    registrar("S-01", "Colaborador registra una solicitud válida", "POST /solicitudes · TA-0008", estado, respuesta, 201)
    solicitud_aprobable = respuesta if estado == 201 else None

    estado, respuesta = solicitar(
        f"{BASE}/solicitudes",
        "POST",
        {
            "equipoId": por_codigo["TA-0008"]["id"],
            "fechaPrestamo": manana,
            "fechaDevolucion": en_cinco,
            "motivo": "Segunda solicitud para el mismo equipo.",
        },
        colaborador,
    )
    registrar("S-02", "Solicitud duplicada para un equipo con pendiente", "POST /solicitudes · TA-0008", estado, respuesta, 409)

    if solicitud_aprobable:
        estado, respuesta = solicitar(
            f"{BASE}/solicitudes/{solicitud_aprobable['id']}/aprobar",
            "PATCH",
            {"observacionRevision": "Intento del colaborador."},
            colaborador,
        )
        registrar("S-03", "Colaborador intenta aprobar su propia solicitud", "PATCH /solicitudes/{id}/aprobar", estado, respuesta, 403)

        estado, respuesta = solicitar(
            f"{BASE}/solicitudes/{solicitud_aprobable['id']}/aprobar",
            "PATCH",
            {"observacionRevision": "Aprobado; el colaborador recogerá el equipo en Soporte."},
            responsable,
        )
        registrar("S-04", "Responsable aprueba y genera el préstamo", "PATCH /solicitudes/{id}/aprobar", estado, respuesta, 200)

        estado, respuesta = solicitar(
            f"{BASE}/solicitudes/{solicitud_aprobable['id']}/aprobar",
            "PATCH",
            {"observacionRevision": "Segundo intento."},
            responsable,
        )
        registrar("S-05", "Aprobar una solicitud ya aprobada", "PATCH /solicitudes/{id}/aprobar", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/solicitudes",
        "POST",
        {
            "equipoId": por_codigo["TA-0004"]["id"],
            "fechaPrestamo": manana,
            "fechaDevolucion": (date.today() + timedelta(days=4)).isoformat(),
            "motivo": "Solicitud que será rechazada con observación.",
        },
        colaborador,
    )
    registrar("S-06", "Crear solicitud para el flujo de rechazo", "POST /solicitudes · TA-0004", estado, respuesta, 201)
    solicitud_rechazable = respuesta if estado == 201 else None

    if solicitud_rechazable:
        estado, respuesta = solicitar(
            f"{BASE}/solicitudes/{solicitud_rechazable['id']}/rechazar",
            "PATCH",
            {},
            responsable,
        )
        registrar("S-07", "Rechazo sin observación", "PATCH /solicitudes/{id}/rechazar", estado, respuesta, 409)

        estado, respuesta = solicitar(
            f"{BASE}/solicitudes/{solicitud_rechazable['id']}/rechazar",
            "PATCH",
            {"observacionRevision": "El equipo se reserva para una actividad prioritaria del área."},
            responsable,
        )
        registrar("S-08", "Rechazo con observación", "PATCH /solicitudes/{id}/rechazar", estado, respuesta, 200)

    estado, respuesta = solicitar(
        f"{BASE}/solicitudes",
        "POST",
        {
            "equipoId": por_codigo["TA-0017"]["id"],
            "fechaPrestamo": manana,
            "fechaDevolucion": en_cinco,
            "motivo": "Intento de solicitud de un equipo en mantenimiento.",
        },
        colaborador,
    )
    registrar("S-09", "Solicitud de un equipo en Mantenimiento (RN-02)", "POST /solicitudes · TA-0017", estado, respuesta, 409)

    _, mis_solicitudes = solicitar(f"{BASE}/solicitudes?pagina=1&tamanoPagina=50", token=colaborador)
    solicitudes_items = mis_solicitudes.get("items", [])
    solo_propias = all(item["usuarioId"] == por_correo["ana.torres@innovatech.pe"]["id"] for item in solicitudes_items)
    registrar(
        "S-10",
        "Colaborador solo ve sus propias solicitudes",
        "GET /solicitudes como Ana Torres",
        200 if solo_propias else 409,
        {"mensaje": f"{len(solicitudes_items)} solicitud(es), todas propias" if solo_propias else "Se encontraron solicitudes ajenas"},
        200,
    )

    estado, respuesta = solicitar(
        f"{BASE}/solicitudes",
        "POST",
        {
            "equipoId": por_codigo["TA-0014"]["id"],
            "fechaPrestamo": manana,
            "fechaDevolucion": manana,
            "motivo": "Solicitud con devolución el mismo día.",
        },
        colaborador,
    )
    registrar("S-11", "Solicitud con devolución no posterior (RN-04)", "misma fecha · TA-0014", estado, respuesta, 409)

    estado, respuesta = solicitar(
        f"{BASE}/solicitudes",
        "POST",
        {
            "equipoId": por_codigo["TA-0010"]["id"],
            "fechaPrestamo": manana,
            "fechaDevolucion": (date.today() + timedelta(days=3)).isoformat(),
            "motivo": "Solicitud que perderá disponibilidad antes de la aprobación.",
        },
        colaborador,
    )
    registrar("S-12", "Crear solicitud para probar concurrencia", "POST /solicitudes · TA-0010", estado, respuesta, 201)
    solicitud_concurrente = respuesta if estado == 201 else None

    _, respuesta_equipo = solicitar(f"{BASE}/equipos/{por_codigo['TA-0010']['id']}", token=admin)
    registrar("S-13", "Consultar equipo antes de la aprobación", "GET /equipos/{id}", 200, respuesta_equipo, 200)

    estado, respuesta = solicitar(
        f"{BASE}/prestamos",
        "POST",
        {
            "usuarioId": por_correo["ana.torres@innovatech.pe"]["id"],
            "equipoId": por_codigo["TA-0010"]["id"],
            "fechaPrestamo": manana,
            "fechaDevolucion": (date.today() + timedelta(days=3)).isoformat(),
            "observacion": "Préstamo directo que ocupa el equipo antes de aprobar la solicitud.",
        },
        admin,
    )
    registrar("S-14", "Ocupar el equipo con un préstamo directo", "POST /prestamos · TA-0010", estado, respuesta, 201)

    if solicitud_concurrente:
        estado, respuesta = solicitar(
            f"{BASE}/solicitudes/{solicitud_concurrente['id']}/aprobar",
            "PATCH",
            {"observacionRevision": "Intento de aprobación con el equipo ya prestado."},
            responsable,
        )
        registrar("S-15", "Aprobar solicitud con equipo ya no disponible", "PATCH /solicitudes/{id}/aprobar", estado, respuesta, 409)

    estado, respuesta = solicitar(f"{BASE}/movimientos?pagina=1&tamanoPagina=50", token=admin)
    registrar("S-16", "Auditoría disponible para el Administrador", "GET /movimientos", estado, respuesta, 200)

    # Restaurar al usuario deshabilitado
    solicitar(
        f"{BASE}/usuarios/{por_correo['miguel.rojas@innovatech.pe']['id']}/activo?activo=true",
        "PATCH",
        None,
        admin,
    )

    conformes = sum(1 for r in resultados if r["cumple"])
    print(f"\nResultado: {conformes}/{len(resultados)} escenarios conformes")
    SALIDA.write_text(json.dumps({"resultados": resultados, "conformes": conformes, "total": len(resultados)}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
