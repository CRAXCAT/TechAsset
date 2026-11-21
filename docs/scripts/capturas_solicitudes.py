"""Capturas del flujo de solicitudes, aprobación y auditoría."""
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "capturas"
BASE = "http://localhost:5173"
ADMIN = ("kevin.ccente@innovatech.pe", "Tech.2026*")
COLABORADOR = ("rosa.quispe@innovatech.pe", "Tech.2026*")


def iniciar(page, credenciales):
    page.goto(f"{BASE}/login", wait_until="networkidle")
    page.fill("#correo", credenciales[0])
    page.fill("#clave", credenciales[1])
    page.get_by_role("button", name="Ingresar").click()
    page.wait_for_timeout(1500)


def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch()

        # -------------------- Colaborador --------------------
        contexto = navegador.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1.5)
        page = contexto.new_page()
        iniciar(page, COLABORADOR)
        page.wait_for_timeout(700)
        page.screenshot(path=str(SALIDA / "33-dashboard-colaborador.png"))

        page.goto(f"{BASE}/solicitudes", wait_until="networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SALIDA / "34-mis-solicitudes.png"))

        page.goto(f"{BASE}/solicitudes/nueva", wait_until="networkidle")
        page.wait_for_selector("#equipoId")
        page.screenshot(path=str(SALIDA / "35-nueva-solicitud.png"))

        page.get_by_role("button", name="Enviar solicitud").click()
        page.wait_for_timeout(700)
        page.screenshot(path=str(SALIDA / "36-nueva-solicitud-validacion.png"))

        page.reload(wait_until="networkidle")
        page.wait_for_selector("#equipoId")
        opcion = page.locator("#equipoId option", has_text="TA-0008").get_attribute("value")
        page.select_option("#equipoId", opcion)
        page.fill("#motivo", "Apoyo visual para la feria de reclutamiento del área de Recursos Humanos.")
        page.get_by_role("button", name="Enviar solicitud").click()
        page.wait_for_selector(".confirmacion")
        page.wait_for_timeout(900)
        page.screenshot(path=str(SALIDA / "37-solicitud-registrada.png"))

        page.goto(f"{BASE}/prestamos", wait_until="networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SALIDA / "38-mi-historial.png"))

        page.goto(f"{BASE}/equipos", wait_until="networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SALIDA / "39-equipos-colaborador.png"))
        contexto.close()

        # -------------------- Administrador --------------------
        contexto = navegador.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1.5)
        page = contexto.new_page()
        iniciar(page, ADMIN)
        page.goto(f"{BASE}/solicitudes", wait_until="networkidle")
        page.wait_for_timeout(900)
        page.screenshot(path=str(SALIDA / "28-solicitudes-admin.png"))

        page.get_by_role("button", name="Ver").first.click()
        page.wait_for_timeout(500)
        page.screenshot(path=str(SALIDA / "29-solicitud-detalle.png"))
        page.get_by_role("button", name="Cerrar", exact=True).click()
        page.wait_for_timeout(300)

        page.get_by_role("button", name="Revisar").first.click()
        page.wait_for_timeout(500)
        page.fill("#observacion-revision", "Aprobado. El colaborador recogerá el equipo en Soporte.")
        page.screenshot(path=str(SALIDA / "30-solicitud-aprobacion.png"))

        page.get_by_role("button", name="Aprobar y generar préstamo").click()
        page.wait_for_timeout(1400)
        page.screenshot(path=str(SALIDA / "31-solicitud-aprobada.png"))

        page.goto(f"{BASE}/movimientos", wait_until="networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SALIDA / "32-movimientos.png"))
        contexto.close()

        navegador.close()
        print("Capturas de solicitudes y auditoría generadas.")


if __name__ == "__main__":
    main()
