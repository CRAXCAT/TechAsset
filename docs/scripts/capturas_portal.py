"""Captura el portal público y las pantallas de acceso actualizadas."""
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "capturas"
BASE = "http://localhost:5173"


def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch()

        contexto = navegador.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1.5)
        page = contexto.new_page()
        page.goto(f"{BASE}/", wait_until="networkidle")
        page.wait_for_timeout(900)
        page.screenshot(path=str(SALIDA / "26-portal-publico.png"))

        page.goto(f"{BASE}/login", wait_until="networkidle")
        page.wait_for_timeout(600)
        page.screenshot(path=str(SALIDA / "01-login.png"))
        page.fill("#correo", "kevin.ccente@innovatech.pe")
        page.fill("#clave", "incorrecta")
        page.get_by_role("button", name="Ingresar").click()
        page.wait_for_timeout(900)
        page.screenshot(path=str(SALIDA / "02-login-error.png"))
        contexto.close()

        contexto = navegador.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        page = contexto.new_page()
        page.goto(f"{BASE}/", wait_until="networkidle")
        page.wait_for_timeout(900)
        page.screenshot(path=str(SALIDA / "27-portal-movil.png"))

        page.goto(f"{BASE}/login", wait_until="networkidle")
        page.wait_for_timeout(700)
        page.screenshot(path=str(SALIDA / "21-login-movil.png"))
        contexto.close()

        navegador.close()
        print("Capturas del portal y del acceso actualizadas.")


if __name__ == "__main__":
    main()
