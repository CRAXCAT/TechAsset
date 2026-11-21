"""Capturas de evidencia de TechAsset con Playwright."""
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "capturas"
SALIDA.mkdir(exist_ok=True)
BASE = "http://localhost:5173"

ADMIN = ("kevin.ccente@innovatech.pe", "Tech.2026*")
RESPONSABLE = ("lucia.paredes@innovatech.pe", "Tech.2026*")
TEMPORAL = ("diego.flores@innovatech.pe", "Temporal.2026*")


def capturar(page, nombre, completo=False):
    page.wait_for_timeout(450)
    page.screenshot(path=str(SALIDA / f"{nombre}.png"), full_page=completo)
    print("captura", nombre)


def iniciar_sesion(page, credenciales):
    page.goto(f"{BASE}/login", wait_until="networkidle")
    page.fill("#correo", credenciales[0])
    page.fill("#clave", credenciales[1])
    page.get_by_role("button", name="Ingresar").click()
    page.wait_for_timeout(1200)


def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch()

        # ---------------- Escritorio: administrador ----------------
        contexto = navegador.new_context(viewport={"width": 1440, "height": 980}, device_scale_factor=1.5)
        page = contexto.new_page()

        page.goto(f"{BASE}/login", wait_until="networkidle")
        capturar(page, "01-login")

        page.fill("#correo", "kevin.ccente@innovatech.pe")
        page.fill("#clave", "incorrecta")
        page.get_by_role("button", name="Ingresar").click()
        page.wait_for_selector(".aviso--error")
        capturar(page, "02-login-error")

        iniciar_sesion(page, ADMIN)
        page.wait_for_selector(".rejilla-indicadores")
        capturar(page, "03-dashboard")

        # Modo oscuro
        page.get_by_role("button", name="Cambiar a tema oscuro").first.click()
        page.wait_for_timeout(600)
        capturar(page, "04-dashboard-oscuro")
        page.get_by_role("button", name="Cambiar a tema claro").first.click()
        page.wait_for_timeout(400)

        # Ayuda y atajos
        page.get_by_role("button", name="Ayuda y atajos").first.click()
        page.wait_for_selector(".ayuda")
        capturar(page, "05-ayuda")
        page.get_by_role("button", name="Entendido").click()
        page.wait_for_timeout(300)

        # Usuarios
        page.goto(f"{BASE}/usuarios", wait_until="domcontentloaded")
        page.wait_for_selector(".tabla")
        capturar(page, "06-usuarios")

        page.get_by_role("button", name="Nuevo usuario").click()
        page.wait_for_selector(".modal")
        page.get_by_role("button", name="Registrar usuario").click()
        page.wait_for_timeout(400)
        capturar(page, "07-usuarios-validacion")
        page.get_by_role("button", name="Cancelar").click()
        page.wait_for_timeout(300)

        # Equipos
        page.goto(f"{BASE}/equipos", wait_until="domcontentloaded")
        page.wait_for_selector(".tabla")
        capturar(page, "08-equipos")

        page.get_by_role("button", name="Nuevo equipo").click()
        page.wait_for_selector(".modal")
        page.get_by_role("button", name="Registrar equipo").click()
        page.wait_for_timeout(400)
        capturar(page, "09-equipos-validacion")
        page.get_by_role("button", name="Cancelar").click()
        page.wait_for_timeout(300)

        # Préstamos
        page.goto(f"{BASE}/prestamos", wait_until="domcontentloaded")
        page.wait_for_selector(".tabla")
        capturar(page, "10-prestamos")

        page.goto(f"{BASE}/prestamos?estado=Activo&area=Desarrollo", wait_until="domcontentloaded")
        page.wait_for_selector(".tabla")
        capturar(page, "11-prestamos-filtrados")

        page.get_by_role("button", name="Ver").first.click()
        page.wait_for_selector(".detalle")
        capturar(page, "12-prestamo-detalle")
        page.get_by_role("button", name="Cerrar", exact=True).click()
        page.wait_for_timeout(300)

        page.get_by_role("button", name="Devolver").first.click()
        page.wait_for_selector("#observacion-devolucion")
        capturar(page, "13-prestamo-devolucion")
        page.get_by_role("button", name="Cancelar").click()
        page.wait_for_timeout(300)

        # Nuevo préstamo
        page.goto(f"{BASE}/prestamos/nuevo", wait_until="domcontentloaded")
        page.wait_for_selector("#usuarioId")
        capturar(page, "14-nuevo-prestamo")

        page.get_by_role("button", name="Registrar préstamo").click()
        page.wait_for_timeout(500)
        capturar(page, "15-nuevo-prestamo-validacion")

        page.select_option("#usuarioId", label="Sandra Huanca Paredes · Desarrollo")
        page.select_option("#equipoId", label="TA-0006 · Computadora Dell OptiPlex 7010")
        page.fill("#observacion", "Implementación del nuevo portal interno durante la semana de integración.")
        page.get_by_role("button", name="Registrar préstamo").click()
        page.wait_for_selector(".confirmacion")
        capturar(page, "16-nuevo-prestamo-ok")

        # Reportes
        page.goto(f"{BASE}/reportes", wait_until="domcontentloaded")
        page.wait_for_timeout(1400)
        capturar(page, "17-reportes")

        # Página no encontrada
        page.goto(f"{BASE}/ruta-inexistente", wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        capturar(page, "18-no-encontrada")

        contexto.close()

        # ---------------- Cambio obligatorio de contraseña ----------------
        contexto = navegador.new_context(viewport={"width": 1440, "height": 980}, device_scale_factor=1.5)
        page = contexto.new_page()
        iniciar_sesion(page, TEMPORAL)
        page.wait_for_selector("#actual")
        capturar(page, "19-cambiar-clave")
        contexto.close()

        # ---------------- Rol Responsable: restricción visible ----------------
        contexto = navegador.new_context(viewport={"width": 1440, "height": 980}, device_scale_factor=1.5)
        page = contexto.new_page()
        iniciar_sesion(page, RESPONSABLE)
        page.goto(f"{BASE}/usuarios", wait_until="domcontentloaded")
        page.wait_for_selector(".tabla")
        capturar(page, "20-usuarios-responsable")
        contexto.close()

        # ---------------- Móvil ----------------
        contexto = navegador.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        page = contexto.new_page()
        page.goto(f"{BASE}/login", wait_until="networkidle")
        capturar(page, "21-login-movil")
        iniciar_sesion(page, ADMIN)
        page.wait_for_timeout(1200)
        capturar(page, "22-dashboard-movil")
        contexto.close()

        # ---------------- Swagger ----------------
        contexto = navegador.new_context(viewport={"width": 1440, "height": 1100}, device_scale_factor=1.5)
        page = contexto.new_page()
        page.goto("http://localhost:5143/swagger/index.html", wait_until="networkidle")
        page.wait_for_timeout(1500)
        capturar(page, "23-swagger")
        contexto.close()

        navegador.close()

    (RAIZ / "capturas" / "_listado.txt").write_text(
        "\n".join(sorted(f.name for f in SALIDA.glob("*.png"))), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
