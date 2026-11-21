"""Recaptura de las evidencias de nuevo préstamo y reportes."""
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

        # Validación del formulario
        page.goto(f"{BASE}/prestamos/nuevo", wait_until="networkidle")
        page.wait_for_selector("#usuarioId")
        page.get_by_role("button", name="Registrar préstamo").click()
        page.wait_for_timeout(700)
        page.screenshot(path=str(SALIDA / "15-nuevo-prestamo-validacion.png"))
        print("captura 15")

        # Registro exitoso sin mensajes previos
        page.goto(f"{BASE}/prestamos/nuevo", wait_until="networkidle")
        page.wait_for_selector("#usuarioId")
        page.select_option("#usuarioId", label="Sandra Huanca Paredes · Desarrollo")
        page.select_option("#equipoId", label="TA-0006 · Computadora Dell OptiPlex 7010")
        page.fill("#observacion", "Implementación del nuevo portal interno durante la semana de integración.")
        page.get_by_role("button", name="Registrar préstamo").click()
        page.wait_for_selector(".confirmacion")
        page.wait_for_timeout(900)
        page.screenshot(path=str(SALIDA / "16-nuevo-prestamo-ok.png"))
        print("captura 16")

        # Reportes con el estado base del conjunto de datos
        page.goto(f"{BASE}/reportes", wait_until="networkidle")
        page.wait_for_timeout(1200)
        page.screenshot(path=str(SALIDA / "17-reportes.png"))
        print("captura 17")

        contexto.close()
        navegador.close()


if __name__ == "__main__":
    main()
