"""Exporta el informe de TechAsset a PDF en dos pasadas (índice paginado)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pymupdf
from docx import Document

BASE = Path(__file__).resolve().parents[1]
DOCX = BASE / "Informe_TechAsset_KevinCcente.docx"
COPIA = BASE / "Informe_TechAsset_KevinCcente_pdf.docx"
TEMPORAL = BASE / "Informe_TechAsset_KevinCcente_sin_pie.pdf"
FINAL = BASE / "Informe_TechAsset_KevinCcente.pdf"

sys.path.insert(0, str(BASE / "scripts"))
from informe_techasset import SECCIONES  # noqa: E402


def generar(paginas=None):
    entorno = os.environ.copy()
    if paginas:
        entorno["TOC_PAGES"] = json.dumps(paginas, ensure_ascii=False)
    else:
        entorno.pop("TOC_PAGES", None)
    subprocess.run([sys.executable, str(BASE / "scripts" / "informe_techasset.py")], check=True, env=entorno)


def quitar_pies(origen, destino):
    doc = Document(origen)
    for seccion in doc.sections:
        for parrafo in list(seccion.header.paragraphs):
            for run in list(parrafo.runs):
                run._r.getparent().remove(run._r)
        for parrafo in list(seccion.footer.paragraphs):
            for run in list(parrafo.runs):
                run._r.getparent().remove(run._r)
    doc.save(destino)


def exportar(docx, pdf):
    script = f"""
$ErrorActionPreference = 'Stop'
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.Options.UpdateFieldsAtPrint = $false
$doc = $word.Documents.Open('{docx}')
$doc.Repaginate()
$doc.SaveAs2('{pdf}', 17)
$doc.Close(0)
$word.Quit()
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", script], check=True, timeout=600)


def paginas_de(pdf):
    doc = pymupdf.open(pdf)
    textos = [" ".join(p.get_text().split()) for p in doc]
    doc.close()
    indice = [i for i, t in enumerate(textos) if t.count(".......") >= 5]
    inicio = max(indice) + 1 if indice else 0

    paginas = {}
    for _, titulo in SECCIONES:
        clave = " ".join(titulo.split())
        for i in range(inicio, len(textos)):
            if clave in textos[i]:
                paginas[titulo] = i + 1
                break
    return paginas


def enlazar(doc, paginas):
    paginas_indice = [
        i for i in range(min(6, doc.page_count)) if doc[i].get_text().count(".......") >= 5
    ]

    for i in paginas_indice:
        for enlace in list(doc[i].get_links()):
            if enlace.get("kind") == pymupdf.LINK_GOTO:
                doc[i].delete_link(enlace)

    for nivel, titulo in SECCIONES:
        destino = paginas.get(titulo)
        if not destino:
            continue
        for i in paginas_indice:
            for rect in doc[i].search_for(titulo):
                doc[i].insert_link(
                    {
                        "kind": pymupdf.LINK_GOTO,
                        "from": rect,
                        "page": destino - 1,
                        "to": pymupdf.Point(0, 0),
                    }
                )

    doc.set_toc([[nivel, titulo, paginas.get(titulo, 1)] for nivel, titulo in SECCIONES])


def numerar(entrada, salida, paginas):
    doc = pymupdf.open(entrada)
    total = doc.page_count
    for i, p in enumerate(doc):
        if i == 0:
            continue
        ancho, alto = p.rect.width, p.rect.height
        p.insert_text((72, 28), "Construcción de Software · TechAsset · UPLA 2026-II",
                      fontname="helv", fontsize=7, color=(0.49, 0.56, 0.66))
        p.draw_line(pymupdf.Point(60, 34), pymupdf.Point(ancho - 60, 34),
                    color=(0.84, 0.88, 0.93), width=0.5)
        p.insert_text((60, alto - 24), "Kevin Ccente Garcia", fontname="helv", fontsize=7,
                      color=(0.49, 0.56, 0.66))
        etiqueta = f"Página {i + 1} de {total}"
        largo = pymupdf.get_text_length(etiqueta, fontname="helv", fontsize=7)
        p.insert_text((ancho - 60 - largo, alto - 24), etiqueta, fontname="helv", fontsize=7,
                      color=(0.49, 0.56, 0.66))
        p.draw_line(pymupdf.Point(60, alto - 32), pymupdf.Point(ancho - 60, alto - 32),
                    color=(0.84, 0.88, 0.93), width=0.5)

    enlazar(doc, paginas)
    doc.save(salida, garbage=3, deflate=True)
    doc.close()
    print(f"PDF generado: {salida.name} ({total} páginas)")
    return total


def main():
    generar()
    quitar_pies(DOCX, COPIA)
    exportar(COPIA, TEMPORAL)
    paginas = paginas_de(TEMPORAL)
    print(f"Secciones localizadas: {len(paginas)} de {len(SECCIONES)}")
    faltantes = [t for _, t in SECCIONES if t not in paginas]
    for t in faltantes:
        print("  FALTA:", t)

    generar(paginas)
    quitar_pies(DOCX, COPIA)
    exportar(COPIA, TEMPORAL)
    numerar(TEMPORAL, FINAL, paginas)

    COPIA.unlink(missing_ok=True)
    TEMPORAL.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
