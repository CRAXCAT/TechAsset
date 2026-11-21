"""Genera las figuras técnicas del informe de TechAsset."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BASE = Path(__file__).resolve().parents[1]
SALIDA = BASE / "figuras"
SALIDA.mkdir(exist_ok=True)

AZUL = "#1D4ED8"
AZUL_OSCURO = "#16367F"
AZUL_CLARO = "#DBEAFE"
AZUL_MEDIO = "#93C5FD"
GRIS = "#475569"
GRIS_CLARO = "#64748B"
VERDE = "#047857"
AMBAR = "#B45309"
BLANCO = "#FFFFFF"


def caja(ax, x, y, w, h, titulo, lineas, color=AZUL, relleno=BLANCO, tam_titulo=10, tam=8):
    ax.add_patch(FancyBboxPatch((x + 0.006, y - 0.008), w, h,
                                boxstyle="round,pad=0.008,rounding_size=0.012",
                                linewidth=0, facecolor="#DCE3EE", alpha=0.55, zorder=1))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.008,rounding_size=0.012",
                                linewidth=1.4, edgecolor=color, facecolor=relleno, zorder=2))
    ax.text(x + w / 2, y + h - 0.035, titulo, ha="center", va="top", fontsize=tam_titulo,
            fontweight="bold", color=color, zorder=3)
    if lineas:
        ax.text(x + w / 2, y + h - 0.088, "\n".join(lineas), ha="center", va="top", fontsize=tam,
                color=GRIS, linespacing=1.45, zorder=3)


def flecha(ax, x1, y1, x2, y2, color=GRIS_CLARO):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
                                 linewidth=1.3, color=color, zorder=4))


def guardar(fig, nombre):
    fig.savefig(SALIDA / nombre, dpi=200, bbox_inches="tight", facecolor=BLANCO)
    plt.close(fig)
    print("figura", nombre)


# ---------------------------------------------------------------------------
# 1. Arquitectura por capas
# ---------------------------------------------------------------------------
def arquitectura():
    fig, ax = plt.subplots(figsize=(13, 5.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0.015, 0.08), 0.165, 0.8,
                                boxstyle="round,pad=0.008,rounding_size=0.015",
                                facecolor="#EFF6FF", edgecolor=AZUL_MEDIO, linewidth=1.2))
    ax.text(0.0975, 0.83, "FRONTEND", ha="center", fontsize=9, fontweight="bold", color=AZUL)
    caja(ax, 0.03, 0.58, 0.135, 0.19, "SPA React 19", ["Vite · React Router", "Hooks y contexto"],
         color=AZUL, tam_titulo=9.5, tam=7.4)
    caja(ax, 0.03, 0.33, 0.135, 0.19, "Componentes", ["Formularios, tablas,", "modales y tarjetas"],
         color=AZUL, tam_titulo=9.5, tam=7.4)
    caja(ax, 0.03, 0.11, 0.135, 0.16, "Cliente API", ["fetch + JWT", "Manejo de errores"],
         color=AZUL, tam_titulo=9.5, tam=7.4)

    flecha(ax, 0.175, 0.62, 0.225, 0.62)

    caja(ax, 0.235, 0.50, 0.16, 0.30, "API", ["Controllers REST", "Middleware de errores",
                                              "Swagger / CORS", "[Authorize(Roles)]"],
         color=AZUL_OSCURO, tam_titulo=10)
    caja(ax, 0.425, 0.50, 0.16, 0.30, "Application", ["Servicios de caso de uso", "DTO y validaciones",
                                                      "RN-01 a RN-10", "Excepciones de negocio"],
         color=AZUL_OSCURO, tam_titulo=10)
    caja(ax, 0.615, 0.50, 0.16, 0.30, "Infrastructure", ["Repositorios EF Core", "DbContext y migraciones",
                                                         "BCrypt · JWT", "Consultas y agregados"],
         color=AZUL_OSCURO, tam_titulo=10)
    caja(ax, 0.805, 0.50, 0.16, 0.30, "PostgreSQL 18", ["TechAssetDB", "Usuarios · Equipos", "Prestamos"],
         color=VERDE, tam_titulo=10)

    flecha(ax, 0.395, 0.65, 0.425, 0.65)
    flecha(ax, 0.585, 0.65, 0.615, 0.65)
    flecha(ax, 0.775, 0.65, 0.805, 0.65)

    ax.add_patch(FancyBboxPatch((0.235, 0.155), 0.54, 0.18,
                                boxstyle="round,pad=0.008,rounding_size=0.012",
                                facecolor="#FFF7ED", edgecolor="#FDBA74", linewidth=1.2))
    ax.text(0.505, 0.295, "SEGURIDAD TRANSVERSAL", ha="center", fontsize=8.4, fontweight="bold", color=AMBAR)
    ax.text(0.505, 0.235,
            "BCrypt para contraseñas  ·  JWT firmado (rol y área)  ·  contraseña temporal  ·  rutas privadas",
            ha="center", fontsize=7.6, color=GRIS)

    ax.text(0.0975, 0.035, "Navegador", ha="center", fontsize=7.8, color=GRIS_CLARO)
    ax.text(0.885, 0.42, "Persistencia", ha="center", fontsize=7.8, color=GRIS_CLARO)
    ax.text(0.5, 0.075, "El cliente consume la API por HTTPS con token JWT; las respuestas viajan en JSON.",
            ha="center", fontsize=7.6, color=GRIS_CLARO, style="italic")
    ax.text(0.5, 0.03,
            "Domain: entidades Usuario, Equipo y Prestamo + catálogo centralizado de roles, áreas, categorías y estados",
            ha="center", fontsize=7.2, color="#94A3B8", style="italic")
    guardar(fig, "arquitectura.png")


# ---------------------------------------------------------------------------
# 2. Modelo de datos
# ---------------------------------------------------------------------------
def modelo_datos():
    fig, ax = plt.subplots(figsize=(12.5, 7.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def entidad(x, y, w, h, titulo, campos, color=AZUL):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                    facecolor=BLANCO, edgecolor=color, linewidth=1.4, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.085), w, 0.085,
                                    boxstyle="round,pad=0.006,rounding_size=0.012",
                                    facecolor=color, edgecolor=color, linewidth=1.4, zorder=3))
        ax.text(x + w / 2, y + h - 0.042, titulo, ha="center", va="center", fontsize=10,
                fontweight="bold", color=BLANCO, zorder=4)
        for i, (nombre, detalle) in enumerate(campos):
            yy = y + h - 0.125 - i * 0.0455
            peso = "bold" if nombre in ("PK", "FK", "UQ") else "normal"
            ax.text(x + 0.012, yy, nombre, fontsize=7.3,
                    color=AZUL_OSCURO if peso == "bold" else GRIS,
                    fontweight=peso, va="center", zorder=4)
            ax.text(x + 0.075, yy, detalle, fontsize=7.1, color=GRIS, va="center", zorder=4)

    entidad(0.02, 0.30, 0.28, 0.58, "Usuarios", [
        ("PK", "Id (Guid)"),
        ("", "Nombres (varchar 100)"),
        ("", "Apellidos (varchar 100)"),
        ("UQ", "Correo (varchar 150)"),
        ("", "Area (varchar 100)"),
        ("", "Rol (varchar 30)"),
        ("", "Activo (bool)"),
        ("", "PasswordHash (varchar 300)"),
        ("", "DebeCambiarPassword (bool)"),
        ("", "FechaRegistro (timestamp)"),
    ])

    entidad(0.36, 0.20, 0.28, 0.68, "Prestamos", [
        ("PK", "Id (Guid)"),
        ("FK", "UsuarioId → Usuarios"),
        ("FK", "EquipoId → Equipos"),
        ("FK", "ResponsableId → Usuarios"),
        ("", "FechaPrestamo (DateOnly)"),
        ("", "FechaDevolucion (DateOnly)"),
        ("", "FechaDevolucionReal (opcional)"),
        ("", "Observacion (varchar 300)"),
        ("", "ObservacionDevolucion (opcional)"),
        ("", "Estado (varchar 30)"),
        ("", "FechaRegistro (timestamp)"),
    ], color=AZUL_OSCURO)

    entidad(0.71, 0.42, 0.27, 0.46, "Equipos", [
        ("PK", "Id (Guid)"),
        ("UQ", "CodigoPatrimonial (varchar 50)"),
        ("", "Nombre (varchar 100)"),
        ("", "Categoria (varchar 50)"),
        ("", "Marca (varchar 50)"),
        ("", "Estado (varchar 30)"),
        ("", "FechaRegistro (timestamp)"),
    ], color=VERDE)

    ax.plot([0.30, 0.36], [0.74, 0.74], color=GRIS_CLARO, linewidth=1.3, zorder=1)
    ax.plot([0.30, 0.36], [0.68, 0.68], color=GRIS_CLARO, linewidth=1.3, zorder=1)
    ax.text(0.322, 0.755, "1", fontsize=8, color=GRIS, ha="center")
    ax.text(0.338, 0.695, "N", fontsize=8, color=GRIS, ha="center")

    ax.plot([0.71, 0.64], [0.62, 0.62], color=GRIS_CLARO, linewidth=1.3, zorder=1)
    ax.text(0.695, 0.635, "1", fontsize=8, color=GRIS, ha="center")
    ax.text(0.652, 0.589, "N", fontsize=8, color=GRIS, ha="center")

    ax.text(0.5, 0.955, "Modelo relacional de TechAsset (3 tablas y 3 claves foráneas)",
            ha="center", fontsize=11, fontweight="bold", color=AZUL_OSCURO)
    ax.text(0.5, 0.912,
            "El usuario solicitante y el usuario responsable se relacionan con Prestamos; el borrado es RESTRICT para conservar el historial.",
            ha="center", fontsize=7.6, color=GRIS_CLARO)
    ax.text(0.02, 0.255,
            "Índices:\n· Prestamos (EquipoId, Estado)\n· Prestamos (UsuarioId, FechaPrestamo)\n· Usuarios (Correo) único\n· Equipos (CodigoPatrimonial) único",
            fontsize=7.2, color=GRIS_CLARO, va="top", linespacing=1.5)
    guardar(fig, "modelo_datos.png")


# ---------------------------------------------------------------------------
# 3. Flujo de registro de un prestamo (pipeline en U)
# ---------------------------------------------------------------------------
def flujo_prestamo():
    fig, ax = plt.subplots(figsize=(13, 6.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def paso(x, y, w, h, numero, titulo, detalle, color=AZUL):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                    facecolor=BLANCO, edgecolor=color, linewidth=1.3, zorder=2))
        ax.add_patch(mpatches.Circle((x + 0.022, y + h - 0.032), 0.014,
                                     facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.022, y + h - 0.032, str(numero), ha="center", va="center", fontsize=7.6,
                fontweight="bold", color=BLANCO, zorder=4)
        ax.text(x + 0.045, y + h - 0.032, titulo, ha="left", va="center", fontsize=9,
                fontweight="bold", color=color, zorder=4)
        ax.text(x + 0.016, y + h - 0.075, detalle, ha="left", va="top", fontsize=7.2,
                color=GRIS, linespacing=1.45, zorder=4)

    paso(0.02, 0.62, 0.22, 0.28, 1, "Responsable", "Abre «Nuevo préstamo», elige\ncolaborador, equipo, fechas\ny motivo.")
    paso(0.27, 0.62, 0.22, 0.28, 2, "React · formulario", "Valida campos, formato, fechas\n(RN-04) y observación de\n5 a 300 caracteres.")
    paso(0.52, 0.62, 0.22, 0.28, 3, "API · controller", "Recibe POST /api/prestamos\ncon JWT, verifica el rol y el\nDTO antes de continuar.")
    paso(0.77, 0.62, 0.22, 0.28, 4, "Application · RN", "Comprueba usuario activo,\nequipo disponible, RN-01,\nRN-02, RN-03 y RN-05.")

    flecha(ax, 0.24, 0.76, 0.27, 0.76)
    flecha(ax, 0.49, 0.76, 0.52, 0.76)
    flecha(ax, 0.74, 0.76, 0.77, 0.76)
    flecha(ax, 0.88, 0.62, 0.88, 0.42)

    paso(0.77, 0.12, 0.22, 0.28, 5, "Infrastructure", "INSERT del préstamo y\nUPDATE del equipo a estado\nPrestado, en una operación.")
    paso(0.52, 0.12, 0.22, 0.28, 6, "PostgreSQL 18", "COMMIT: el préstamo y el\nequipo quedan consistentes\nen TechAssetDB.")
    paso(0.27, 0.12, 0.22, 0.28, 7, "API · respuesta", "Devuelve 201 Created con\nel DTO completo (código\nPR- y relaciones).")
    paso(0.02, 0.12, 0.22, 0.28, 8, "React · confirmación", "Muestra banner y toast,\nlimpia el formulario y ofrece\nir al historial.", color=VERDE)

    flecha(ax, 0.77, 0.26, 0.74, 0.26)
    flecha(ax, 0.52, 0.26, 0.49, 0.26)
    flecha(ax, 0.27, 0.26, 0.24, 0.26)

    ax.text(0.5, 0.975, "Flujo de una operación de entrada: registro de un préstamo",
            ha="center", fontsize=11, fontweight="bold", color=AZUL_OSCURO)
    ax.text(0.5, 0.935, "Las validaciones del cliente mejoran la experiencia; las del servidor garantizan la integridad de los datos.",
            ha="center", fontsize=7.4, color=GRIS_CLARO, style="italic")
    guardar(fig, "flujo_prestamo.png")


# ---------------------------------------------------------------------------
# 4. Casos de uso
# ---------------------------------------------------------------------------
def casos_uso():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.972, "Casos de uso por actor", ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=AZUL_OSCURO)
    ax.text(0.5, 0.942, "El Administrador hereda las funciones del Responsable; el Responsable, las del Colaborador.",
            ha="center", va="center", fontsize=6.4, color=GRIS_CLARO, style="italic")

    ax.add_patch(FancyBboxPatch((0.012, 0.025), 0.976, 0.892,
                                boxstyle="round,pad=0.006,rounding_size=0.01",
                                facecolor=BLANCO, edgecolor="#CBD5E1", linewidth=1.1))

    actores = [
        ("Administrador", AZUL, 0.585),
        ("Responsable", VERDE, 0.752),
        ("Colaborador", AMBAR, 0.919),
    ]
    cabecera_y = 0.875
    ax.add_patch(mpatches.Rectangle((0.02, 0.835), 0.96, 0.072,
                                    facecolor="#F1F5FB", edgecolor="none"))
    ax.text(0.03, cabecera_y, "Caso de uso", fontsize=8.2, fontweight="bold",
            color=AZUL_OSCURO, va="center")

    for nombre, color, x in actores:
        ax.add_patch(mpatches.Circle((x, 0.898), 0.0105, facecolor="#E8EFFC",
                                     edgecolor=color, linewidth=1.1, zorder=5))
        ax.plot([x, x], [0.887, 0.866], color=color, linewidth=1.5, zorder=4)
        ax.plot([x - 0.013, x + 0.013], [0.879, 0.879], color=color, linewidth=1.4, zorder=4)
        ax.plot([x, x - 0.010], [0.866, 0.852], color=color, linewidth=1.3, zorder=4)
        ax.plot([x, x + 0.010], [0.866, 0.852], color=color, linewidth=1.3, zorder=4)
        ax.text(x, 0.842, nombre, ha="center", va="center", fontsize=7.2,
                fontweight="bold", color=color)

    ax.plot([0.505, 0.505], [0.14, 0.835], color="#E2E8F0", linewidth=0.8)
    for x in (0.668, 0.835):
        ax.plot([x, x], [0.14, 0.835], color="#E2E8F0", linewidth=0.8)

    filas = [
        ("Iniciar sesión y cambiar contraseña", {"Administrador", "Responsable", "Colaborador"}),
        ("Gestionar usuarios y accesos", {"Administrador"}),
        ("Gestionar equipos", {"Administrador", "Responsable"}),
        ("Registrar préstamo", {"Administrador", "Responsable"}),
        ("Registrar devolución", {"Administrador", "Responsable"}),
        ("Consultar inventario", {"Administrador", "Responsable", "Colaborador"}),
        ("Consultar historial y filtrar", {"Administrador", "Responsable", "Colaborador"}),
        ("Ver dashboard e indicadores", {"Administrador", "Responsable", "Colaborador"}),
        ("Solicitar equipo", {"Colaborador"}),
        ("Aprobar o rechazar solicitud", {"Administrador", "Responsable"}),
        ("Exportar reportes CSV", {"Administrador", "Responsable"}),
        ("Consultar movimientos", {"Administrador", "Responsable"}),
        ("Eliminar equipos sin historial", {"Administrador"}),
    ]

    y0 = 0.790
    dy = 0.053
    for i, (texto, permitidos) in enumerate(filas):
        y = y0 - i * dy
        if i % 2 == 0:
            ax.add_patch(mpatches.Rectangle((0.02, y - 0.031), 0.96, dy,
                                            facecolor="#F8FAFC", edgecolor="none", zorder=0))
        ax.text(0.03, y, texto, fontsize=8.0, color=GRIS, va="center", zorder=3)
        for nombre, color, x in actores:
            if nombre in permitidos:
                ax.scatter([x], [y], s=30, facecolor=color, edgecolor=BLANCO, linewidth=1.1, zorder=4)
            else:
                ax.text(x, y, "—", ha="center", va="center", fontsize=7,
                        color="#CBD5E1", zorder=3)

    ax.scatter([0.035], [0.055], s=22, facecolor=AZUL, edgecolor=BLANCO, linewidth=0.8, zorder=4)
    ax.text(0.048, 0.055, "Permitido", fontsize=6.5, color=GRIS, va="center")
    ax.text(0.135, 0.055, "—", fontsize=7, color="#CBD5E1", va="center")
    ax.text(0.147, 0.055, "No permitido", fontsize=6.5, color=GRIS, va="center")
    ax.text(0.985, 0.055, "Fuente: matriz de permisos del sistema", ha="right",
            fontsize=6.0, color="#94A3B8", style="italic", va="center")

    guardar(fig, "casos_uso.png")


# ---------------------------------------------------------------------------
# 5. Planificacion (Gantt con etiquetas al costado)
# ---------------------------------------------------------------------------
def planificacion():
    fig, ax = plt.subplots(figsize=(12, 4.9))
    actividades = [
        ("Análisis del caso, actores, RF y RN", 1, 1, "#93C5FD"),
        ("Diseño de arquitectura y modelo de datos", 1, 2, "#60A5FA"),
        ("Módulos de entrada: usuarios, equipos y préstamos", 2, 2, "#3B82F6"),
        ("Autenticación JWT, BCrypt y roles", 3, 1, "#1D4ED8"),
        ("Módulos de salida: consultas, filtros y reportes", 3, 2, "#1E40AF"),
        ("Integración frontend–API–PostgreSQL", 4, 2, "#16367F"),
        ("Refinamiento, componentes y accesibilidad", 5, 1, "#0EA5E9"),
        ("Pruebas funcionales, capturas e informe", 5, 2, "#047857"),
    ]
    nombres = [a[0] for a in actividades]
    for i, (_, inicio, duracion, color) in enumerate(actividades):
        y = len(actividades) - i - 1
        ax.barh(y, duracion, left=inicio - 0.5, height=0.55, color=color,
                edgecolor="white", linewidth=2)
    ax.set_yticks(range(len(actividades)))
    ax.set_yticklabels(list(reversed(nombres)), fontsize=8.2)
    ax.set_xticks(range(1, 7))
    ax.set_xticklabels(["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5", "Semana 6"], fontsize=8)
    ax.set_xlim(0.5, 6.5)
    ax.set_ylim(-0.6, len(actividades) - 0.4)
    ax.grid(axis="x", color="#E2E8F0", linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("Planificación incremental del proyecto (6 semanas)", fontsize=11,
                 fontweight="bold", color=AZUL_OSCURO, loc="left", pad=12)
    guardar(fig, "planificacion.png")


# ---------------------------------------------------------------------------
# 6. Mapa de componentes reutilizables
# ---------------------------------------------------------------------------
def componentes():
    fig, ax = plt.subplots(figsize=(12.6, 6.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.14, 0.94, "PÁGINAS", ha="center", fontsize=8.6, fontweight="bold", color=AZUL)
    paginas = ["Login", "Dashboard", "Usuarios", "Equipos", "Préstamos", "Nuevo préstamo", "Reportes"]
    for i, nombre in enumerate(paginas):
        y = 0.80 - i * 0.095
        ax.add_patch(FancyBboxPatch((0.02, y), 0.24, 0.075,
                                    boxstyle="round,pad=0.005,rounding_size=0.008",
                                    facecolor=AZUL_CLARO, edgecolor=AZUL_MEDIO, linewidth=1))
        ax.text(0.14, y + 0.0375, nombre, ha="center", va="center", fontsize=7.6,
                fontweight="bold", color=AZUL_OSCURO)

    ax.add_patch(FancyArrowPatch((0.28, 0.5), (0.34, 0.5), arrowstyle="-|>", mutation_scale=16,
                                 linewidth=1.6, color=AZUL_MEDIO))

    ax.text(0.66, 0.94, "COMPONENTES COMPARTIDOS", ha="center", fontsize=8.6,
            fontweight="bold", color=VERDE)
    grupos = [
        ("Formularios", "CampoTexto · CampoSelect · CampoArea\nBoton · validaciones reutilizables", 0.79),
        ("Tablas y estados", "TablaDatos · Paginacion · EstadoVacio\nCargando", 0.615),
        ("Diálogos", "Modal accesible · ModalAyuda\nConfirmaciones y devoluciones", 0.44),
        ("Indicadores", "TarjetaIndicador · BarrasDatos\nEncabezadoPagina", 0.265),
        ("Etiquetas e iconos", "EtiquetaEquipo · EtiquetaPrestamo\nEtiquetaRol · Iconos", 0.09),
    ]
    for titulo, detalle, y in grupos:
        ax.add_patch(FancyBboxPatch((0.35, y), 0.62, 0.135,
                                    boxstyle="round,pad=0.006,rounding_size=0.01",
                                    facecolor=BLANCO, edgecolor=VERDE, linewidth=1.2))
        ax.text(0.375, y + 0.098, titulo, ha="left", va="center", fontsize=8.2,
                fontweight="bold", color=VERDE)
        ax.text(0.375, y + 0.045, detalle, ha="left", va="center", fontsize=7.2,
                color=GRIS, linespacing=1.45)

    ax.text(0.5, 0.985, "Componentes reutilizables compartidos por los módulos", ha="center",
            fontsize=11, fontweight="bold", color=AZUL_OSCURO)
    guardar(fig, "componentes.png")


if __name__ == "__main__":
    arquitectura()
    modelo_datos()
    flujo_prestamo()
    casos_uso()
    planificacion()
    componentes()
