"""Captura las altas exitosas de usuario y equipo para el anexo de evidencias."""
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "capturas"
BASE = "http://localhost:5173"


def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        contexto = navegador.new_context(viewport={"width": 1440, "height": 980}, device_scale_factor=1.5)
        page = contexto.new_page()

        page.goto(f"{BASE}/login", wait_until="networkidle")
        page.fill("#correo", "kevin.ccente@innovatech.pe")
        page.fill("#clave", "Tech.2026*")
        page.get_by_role("button", name="Ingresar").click()
        page.wait_for_timeout(1200)

        # Alta de usuario
        page.goto(f"{BASE}/usuarios", wait_until="networkidle")
        page.get_by_role("button", name="Nuevo usuario").click()
        page.wait_for_selector("#nombres")
        page.fill("#nombres", "Usuario")
        page.fill("#apellidos", "Evidencia")
        page.fill("#correo", "usuario.evidencia@innovatech.pe")
        page.select_option("#area", "Soporte")
        page.select_option("#rol", "Colaborador")
        page.fill("#claveTemporal", "Evidencia.2026*")
        page.get_by_role("button", name="Registrar usuario").click()
        page.wait_for_timeout(900)
        page.fill("#busqueda-usuario", "Evidencia")
        page.get_by_role("button", name="Buscar").click()
        page.wait_for_timeout(700)
        page.screenshot(path=str(SALIDA / "24-alta-usuario.png"))
        print("captura 24")

        # Alta de equipo
        page.goto(f"{BASE}/equipos", wait_until="networkidle")
        page.get_by_role("button", name="Nuevo equipo").click()
        page.wait_for_selector("#codigoPatrimonial")
        page.fill("#codigoPatrimonial", "TA-0099")
        page.fill("#nombre", "Proyector de prueba")
        page.select_option("#categoria", "Proyector")
        page.fill("#marca", "Epson")
        page.select_option("#estado", "Disponible")
        page.get_by_role("button", name="Registrar equipo").click()
        page.wait_for_timeout(900)
        page.fill("#busqueda-equipo", "TA-0099")
        page.get_by_role("button", name="Buscar").click()
        page.wait_for_timeout(700)
        page.screenshot(path=str(SALIDA / "25-alta-equipo.png"))
        print("captura 25")

        contexto.close()
        navegador.close()


if __name__ == "__main__":
    main()
