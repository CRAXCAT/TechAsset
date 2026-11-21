"""Genera el informe técnico completo de TechAsset (caso integrador Semana 12)."""
import json
import os
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
CAPTURAS = BASE / "capturas"
FIGURAS = BASE / "figuras"
CACHE = FIGURAS / "_cache"
SALIDA = BASE / "Informe_TechAsset_KevinCcente.docx"

AZUL = RGBColor(0x1D, 0x4E, 0xD8)
AZUL_OSCURO = RGBColor(0x16, 0x36, 0x7F)
GRIS = RGBColor(0x47, 0x55, 0x69)
GRIS_CLARO = RGBColor(0x7C, 0x8E, 0xA8)
VERDE = RGBColor(0x04, 0x78, 0x57)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
NEGRO = RGBColor(0x0F, 0x17, 0x2A)

ANCHO = 16.8
contador = {"figura": 0, "tabla": 0}

SECCIONES = [
    (1, "RESUMEN EJECUTIVO"),
    (1, "1. ANÁLISIS Y PLANIFICACIÓN"),
    (2, "1.1 Contexto y problemática"),
    (2, "1.2 Objetivos"),
    (2, "1.3 Alcance del sistema"),
    (2, "1.4 Actores y roles"),
    (2, "1.5 Requerimientos funcionales"),
    (2, "1.6 Reglas de negocio"),
    (2, "1.7 Requerimientos no funcionales"),
    (2, "1.8 Casos de uso"),
    (2, "1.9 Planificación del proyecto"),
    (2, "1.10 Tecnologías utilizadas"),
    (1, "2. ARQUITECTURA Y DISEÑO"),
    (2, "2.1 Arquitectura por capas"),
    (2, "2.2 Estructura del proyecto"),
    (2, "2.3 Modelo de datos"),
    (2, "2.4 Seguridad y control de acceso"),
    (2, "2.5 Catálogo de la API REST"),
    (2, "2.6 Estándares de codificación"),
    (1, "3. MÓDULOS DE ENTRADA"),
    (2, "3.1 Portal público y acceso"),
    (2, "3.2 Gestión de usuarios"),
    (2, "3.3 Gestión de equipos"),
    (2, "3.4 Registro de préstamos"),
    (2, "3.5 Registro de devoluciones"),
    (2, "3.6 Validación en dos capas"),
    (2, "3.7 Solicitud y aprobación de equipos"),
    (1, "4. REUTILIZACIÓN Y REFINAMIENTO"),
    (2, "4.1 Organización del frontend"),
    (2, "4.2 Componentes reutilizables"),
    (2, "4.3 Hooks personalizados"),
    (2, "4.4 Servicios y cliente API"),
    (2, "4.5 Catálogo centralizado y DTO"),
    (2, "4.6 Refinamientos aplicados"),
    (2, "4.7 Métricas y beneficios"),
    (1, "5. MÓDULOS DE SALIDA"),
    (2, "5.1 Consultas y filtros"),
    (2, "5.2 Búsqueda y paginación"),
    (2, "5.3 Dashboard e indicadores"),
    (2, "5.4 Reportes y gráficos"),
    (2, "5.5 Exportación de datos"),
    (2, "5.6 Detalle y trazabilidad"),
    (2, "5.7 Historial por rol y auditoría"),
    (1, "6. INTEGRACIÓN DE MÓDULOS"),
    (2, "6.1 Flujo integral"),
    (2, "6.2 Integración frontend y API"),
    (2, "6.3 Integración API y persistencia"),
    (2, "6.4 Base de datos y migraciones"),
    (2, "6.5 Evidencias de integración"),
    (2, "6.6 Consistencia de las operaciones"),
    (2, "6.7 Aprobación transaccional"),
    (1, "7. EVALUACIÓN FUNCIONAL"),
    (2, "7.1 Estrategia de pruebas"),
    (2, "7.2 Pruebas de API"),
    (2, "7.3 Pruebas de interfaz"),
    (2, "7.4 Trazabilidad de requerimientos"),
    (2, "7.5 Cobertura de reglas de negocio"),
    (2, "7.6 Resultados y análisis"),
    (1, "8. USABILIDAD Y GUÍA DE USO"),
    (2, "8.1 Nielsen y Shneiderman"),
    (2, "8.2 Ayuda y atajos"),
    (2, "8.3 Modo oscuro y diseño móvil"),
    (2, "8.4 Flujo de uso recomendado"),
    (2, "8.5 Credenciales de demostración"),
    (1, "9. CONCLUSIONES Y RECOMENDACIONES"),
    (2, "9.1 Conclusiones"),
    (2, "9.2 Limitaciones"),
    (2, "9.3 Trabajo futuro"),
    (2, "9.4 Reflexión final"),
    (1, "REFERENCIAS"),
    (1, "ANEXOS"),
    (2, "Anexo A. Estructura de carpetas"),
    (2, "Anexo B. Instalación y ejecución"),
    (2, "Anexo C. Escenarios de prueba ejecutados"),
    (2, "Anexo D. Altas de usuario y equipo"),
    (2, "Anexo E. Portal público de inicio"),
    (2, "Anexo F. Solicitudes y auditoría"),
    (2, "Anexo G. Pruebas de integridad"),
    (2, "Anexo H. Repositorio público"),
]


# --------------------------------------------------------------------------
# Utilidades de formato
# --------------------------------------------------------------------------
def estilos(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(9.8)
    normal.font.color.rgb = NEGRO
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.line_spacing = 1.12
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")

    h1 = doc.styles["Heading 1"]
    h1.font.name = "Arial"
    h1.font.size = Pt(14)
    h1.font.bold = True
    h1.font.color.rgb = AZUL
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(5)
    h1.paragraph_format.keep_with_next = True

    h2 = doc.styles["Heading 2"]
    h2.font.name = "Arial"
    h2.font.size = Pt(11.2)
    h2.font.bold = True
    h2.font.color.rgb = AZUL_OSCURO
    h2.paragraph_format.space_before = Pt(8)
    h2.paragraph_format.space_after = Pt(3)
    h2.paragraph_format.keep_with_next = True

    cap = doc.styles.add_style("Pie breve", 1)
    cap.base_style = doc.styles["Normal"]
    cap.font.name = "Arial"
    cap.font.size = Pt(8)
    cap.font.italic = True
    cap.font.color.rgb = GRIS
    cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(8)

    nota = doc.styles.add_style("Nota", 1)
    nota.base_style = doc.styles["Normal"]
    nota.font.name = "Arial"
    nota.font.size = Pt(8.4)
    nota.font.color.rgb = GRIS
    nota.paragraph_format.space_after = Pt(4)
    nota.paragraph_format.left_indent = Cm(0.3)
    nota.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def pagina(doc):
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.top_margin, s.bottom_margin = Cm(1.8), Cm(1.6)
    s.left_margin, s.right_margin = Cm(2.1), Cm(2.1)
    s.header_distance, s.footer_distance = Cm(0.9), Cm(0.8)
    s.different_first_page_header_footer = True
    return s


def campo(p, instruccion, valor="1"):
    ini = OxmlElement("w:fldChar")
    ini.set(qn("w:fldCharType"), "begin")
    ins = OxmlElement("w:instrText")
    ins.set(qn("xml:space"), "preserve")
    ins.text = instruccion
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t")
    t.text = valor
    fin = OxmlElement("w:fldChar")
    fin.set(qn("w:fldCharType"), "end")
    run = p.add_run()
    run._r.append(ini)
    run._r.append(ins)
    run._r.append(sep)
    run._r.append(t)
    run._r.append(fin)


def decoracion(doc):
    s = doc.sections[0]
    enc = s.header.paragraphs[0]
    enc.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = enc.add_run("Construcción de Software · TechAsset · UPLA 2026-II")
    r.font.size = Pt(7.5)
    r.font.color.rgb = GRIS_CLARO
    borde = OxmlElement("w:pBdr")
    inf = OxmlElement("w:bottom")
    inf.set(qn("w:val"), "single")
    inf.set(qn("w:sz"), "4")
    inf.set(qn("w:color"), "D7E0EC")
    borde.append(inf)
    enc._p.get_or_add_pPr().append(borde)

    pie = s.footer.paragraphs[0]
    pie.paragraph_format.tab_stops.add_tab_stop(Cm(ANCHO), 2)
    r = pie.add_run("Kevin Ccente Garcia")
    r.font.size = Pt(7.5)
    r.font.color.rgb = GRIS_CLARO
    pie.add_run("\t")
    r = pie.add_run("Página ")
    r.font.size = Pt(7.5)
    r.font.color.rgb = GRIS_CLARO
    campo(pie, "PAGE")
    r = pie.add_run(" de ")
    r.font.size = Pt(7.5)
    r.font.color.rgb = GRIS_CLARO
    campo(pie, "NUMPAGES")


def par(doc, texto, negrita=False, cursiva=False, tamano=None, alineacion=None, color=None, espacio=4):
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.bold = negrita
    r.italic = cursiva
    if tamano:
        r.font.size = Pt(tamano)
    if color:
        r.font.color.rgb = color
    if alineacion is not None:
        p.alignment = alineacion
    p.paragraph_format.space_after = Pt(espacio)
    return p


def vineta(doc, texto, tamano=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(texto)
    if tamano:
        r.font.size = Pt(tamano)
    return p


def sombra(celda, color):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def bordes(tabla, color="C3D4FF"):
    tblPr = tabla._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{lado}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        b.append(e)
    tblPr.append(b)


def margenes(tabla, arriba=35, abajo=35, izq=65, der=65):
    tblPr = tabla._tbl.tblPr
    m = OxmlElement("w:tblCellMar")
    for nombre, valor in (("top", arriba), ("left", izq), ("bottom", abajo), ("right", der)):
        e = OxmlElement(f"w:{nombre}")
        e.set(qn("w:w"), str(valor))
        e.set(qn("w:type"), "dxa")
        m.append(e)
    tblPr.append(m)


def tabla(doc, cabeceras, filas, anchos, titulo, fuente=8.0):
    contador["tabla"] += 1
    num = contador["tabla"]
    cap = doc.add_paragraph(style="Pie breve")
    cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cap.paragraph_format.space_after = Pt(2)
    cap.paragraph_format.keep_with_next = True
    r = cap.add_run(f"Tabla {num}. ")
    r.bold = True
    r.italic = False
    cap.add_run(titulo)

    t = doc.add_table(rows=1, cols=len(cabeceras))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    t.style = "Table Grid"
    bordes(t)
    margenes(t)

    fila = t.rows[0]
    fila._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    fila._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for i, texto in enumerate(cabeceras):
        c = fila.cells[i]
        c.width = Cm(anchos[i])
        sombra(c, "1D4ED8")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_with_next = True
        r = p.add_run(texto)
        r.bold = True
        r.font.size = Pt(fuente)
        r.font.color.rgb = BLANCO
        r.font.name = "Arial"

    for idx, datos in enumerate(filas):
        celdas = t.add_row().cells
        t.rows[-1]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for i, valor in enumerate(datos):
            c = celdas[i]
            c.width = Cm(anchos[i])
            if idx % 2 == 1:
                sombra(c, "F8FAFC")
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(str(valor))
            r.font.size = Pt(fuente)
            r.font.name = "Arial"

    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def preparar(ruta, ancho=1700):
    CACHE.mkdir(parents=True, exist_ok=True)
    destino = CACHE / f"{ruta.stem}_{ancho}.png"
    if destino.exists() and destino.stat().st_mtime >= ruta.stat().st_mtime:
        return destino
    im = Image.open(ruta).convert("RGB")
    if im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    im.save(destino, optimize=True)
    return destino


def figura(doc, ruta, titulo, ancho=11.5):
    contador["figura"] += 1
    num = contador["figura"]
    ruta = Path(ruta)
    if not ruta.exists():
        print("FALTA FIGURA", ruta)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(preparar(ruta)), width=Cm(ancho))
    cap = doc.add_paragraph(style="Pie breve")
    r = cap.add_run(f"Figura {num}. ")
    r.bold = True
    r.italic = False
    cap.add_run(titulo)


def codigo(doc, lineas, titulo=None):
    if titulo:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(titulo)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = GRIS
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    bordes(t, "E3E9F2")
    margenes(t, 55, 55, 90, 90)
    c = t.rows[0].cells[0]
    c.width = Cm(ANCHO)
    sombra(c, "F6F8FC")
    for i, linea in enumerate(lineas):
        p = c.paragraphs[0] if i == 0 else c.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(linea)
        r.font.name = "Consolas"
        r.font.size = Pt(7.8)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def nota(doc, texto):
    p = doc.add_paragraph(style="Nota")
    r = p.add_run("Nota. ")
    r.bold = True
    p.add_run(texto)
    return p


# --------------------------------------------------------------------------
# Portada, índice y resumen
# --------------------------------------------------------------------------
def portada(doc):
    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    p.add_run().add_picture(str(FIGURAS / "upla-logo.png"), width=Cm(2.7))

    par(doc, "UNIVERSIDAD PERUANA LOS ANDES", negrita=True, tamano=13,
        alineacion=WD_ALIGN_PARAGRAPH.CENTER, color=AZUL_OSCURO, espacio=2)
    par(doc, "FACULTAD DE INGENIERÍA", tamano=10.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio=1)
    par(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS Y COMPUTACIÓN", tamano=10.5,
        alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio=14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    p.add_run().add_picture(str(FIGURAS / "logo-techasset.png"), width=Cm(2.2))

    par(doc, "INFORME TÉCNICO DEL CASO PRÁCTICO INTEGRADOR", negrita=True, tamano=11,
        alineacion=WD_ALIGN_PARAGRAPH.CENTER, color=GRIS, espacio=4)
    par(doc, "TechAsset: Sistema de Gestión de Inventario y Préstamo de Equipos Tecnológicos",
        negrita=True, tamano=18, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color=AZUL, espacio=6)
    par(doc,
        "Aplicación web con autenticación por roles, validación de reglas de negocio, consultas, "
        "reportes y dashboard, construida con React, ASP.NET Core y PostgreSQL",
        cursiva=True, tamano=9.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color=GRIS, espacio=20)

    datos = [
        ("Asignatura", "Construcción de Software"),
        ("Caso", "Caso práctico integrador · Semana 12"),
        ("Estudiante", "Kevin Ccente Garcia"),
        ("Docente", "Jorge Alberto Vega Flores"),
        ("Ciclo académico", "IX"),
        ("Periodo académico", "2026-II"),
    ]
    t = doc.add_table(rows=0, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for etiqueta, valor in datos:
        c = t.add_row().cells
        c[0].width, c[1].width = Cm(4.6), Cm(8.8)
        p0 = c[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p0.add_run(etiqueta)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = GRIS
        p0.paragraph_format.space_after = Pt(2)
        p1 = c[1].paragraphs[0]
        r = p1.add_run(valor)
        r.font.size = Pt(9.5)
        p1.paragraph_format.space_after = Pt(2)

    for _ in range(7):
        doc.add_paragraph()

    par(doc, "HUANCAYO - PERÚ", negrita=True, tamano=10, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio=1)
    par(doc, "2026", negrita=True, tamano=10, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()


def enlace_interno(parrafo, texto, ancla, tamano, negrita, color):
    enlace = OxmlElement("w:hyperlink")
    enlace.set(qn("w:anchor"), ancla)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fuentes = OxmlElement("w:rFonts")
    fuentes.set(qn("w:ascii"), "Arial")
    fuentes.set(qn("w:hAnsi"), "Arial")
    rPr.append(fuentes)
    if negrita:
        rPr.append(OxmlElement("w:b"))
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(tamano * 2)))
    rPr.append(sz)
    color_xml = OxmlElement("w:color")
    color_xml.set(qn("w:val"), "%02X%02X%02X" % (color[0], color[1], color[2]))
    rPr.append(color_xml)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = texto
    run.append(t)
    enlace.append(run)
    parrafo._p.append(enlace)


def marcar_secciones(doc):
    indice_actual = 0
    for parrafo in doc.paragraphs:
        if indice_actual >= len(SECCIONES):
            break
        if parrafo.style.name not in ("Heading 1", "Heading 2"):
            continue
        nivel, titulo = SECCIONES[indice_actual]
        if parrafo.text.strip() != titulo:
            continue
        start = OxmlElement("w:bookmarkStart")
        start.set(qn("w:id"), str(100 + indice_actual))
        start.set(qn("w:name"), f"sec_{indice_actual + 1}")
        end = OxmlElement("w:bookmarkEnd")
        end.set(qn("w:id"), str(100 + indice_actual))
        if parrafo._p.pPr is not None:
            parrafo._p.pPr.addnext(start)
        else:
            parrafo._p.insert(0, start)
        parrafo._p.append(end)
        indice_actual += 1
    print(f"Marcadores creados: {indice_actual} de {len(SECCIONES)}")


def indice(doc):
    par(doc, "ÍNDICE", negrita=True, tamano=12.5, color=AZUL, espacio=5)
    paginas = json.loads(os.environ.get("TOC_PAGES", "{}"))

    for posicion, (nivel, titulo) in enumerate(SECCIONES, start=1):
        p = doc.add_paragraph()
        f = p.paragraph_format
        f.tab_stops.add_tab_stop(Cm(ANCHO), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        f.space_after = Pt(0)
        f.space_before = Pt(1.5 if nivel == 1 else 0)
        f.left_indent = Cm(0 if nivel == 1 else 0.5)
        f.alignment = WD_ALIGN_PARAGRAPH.LEFT
        f.line_spacing = 0.95
        enlace_interno(
            p,
            titulo,
            f"sec_{posicion}",
            8.4 if nivel == 1 else 7.9,
            nivel == 1,
            AZUL_OSCURO if nivel == 1 else GRIS,
        )
        p.add_run("\t")
        n = p.add_run(str(paginas.get(titulo, "")))
        n.font.size = Pt(8)

    doc.add_page_break()


def resumen(doc):
    doc.add_heading("RESUMEN EJECUTIVO", level=1)
    par(doc,
        "TechAsset es una aplicación web desarrollada para Innovatech Solutions S.A.C. que centraliza el "
        "inventario de equipos tecnológicos y el registro de préstamos y devoluciones. La empresa administra "
        "laptops, computadoras de escritorio, monitores, impresoras, tablets, proyectores y equipos de red "
        "mediante hojas de cálculo, lo que provoca pérdida de información, duplicidad de registros, falta de "
        "control de préstamos y desconocimiento de la ubicación de los equipos. La solución reemplaza ese "
        "proceso por una SPA con portal público de inicio, autenticación real, autorización por roles, formularios validados, consultas "
        "con filtros, solicitudes con aprobación, auditoría de movimientos, reportes exportables y un dashboard con seis indicadores.")
    par(doc,
        "El sistema se construyó con una arquitectura por capas (Domain, Application, Infrastructure y API), "
        "Entity Framework Core, PostgreSQL 18, BCrypt para contraseñas, JWT para sesiones y una interfaz React "
        "con componentes reutilizables. Se implementaron los 17 requerimientos funcionales y las 10 reglas de "
        "negocio del caso, tres actores, tres tablas del núcleo y dos tablas de extensión (Solicitudes y Movimientos), "
        "además de los seis indicadores solicitados. La verificación funcional ejecutó 50 escenarios de API y 12 "
        "comprobaciones directas de integridad en PostgreSQL, todos conformes; además se documentaron 40 capturas de "
        "interfaz y 6 diagramas técnicos. El backend compila sin errores ni advertencias y el frontend se empaqueta en 82 módulos.")

    banda = doc.add_table(rows=1, cols=6)
    banda.alignment = WD_TABLE_ALIGNMENT.CENTER
    banda.autofit = False
    datos_banda = [
        ("17", "REQUERIMIENTOS"),
        ("10", "REGLAS DE NEGOCIO"),
        ("6", "INDICADORES"),
        ("26", "ENDPOINTS"),
        ("50/50", "PRUEBAS DE API"),
        ("40", "CAPTURAS"),
    ]
    for i, (valor, etiqueta) in enumerate(datos_banda):
        c = banda.rows[0].cells[i]
        c.width = Cm(2.8)
        sombra(c, "1D4ED8")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(valor)
        r.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = BLANCO
        p2 = c.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(etiqueta)
        r2.font.size = Pt(6.3)
        r2.font.color.rgb = BLANCO

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    par(doc, "Ficha del proyecto", negrita=True, tamano=10.5, color=AZUL, espacio=4)

    datos = [
        ("Producto", "TechAsset · Gestión de inventario y préstamo de equipos tecnológicos"),
        ("Organización", "Innovatech Solutions S.A.C."),
        ("Arquitectura", "React 19 · ASP.NET Core 10 · Entity Framework Core 10 · PostgreSQL 18"),
        ("Capas", "Domain · Application · Infrastructure · API · SPA"),
        ("Módulos", "Portal público, acceso, dashboard, usuarios, equipos, solicitudes, préstamos, devoluciones, reportes y auditoría"),
        ("Seguridad", "BCrypt, JWT con rol y área, contraseña temporal, rutas privadas y alcance por rol"),
        ("Datos", "5 tablas (3 de núcleo + 2 de extensión) · 18 equipos · 13 usuarios · 17 préstamos · 4 solicitudes"),
        ("Entorno local", "Portal http://localhost:5173/ · API http://localhost:5143 · Panel /panel"),
        ("Documentación", "Swagger/OpenAPI, README y scripts de datos y pruebas"),
    ]
    ficha = doc.add_table(rows=0, cols=2)
    ficha.autofit = False
    for etiqueta, valor in datos:
        c = ficha.add_row().cells
        c[0].width, c[1].width = Cm(3.8), Cm(12.8)
        p0 = c[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(etiqueta)
        r0.bold = True
        r0.font.size = Pt(8.2)
        r0.font.color.rgb = GRIS
        p1 = c[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(valor)
        r1.font.size = Pt(8.2)

    nota(doc,
         "Los conteos corresponden al conjunto de datos de demostración cargado con docs/scripts/seed.py. "
         "Las pruebas de API agregan, aprueban, devuelven y rechazan registros temporales, por lo que el resumen "
         "puede variar durante su ejecución; los datos se restauran con docs/scripts/reiniciar_datos.py.")

    par(doc, "Correspondencia con la rúbrica de evaluación", negrita=True, tamano=10.5,
        color=AZUL, espacio=4)
    tabla(
        doc,
        ["Criterio", "Peso", "Secciones", "Evidencia principal"],
        [
            ("1. Análisis y planificación", "3", "1.1 a 1.10",
             "Problema, actores, 17 RF, 10 RN, 4 reglas de integridad, casos de uso, Gantt y estándares."),
            ("2. Módulos de entrada", "3", "3.1 a 3.7",
             "Formularios de usuarios, equipos, préstamos, solicitudes y validación en dos capas."),
            ("3. Reutilización y refinamiento", "3", "4.1 a 4.7",
             "22 componentes, 10 hooks, 8 servicios y 13 refinamientos documentados."),
            ("4. Módulos de salida", "4", "5.1 a 5.7",
             "Consultas, filtros, paginación, dashboard, reportes, CSV, detalle y auditoría."),
            ("5. Integración de módulos", "3", "6.1 a 6.7",
             "React-API-PostgreSQL, transacciones, aprobación, migraciones, Swagger y evidencias."),
            ("6. Evaluación funcional", "4", "7.1 a 7.6, 8 y 9",
             "50/50 pruebas de API, 12/12 comprobaciones de integridad, 40 capturas y trazabilidad."),
        ],
        [4.8, 1.2, 3.0, 7.8],
        "Correspondencia entre la rúbrica y el contenido del informe.",
        fuente=7.6,
    )


# --------------------------------------------------------------------------
# 1. Análisis y planificación
# --------------------------------------------------------------------------
def seccion_1(doc):
    doc.add_heading("1. ANÁLISIS Y PLANIFICACIÓN", level=1)
    doc.add_heading("1.1 Contexto y problemática", level=2)
    par(doc,
        "Innovatech Solutions S.A.C. es una empresa de desarrollo de soluciones tecnológicas con más de 500 "
        "colaboradores distribuidos en áreas funcionales. Cada área utiliza laptops, computadoras de escritorio, "
        "monitores, impresoras, tablets, proyectores y equipos de red para sus actividades. El control de esos "
        "activos se realiza con hojas de cálculo y registros manuales, lo que genera cinco problemas recurrentes: "
        "pérdida de información, duplicidad de registros, falta de control de los préstamos, desconocimiento de la "
        "ubicación de los equipos y dificultad para conocer la disponibilidad real.")
    par(doc,
        "El problema central es la ausencia de una fuente única de verdad. Un equipo puede aparecer como disponible "
        "en una hoja y estar asignado en otra; no existe trazabilidad de quién lo tiene, desde cuándo y con qué "
        "responsable; y los reportes se construyen manualmente, por lo que llegan tarde o con errores. TechAsset "
        "resuelve este problema con un registro único de usuarios y equipos, un historial de préstamos con estados "
        "controlados, reglas de negocio verificadas en el servidor y consultas que permiten tomar decisiones con "
        "datos actuales.")
    par(doc,
        "El caso práctico integrador de la Semana 12 exige integrar los módulos construidos durante el curso en un "
        "sistema funcional. Por ello, el proyecto no se limita a pantallas aisladas: incluye autenticación, "
        "persistencia, validaciones en dos capas, componentes reutilizables, refinamiento, módulos de salida, "
        "integración y una evaluación funcional con evidencias.")

    doc.add_heading("1.2 Objetivos", level=2)
    par(doc, "Objetivo general", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    par(doc,
        "Desarrollar e integrar un sistema web que gestione el inventario y el préstamo de equipos tecnológicos de "
        "Innovatech Solutions S.A.C., aplicando buenas prácticas de construcción de software, validaciones, "
        "reutilización de componentes y evaluación funcional con evidencias.")
    par(doc, "Objetivos específicos", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    for texto in [
        "Analizar el problema, identificar a los actores, los 17 requerimientos funcionales y las 10 reglas de negocio.",
        "Diseñar una arquitectura por capas y un modelo relacional de tres tablas de núcleo y dos de extensión que garantice integridad y trazabilidad.",
        "Implementar formularios de usuarios, equipos y préstamos con validaciones completas en frontend y backend.",
        "Construir componentes reutilizables, hooks y servicios que reduzcan la duplicación y faciliten el mantenimiento.",
        "Desarrollar consultas, filtros, búsquedas, reportes y un dashboard con los seis indicadores solicitados.",
        "Integrar React, ASP.NET Core y PostgreSQL y verificar el funcionamiento con pruebas y capturas de evidencia.",
    ]:
        vineta(doc, texto)

    doc.add_heading("1.3 Alcance del sistema", level=2)
    par(doc,
        "El alcance incluye el portal público de inicio, la autenticación con roles, la gestión de usuarios y equipos, el registro de préstamos y "
        "devoluciones, la consulta del inventario y del historial, el dashboard y la exportación de reportes en CSV. "
        "Quedan fuera del alcance el envío automático de correos, la recuperación automática de contraseña, la "
        "integración con directorios corporativos, la firma digital, la aplicación móvil nativa y el despliegue en "
        "infraestructura cloud. El sistema se ejecuta en un entorno local con la API en el puerto 5143 y la SPA en "
        "el 5173.")
    par(doc,
        "El sistema incorpora una ampliación coherente con las funciones de los actores: el Colaborador registra una "
        "solicitud, el Responsable de Tecnología la aprueba o rechaza, y la aprobación genera el préstamo dentro de "
        "una transacción. La solicitud no reserva el equipo: la disponibilidad se vuelve a verificar al aprobar. El "
        "Responsable y el Administrador conservan el registro directo de préstamos para operaciones presenciales. "
        "También se añadieron auditoría de movimientos, historial limitado al propio colaborador y un portal público "
        "de orientación. Estas extensiones complementan los 17 requerimientos y las 10 reglas del caso; no los sustituyen.")

    doc.add_heading("1.4 Actores y roles", level=2)
    par(doc,
        "El sistema reconoce tres actores. El rol se almacena en la tabla Usuarios, se incluye como claim del token JWT "
        "y se verifica tanto en la interfaz como en los controladores mediante [Authorize(Roles = ...)].")
    tabla(
        doc,
        ["Actor", "Responsabilidad principal", "Funciones en TechAsset"],
        [
            ("Administrador", "Administra la información y supervisa la operación.",
             "Gestiona usuarios y equipos, aprueba o rechaza solicitudes, registra préstamos y devoluciones, consulta reportes y auditoría."),
            ("Responsable de Tecnología", "Controla la asignación y el estado de los equipos.",
             "Registra y actualiza equipos, aprueba o rechaza solicitudes, registra préstamos y devoluciones, consulta inventario, disponibilidad e historial."),
            ("Colaborador", "Solicita equipos y consulta su disponibilidad.",
             "Consulta el inventario, registra solicitudes y revisa únicamente su propio historial; no modifica equipos, usuarios ni préstamos."),
        ],
        [3.8, 4.2, 8.8],
        "Actores del sistema y funciones permitidas.",
    )
    tabla(
        doc,
        ["Acción", "Administrador", "Responsable", "Colaborador"],
        [
            ("Iniciar sesión y cambiar su contraseña", "Sí", "Sí", "Sí"),
            ("Consultar usuarios", "Sí", "Sí", "No"),
            ("Registrar y actualizar usuarios", "Sí", "No", "No"),
            ("Deshabilitar usuarios", "Sí", "No", "No"),
            ("Consultar inventario", "Sí", "Sí", "Sí"),
            ("Registrar y actualizar equipos", "Sí", "Sí", "No"),
            ("Eliminar equipos sin historial", "Sí", "No", "No"),
            ("Solicitar equipo", "No", "No", "Sí"),
            ("Aprobar o rechazar solicitudes", "Sí", "Sí", "No"),
            ("Registrar préstamos y devoluciones", "Sí", "Sí", "No"),
            ("Consultar historial", "Sí (global)", "Sí (global)", "Sí (propio)"),
            ("Consultar dashboard", "Sí", "Sí", "Sí (propio)"),
            ("Exportar CSV", "Sí", "Sí", "No"),
            ("Consultar movimientos", "Sí", "Sí", "No"),
        ],
        [7.0, 3.2, 3.2, 3.2],
        "Matriz de permisos por rol.",
    )

    doc.add_heading("1.5 Requerimientos funcionales", level=2)
    par(doc,
        "Los 17 requerimientos del caso se implementaron en la API y en la interfaz. La tabla siguiente relaciona "
        "cada uno con su realización concreta y con la sección donde se evidencia.")
    tabla(
        doc,
        ["Código", "Requerimiento", "Implementación lograda", "Evidencia"],
        [
            ("RF-01", "Registrar usuarios.", "Modal con nombres, apellidos, correo @innovatech.pe, área, rol y contraseña temporal; alta con BCrypt y cambio obligatorio.", "3.2 / Fig. 7-8 / Anexo D"),
            ("RF-02", "Actualizar usuarios.", "Edición de nombres, apellidos, correo, área y rol; validación de correo único (RN-08).", "3.2"),
            ("RF-03", "Consultar usuarios.", "Directorio con búsqueda y filtros por área, rol y estado.", "5.1 / Fig. 7"),
            ("RF-04", "Deshabilitar usuarios.", "PATCH /api/usuarios/{id}/activo, exclusivo del Administrador (RN-09); bloqueo si tiene préstamos activos.", "3.2 / A-05"),
            ("RF-05", "Registrar equipos.", "Alta con código patrimonial único, nombre, categoría, marca y estado.", "3.3 / Fig. 9-10 / Anexo D"),
            ("RF-06", "Actualizar equipos.", "Edición con validación de código único y protección del estado Prestado.", "3.3"),
            ("RF-07", "Consultar inventario.", "Tabla con búsqueda por código, nombre o marca, filtros por categoría y estado.", "5.1 / Fig. 9"),
            ("RF-08", "Actualizar estado del equipo.", "Cambio a Disponible, Mantenimiento o Baja; Prestado solo se asigna al registrar un préstamo.", "3.3 / E-03"),
            ("RF-09", "Registrar préstamo.", "Formulario con colaborador, equipo disponible, fechas y motivo; transacción que registra el préstamo y actualiza el equipo.", "3.4 / Fig. 11-13"),
            ("RF-10", "Registrar devolución.", "Devolución con fecha real y observación obligatoria; el equipo vuelve a Disponible.", "3.5 / Fig. 14"),
            ("RF-11", "Consultar historial de préstamos.", "Historial paginado con búsqueda, estado, área, equipo y rango de fechas; filtros en la URL.", "5.1 / Fig. 16-17"),
            ("RF-12", "Consultar préstamos activos.", "Filtro estado=Activo, indicador de pendientes y panel de préstamos activos.", "5.1 / Fig. 16"),
            ("RF-13", "Visualizar dashboard general.", "Panel con seis indicadores, alertas y gráficos de distribución.", "5.3 / Fig. 18"),
            ("RF-14", "Consultar equipos por estado.", "Gráfico de barras y listados de disponibles y prestados en Reportes.", "5.4 / Fig. 19"),
            ("RF-15", "Consultar equipos más utilizados.", "Ranking por cantidad de préstamos históricos, calculado en el servidor.", "5.4 / Fig. 19"),
            ("RF-16", "Consultar préstamos por área.", "Agrupación por área y destacado del área con mayor uso.", "5.4 / Fig. 19"),
            ("RF-17", "Consultar historial de movimientos.", "Detalle del préstamo y auditoría de movimientos con actor, fecha y acción.", "5.6 / 5.7 / Fig. 20 y 36"),
        ],
        [1.4, 4.6, 8.4, 2.4],
        "Requerimientos funcionales y su implementación.",
        fuente=7.4,
    )
    par(doc,
        "Además de los 17 requerimientos mínimos, se incorporaron cinco ampliaciones coherentes con las funciones de "
        "los actores. No reemplazan ni cambian los códigos del caso: se documentan como extensiones verificables.")
    tabla(
        doc,
        ["Código", "Ampliación", "Implementación", "Evidencia"],
        [
            ("EF-01", "Solicitud de equipo.", "El Colaborador elige un equipo disponible, fechas y motivo; la solicitud queda Pendiente y no reserva el equipo.", "3.7 / Anexo F / S-01"),
            ("EF-02", "Aprobación o rechazo.", "El Responsable aprueba y genera el préstamo en una transacción, o rechaza con observación obligatoria.", "3.7 / 6.7 / S-04, S-08"),
            ("EF-03", "Historial por rol.", "El Colaborador solo consulta sus préstamos y solicitudes; Administración y Tecnología ven el historial global.", "5.7 / R-19, S-10"),
            ("EF-04", "Auditoría de movimientos.", "Cada préstamo, devolución, solicitud y revisión registra actor, fecha, entidad y detalle.", "5.7 / S-16 / Anexo G"),
            ("EF-05", "Portal público de inicio.", "Portada informativa con funciones, seguridad, roles y acceso corporativo, sin exponer datos operativos.", "3.1 / Anexo E"),
        ],
        [1.4, 4.2, 8.6, 2.6],
        "Ampliaciones funcionales sobre los requerimientos mínimos.",
        fuente=7.4,
    )

    doc.add_heading("1.6 Reglas de negocio", level=2)
    par(doc,
        "Las reglas se implementan en la capa Application y se refuerzan con restricciones de base de datos. Ninguna "
        "regla depende solo de la interfaz: una petición directa a la API también se rechaza con el código HTTP "
        "correspondiente. Las diez reglas del caso se complementan con cuatro reglas de integridad para solicitudes, "
        "alcance por rol y auditoría.")
    tabla(
        doc,
        ["Código", "Regla del caso", "Control implementado", "HTTP / prueba"],
        [
            ("RN-01", "Un equipo solo puede estar asociado a un préstamo activo.", "Consulta de préstamo activo por equipo dentro del servicio; bloqueo antes de insertar.", "409 / R-02"),
            ("RN-02", "No se presta un equipo en Mantenimiento.", "Validación del estado del equipo antes de crear el préstamo.", "409 / R-03"),
            ("RN-03", "No se presta un equipo en Baja.", "Validación del estado del equipo antes de crear el préstamo.", "409 / R-04"),
            ("RN-04", "La devolución debe ser posterior al préstamo.", "Comparación de DateOnly en el DTO y en el servicio.", "409 / R-05"),
            ("RN-05", "Todo préstamo registra un responsable.", "ResponsableId obtenido del token JWT; solo Administrador o Responsable pueden crear.", "403 / R-15"),
            ("RN-06", "No se elimina un equipo con historial de préstamos.", "Verificación de préstamos asociados antes de eliminar; se sugiere marcarlo como Baja.", "409 / E-04"),
            ("RN-07", "El código patrimonial debe ser único.", "Validación en el servicio e índice único en PostgreSQL.", "409 / E-01"),
            ("RN-08", "El correo del usuario debe ser único.", "Validación en el servicio e índice único en PostgreSQL.", "409 / U-01"),
            ("RN-09", "Solo el Administrador deshabilita usuarios.", "[Authorize(Roles = \"Administrador\")] y control visual del botón.", "403 / A-05"),
            ("RN-10", "Toda devolución registra observaciones.", "DTO con longitud mínima y validación en el servicio.", "400 / R-09"),
            ("RN-11", "Una sola solicitud pendiente por equipo.", "Verificación en el servicio e índice único parcial (EquipoId) WHERE Estado = 'Pendiente'.", "409 / S-02, DB-07"),
            ("RN-12", "Solicitud aprobada exige préstamo; pendiente o rechazada no lo admite.", "CHECK CK_Solicitudes_Aprobacion y control en la transacción de aprobación.", "DB-05, DB-06"),
            ("RN-13", "El Colaborador solo consulta su propio historial.", "Filtro por UsuarioId en la consulta y verificación de propiedad en el detalle.", "200 / R-19, S-10"),
            ("RN-14", "Solo Administración y Tecnología consultan la auditoría.", "[Authorize(Roles = \"Administrador,Responsable\")] en /api/movimientos.", "403 / A-08"),
        ],
        [1.4, 5.4, 7.8, 2.2],
        "Reglas de negocio, control y evidencia.",
        fuente=7.5,
    )

    doc.add_heading("1.7 Requerimientos no funcionales", level=2)
    tabla(
        doc,
        ["Atributo", "Requisito", "Cómo se cumple"],
        [
            ("Usabilidad", "Curva de aprendizaje corta y tareas claras.", "Navegación lateral, una acción primaria por pantalla, ayudas, atajos y mensajes explicativos."),
            ("Accesibilidad", "Uso con teclado y lectores de pantalla.", "Foco visible, etiquetas asociadas, aria-live, cierre con Esc, contraste y modo oscuro."),
            ("Seguridad", "Credenciales protegidas y acceso por roles.", "BCrypt, JWT firmado, expiración, [Authorize(Roles)], CORS y contraseña temporal."),
            ("Rendimiento", "Consultas ágiles con datos crecientes.", "Paginación en servidor, índices por estado y fecha, proyecciones DTO y debounce visual."),
            ("Mantenibilidad", "Cambios localizados y código legible.", "Arquitectura por capas, componentes, hooks, servicios, catálogo y validadores puros."),
            ("Portabilidad", "Ejecución en Windows o Linux.", "Configuración por appsettings y variables de entorno; PostgreSQL y .NET multiplataforma."),
            ("Confiabilidad", "Operaciones de préstamo consistentes.", "Transacción de base de datos para insertar el préstamo y actualizar el equipo."),
            ("Escalabilidad", "Crecimiento de usuarios y registros.", "API sin estado, JWT, paginación, consultas agregadas y separación de responsabilidades."),
        ],
        [2.8, 5.0, 9.0],
        "Requerimientos no funcionales.",
    )

    doc.add_heading("1.8 Casos de uso", level=2)
    par(doc,
        "Los casos de uso se agrupan por actor y por módulo. Los siete escenarios mínimos exigidos por el caso "
        "(registrar usuario, registrar equipo, registrar préstamo, registrar devolución, consultar inventario, "
        "consultar historial y consultar dashboard) se ejecutaron y documentaron con capturas. La Figura 1 resume, "
        "en forma de matriz, qué casos puede ejecutar cada actor; el detalle de los escenarios se presenta en la "
        "tabla siguiente.")
    figura(doc, FIGURAS / "casos_uso.png", "Matriz de casos de uso y actores del sistema.", ancho=16.2)
    tabla(
        doc,
        ["Código", "Caso de uso", "Actor principal", "Resultado esperado"],
        [
            ("CU-01", "Registrar usuario", "Administrador", "Cuenta creada con contraseña temporal y correo único."),
            ("CU-02", "Registrar equipo", "Administrador / Responsable", "Equipo registrado con código único y estado válido."),
            ("CU-03", "Registrar préstamo", "Responsable / Administrador", "Préstamo activo y equipo en estado Prestado."),
            ("CU-04", "Registrar devolución", "Responsable / Administrador", "Préstamo devuelto y equipo disponible."),
            ("CU-05", "Consultar inventario", "Todos", "Listado filtrable por texto, categoría y estado."),
            ("CU-06", "Consultar historial", "Todos", "Historial paginado con filtros y detalle."),
            ("CU-07", "Consultar dashboard", "Todos", "Seis indicadores actualizados desde el servidor."),
            ("CU-08", "Solicitar equipo", "Colaborador", "Solicitud pendiente registrada sin reservar el equipo."),
            ("CU-09", "Revisar solicitud", "Responsable / Administrador", "Solicitud aprobada o rechazada con observación."),
            ("CU-10", "Consultar movimientos", "Administrador / Responsable", "Auditoría filtrable de las operaciones."),
        ],
        [1.5, 5.0, 4.5, 5.8],
        "Casos de uso mínimos verificados.",
    )

    doc.add_heading("1.9 Planificación del proyecto", level=2)
    par(doc,
        "Se adoptó un ciclo de vida incremental e iterativo. Cada semana produjo un incremento verificable y se "
        "probaron las reglas antes de avanzar. Este modelo se justifica porque el caso se construye de forma "
        "acumulativa, porque permite corregir el diseño con retroalimentación temprana y porque la separación por "
        "capas facilita sustituir o ampliar módulos sin reescribir el sistema.")
    figura(doc, FIGURAS / "planificacion.png", "Planificación incremental de seis semanas.", ancho=16.0)
    tabla(
        doc,
        ["Fase", "Semanas", "Actividades principales", "Entregable"],
        [
            ("1. Análisis", "1", "Problema, actores, RF, RN, alcance y ciclo de vida.", "Documento de análisis y repositorio inicial."),
            ("2. Diseño", "1-2", "Arquitectura por capas, modelo de datos, estándares y catálogos.", "Diagramas y migración inicial."),
            ("3. Entradas", "2-3", "Formularios de usuarios, equipos, préstamos y solicitudes; validaciones y seguridad.", "Módulos de entrada funcionales."),
            ("4. Salidas", "3-4", "Consultas, filtros, paginación, dashboard, reportes, historial por rol y auditoría.", "Módulos de salida funcionales."),
            ("5. Integración", "4-5", "Conexión React-API-PostgreSQL, transacciones y navegación completa.", "Sistema integrado."),
            ("6. Evaluación", "5-6", "Pruebas de API e integridad, interfaz, capturas e informe.", "Evidencias e informe técnico."),
        ],
        [3.0, 1.8, 8.0, 4.0],
        "Fases, semanas y entregables del proyecto.",
    )

    doc.add_heading("1.10 Tecnologías utilizadas", level=2)
    par(doc,
        "La selección prioriza tecnologías maduras, multiplataforma y coherentes con el stack sugerido por el caso. "
        "Se usó ASP.NET Core 10 en lugar de la versión 8 porque es la versión instalada en el entorno y mantiene "
        "compatibilidad con las APIs de EF Core y JWT utilizadas; el código no depende de características exclusivas "
        "de una versión superior.")
    tabla(
        doc,
        ["Capa", "Tecnología", "Versión", "Uso en el proyecto"],
        [
            ("Backend", "ASP.NET Core", "10", "Controladores REST, middleware, autorización y Swagger."),
            ("Backend", "Entity Framework Core", "10", "Mapeo objeto-relacional, migraciones y consultas LINQ."),
            ("Backend", "Npgsql", "10", "Proveedor de PostgreSQL para EF Core."),
            ("Backend", "BCrypt.Net-Next", "4", "Hash seguro de contraseñas con sal."),
            ("Backend", "JWT Bearer", "10", "Autenticación sin estado con claims de rol y área."),
            ("Datos", "PostgreSQL", "18", "Base TechAssetDB con cinco tablas (tres de núcleo y dos de extensión) e índices."),
            ("Frontend", "React", "19", "SPA con componentes, hooks y contexto."),
            ("Frontend", "Vite", "8", "Servidor de desarrollo y empaquetado."),
            ("Frontend", "CSS propio", "—", "Sistema de diseño, variables, modo oscuro y responsive."),
            ("Pruebas", "Playwright / Python", "—", "Capturas automatizadas y pruebas de API."),
        ],
        [2.4, 4.8, 2.2, 7.4],
        "Tecnologías y herramientas del proyecto.",
    )
    nota(doc,
         "No se utilizó Tailwind CSS: se construyó un sistema de diseño propio con variables CSS, lo que permitió "
         "controlar el modo oscuro, la accesibilidad y la consistencia sin dependencias adicionales. El resultado "
         "mantiene los mismos principios de componentes y utilidades que propone el caso.")


# --------------------------------------------------------------------------
# 2. Arquitectura y diseño
# --------------------------------------------------------------------------
def seccion_2(doc):
    doc.add_heading("2. ARQUITECTURA Y DISEÑO", level=1)
    doc.add_heading("2.1 Arquitectura por capas", level=2)
    par(doc,
        "El backend sigue una arquitectura por capas con dependencias dirigidas hacia el dominio. Domain contiene las "
        "entidades y el catálogo; Application define DTO, interfaces, filtros, excepciones y servicios; Infrastructure "
        "implementa repositorios, DbContext, unidad de trabajo, BCrypt y JWT; API expone controladores, middleware y "
        "Swagger. El frontend se organiza por responsabilidad y consume la API mediante un cliente único.")
    figura(doc, FIGURAS / "arquitectura.png", "Arquitectura por capas y flujo de una operación.", ancho=16.4)
    tabla(
        doc,
        ["Capa", "Responsabilidad", "Contenido principal"],
        [
            ("Domain", "Modelo del negocio y valores válidos.", "Usuario, Equipo, Prestamo, Solicitud, Movimiento y CatalogoTechAsset."),
            ("Application", "Casos de uso, reglas RN-01 a RN-14 y contratos.", "DTO, filtros, interfaces, servicios, solicitudes, auditoría y excepciones."),
            ("Infrastructure", "Persistencia, seguridad y transacciones.", "AppDbContext, repositorios, UnitOfWork, BCrypt, JWT y migraciones."),
            ("API", "Exposición HTTP, autorización y errores.", "Controladores, middleware, CORS, Swagger, alcance por rol y configuración."),
            ("Frontend", "Presentación y experiencia de usuario.", "Rutas, layouts, páginas, componentes, hooks y servicios."),
        ],
        [3.0, 6.4, 7.4],
        "Responsabilidades por capa.",
    )
    par(doc,
        "La regla de dependencia se respeta: los controladores no contienen reglas de negocio y los servicios no "
        "conocen detalles de HTTP. Esto permitió cambiar la implementación de repositorios y agregar transacciones sin "
        "modificar los casos de uso, y facilita probar la lógica con dobles de prueba.")

    doc.add_heading("2.2 Estructura del proyecto", level=2)
    par(doc,
        "El repositorio separa backend, frontend y documentación. La estructura del backend refleja las capas; la del "
        "frontend separa páginas, componentes, hooks, servicios y utilidades. Los scripts de datos, capturas y pruebas "
        "viven en docs/scripts para que el sistema sea reproducible.")
    codigo(doc, [
        "TechAsset/",
        "├─ backend/",
        "│  ├─ TechAsset.Domain/          Entidades y catálogo",
        "│  ├─ TechAsset.Application/     DTO, filtros, interfaces, servicios y reglas",
        "│  ├─ TechAsset.Infrastructure/  DbContext, repositorios, UnitOfWork, seguridad y migraciones",
        "│  ├─ TechAsset.API/             Controladores, middleware, Program.cs y Swagger",
        "│  └─ TechAsset.slnx",
        "├─ frontend/",
        "│  ├─ src/components/            layout, ui y RutaPrivada",
        "│  ├─ src/pages/                 Inicio, Login, Dashboard, Usuarios, Equipos, Prestamos, Reportes",
        "│  ├─ src/hooks/                 useUsuarios, useEquipos, usePrestamos, useResumen, useSolicitudes, useMovimientos, useCatalogos, useTema",
        "│  ├─ src/services/              api, auth, usuarios, equipos, prestamos, solicitudes, movimientos y reportes",
        "│  ├─ src/utils/                 constantes, formato y validaciones",
        "│  └─ src/styles/app.css         sistema de diseño y modo oscuro",
        "└─ docs/",
        "   ├─ capturas/                 27 evidencias de interfaz",
        "   ├─ figuras/                  diagramas y logotipo",
        "   ├─ scripts/                  seed, reinicio, pruebas, capturas e informe",
        "   └─ Informe_TechAsset_KevinCcente.pdf / .docx",
    ])
    nota(doc,
         "La estructura se mantuvo estable durante el refinamiento: los cambios se concentraron en componentes, hooks "
         "y servicios, sin reorganizar carpetas ni romper importaciones.")

    par(doc, "Componentes del backend", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    tabla(
        doc,
        ["Capa / carpeta", "Componente", "Responsabilidad"],
        [
            ("API · Controllers", "Auth, Usuarios, Equipos, Prestamos, Solicitudes, Movimientos, Reportes", "Reciben DTO, aplican autorización y devuelven códigos HTTP coherentes."),
            ("API · Middleware", "ManejadorErroresMiddleware", "Traduce excepciones y validaciones a 400, 401, 403, 404, 409 o 500."),
            ("Application · Services", "Auth, Usuario, Equipo, Prestamo, Solicitud, Movimiento, Reporte", "Casos de uso y reglas RN-01 a RN-14; no conocen HTTP."),
            ("Application · DTO", "AuthDtos, TechAssetDtos, ResultadoPaginado", "Contratos de entrada y salida con DataAnnotations."),
            ("Application · Contracts", "Repositorios, ISolicitudRepository, IMovimientoService, IUnitOfWork, IPasswordHasher, ITokenGenerator", "Inversión de dependencias y transacciones."),
            ("Domain · Entities", "Usuario, Equipo, Prestamo", "Modelo del negocio y relaciones."),
            ("Domain · Constants", "CatalogoTechAsset", "Roles, áreas, categorías y estados válidos."),
            ("Infrastructure · Data", "AppDbContext, UnitOfWork, InicializadorDatos", "Mapeo EF Core, transacción y administrador inicial."),
            ("Infrastructure · Repositories", "Usuario, Equipo, Prestamo, Solicitud, Movimiento", "Consultas LINQ, paginación y persistencia."),
            ("Infrastructure · Security", "PasswordHasher, JwtTokenGenerator", "Hash BCrypt y emisión de tokens JWT."),
        ],
        [4.2, 6.2, 6.4],
        "Componentes del backend y su responsabilidad.",
        fuente=7.4,
    )

    par(doc, "Componentes del frontend", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    tabla(
        doc,
        ["Capa / carpeta", "Componente", "Responsabilidad"],
        [
            ("routes", "AppRoutes", "Rutas públicas (portal y login) y privadas (panel y módulos)."),
            ("layouts", "AppLayout", "Estructura común con barra lateral, cabecera, contenido y pie."),
            ("components/layout", "Sidebar, Topbar", "Navegación, sesión, tema, ayuda y estado de la API."),
            ("components/ui", "22 componentes", "Campos, tabla, modal, paginación, indicadores, barras, etiquetas y estados."),
            ("pages", "Inicio, Login, Dashboard, Usuarios, Equipos, Solicitudes, NuevaSolicitud, Prestamos, NuevoPrestamo, Reportes, Movimientos, CambiarClave, NoEncontrada", "Composición de vistas y estado local."),
            ("hooks", "useUsuarios, useEquipos, usePrestamos, useResumen, useSolicitudes, useMovimientos, useCatalogos, useTema", "Carga de datos, recarga y preferencia de tema."),
            ("context", "AuthContext, ToastContext", "Sesión, token, roles y notificaciones."),
            ("services", "api, auth, usuario, equipo, prestamo, solicitud, movimiento, reporte", "Contratos HTTP y descarga de reportes."),
            ("utils", "constantes, formato, validaciones", "Catálogos, fechas, moneda y validación pura."),
        ],
        [3.6, 7.4, 5.8],
        "Componentes del frontend y su responsabilidad.",
        fuente=7.4,
    )

    doc.add_heading("2.3 Modelo de datos", level=2)
    par(doc,
        "PostgreSQL 18 almacena tres tablas de núcleo —Usuarios, Equipos y Prestamos— y dos tablas de extensión: "
        "Solicitudes y Movimientos. La tabla Usuarios amplía el modelo referencial del caso con Rol, PasswordHash, "
        "Activo y DebeCambiarPassword para soportar la autenticación real y RN-09. Equipos conserva el código "
        "patrimonial único y el estado operativo. Prestamos relaciona al solicitante, al equipo y al responsable. "
        "Solicitudes registra la petición previa del Colaborador y su vínculo con el préstamo aprobado. Movimientos "
        "conserva la auditoría de las operaciones.")
    figura(doc, FIGURAS / "modelo_datos.png", "Modelo relacional del núcleo de TechAsset.", ancho=16.2)
    tabla(
        doc,
        ["Tabla", "Campos principales", "Restricciones y relaciones"],
        [
            ("Usuarios", "Id, Nombres, Apellidos, Correo, Area, Rol, Activo, PasswordHash, DebeCambiarPassword, FechaRegistro.",
             "PK Id; índice único en Correo; índice por Area; 1:N con Prestamos como solicitante y como responsable."),
            ("Equipos", "Id, CodigoPatrimonial, Nombre, Categoria, Marca, Estado, FechaRegistro.",
             "PK Id; índice único en CodigoPatrimonial; índice por Estado; 1:N con Prestamos."),
            ("Prestamos", "Id, UsuarioId, EquipoId, ResponsableId, FechaPrestamo, FechaDevolucion, FechaDevolucionReal, Observacion, ObservacionDevolucion, Estado, FechaRegistro.",
             "PK Id; FK a Usuarios (dos) y Equipos con ON DELETE RESTRICT; índices (EquipoId, Estado) y (UsuarioId, FechaPrestamo); único parcial del equipo activo."),
            ("Solicitudes", "Id, UsuarioId, EquipoId, PrestamoId, FechaPrestamo, FechaDevolucion, Motivo, Estado, ObservacionRevision, RevisadoPorId, Fechas de registro y revisión.",
             "PK Id; FK a Usuarios (solicitante y revisor), Equipos y Prestamos con RESTRICT; único parcial por equipo pendiente y por PrestamoId."),
            ("Movimientos", "Id, Fecha, Entidad, EntidadId, Accion, Detalle, UsuarioId, UsuarioNombre.",
             "PK Id; sin FK polimórfica para conservar el evento; índices por Fecha y (Entidad, EntidadId)."),
        ],
        [2.4, 8.6, 5.8],
        "Estructura de la base de datos.",
        fuente=7.5,
    )
    par(doc,
        "El diccionario siguiente precisa el tipo, la nulabilidad y la restricción de cada campo. Se usa uuid como clave "
        "primaria, varchar con longitudes acotadas para los textos, boolean para los indicadores, date para las fechas "
        "del préstamo y timestamp con zona horaria para los sellos de auditoría. La columna Activo equivale al Estado "
        "booleano del modelo referencial del caso.")
    tabla(
        doc,
        ["Tabla", "Campo", "Tipo", "Nulo", "Restricción"],
        [
            ("Usuarios", "Id", "uuid", "No", "PK"),
            ("Usuarios", "Nombres", "varchar(100)", "No", "—"),
            ("Usuarios", "Apellidos", "varchar(100)", "No", "—"),
            ("Usuarios", "Correo", "varchar(150)", "No", "UNIQUE · formato @innovatech.pe"),
            ("Usuarios", "Area", "varchar(100)", "No", "Catálogo de áreas"),
            ("Usuarios", "Rol", "varchar(30)", "No", "Administrador / Responsable / Colaborador"),
            ("Usuarios", "Activo", "boolean", "No", "Default true"),
            ("Usuarios", "PasswordHash", "varchar(300)", "No", "Hash BCrypt"),
            ("Usuarios", "DebeCambiarPassword", "boolean", "No", "Default false"),
            ("Usuarios", "FechaRegistro", "timestamptz", "No", "UTC"),
            ("Equipos", "Id", "uuid", "No", "PK"),
            ("Equipos", "CodigoPatrimonial", "varchar(50)", "No", "UNIQUE · mayúsculas"),
            ("Equipos", "Nombre", "varchar(100)", "No", "—"),
            ("Equipos", "Categoria", "varchar(50)", "No", "Catálogo de categorías"),
            ("Equipos", "Marca", "varchar(50)", "No", "—"),
            ("Equipos", "Estado", "varchar(30)", "No", "Disponible / Prestado / Mantenimiento / Baja"),
            ("Equipos", "FechaRegistro", "timestamptz", "No", "UTC"),
            ("Prestamos", "Id", "uuid", "No", "PK"),
            ("Prestamos", "UsuarioId", "uuid", "No", "FK Usuarios (solicitante) · RESTRICT"),
            ("Prestamos", "EquipoId", "uuid", "No", "FK Equipos · RESTRICT"),
            ("Prestamos", "ResponsableId", "uuid", "No", "FK Usuarios (responsable) · RESTRICT"),
            ("Prestamos", "FechaPrestamo", "date", "No", "—"),
            ("Prestamos", "FechaDevolucion", "date", "No", "> FechaPrestamo (RN-04)"),
            ("Prestamos", "FechaDevolucionReal", "date", "Sí", "Se asigna al devolver"),
            ("Prestamos", "Observacion", "varchar(300)", "No", "5–300 caracteres"),
            ("Prestamos", "ObservacionDevolucion", "varchar(300)", "Sí", "5–300 al devolver (RN-10)"),
            ("Prestamos", "Estado", "varchar(30)", "No", "Activo / Devuelto"),
            ("Prestamos", "FechaRegistro", "timestamptz", "No", "UTC"),
            ("Solicitudes", "Id", "uuid", "No", "PK"),
            ("Solicitudes", "UsuarioId", "uuid", "No", "FK Usuarios (solicitante) · RESTRICT"),
            ("Solicitudes", "EquipoId", "uuid", "No", "FK Equipos · RESTRICT"),
            ("Solicitudes", "PrestamoId", "uuid", "Sí", "FK Prestamos · único si no es nulo"),
            ("Solicitudes", "FechaPrestamo", "date", "No", "—"),
            ("Solicitudes", "FechaDevolucion", "date", "No", "> FechaPrestamo"),
            ("Solicitudes", "Motivo", "varchar(300)", "No", "5–300 caracteres"),
            ("Solicitudes", "Estado", "varchar(30)", "No", "Pendiente / Aprobada / Rechazada"),
            ("Solicitudes", "ObservacionRevision", "varchar(300)", "Sí", "Obligatoria al rechazar"),
            ("Solicitudes", "RevisadoPorId", "uuid", "Sí", "FK Usuarios (revisor) · RESTRICT"),
            ("Solicitudes", "FechaRegistro / FechaRevision", "timestamptz", "No / Sí", "UTC"),
            ("Movimientos", "Id", "uuid", "No", "PK"),
            ("Movimientos", "Fecha", "timestamptz", "No", "UTC · índice"),
            ("Movimientos", "Entidad", "varchar(30)", "No", "Prestamo / Solicitud / Equipo / Usuario"),
            ("Movimientos", "EntidadId", "uuid", "No", "Referencia lógica"),
            ("Movimientos", "Accion", "varchar(30)", "No", "Registrar / Devolver / Crear / Aprobar / Rechazar"),
            ("Movimientos", "Detalle", "varchar(300)", "No", "Descripción del evento"),
            ("Movimientos", "UsuarioId / UsuarioNombre", "uuid / varchar(150)", "Sí / No", "Instantánea del actor"),
        ],
        [2.2, 4.4, 3.2, 1.2, 5.8],
        "Diccionario de datos de TechAsset.",
        fuente=7.0,
    )
    tabla(
        doc,
        ["Objeto", "Definición", "Propósito"],
        [
            ("PK_Usuarios / PK_Equipos / PK_Prestamos", "Clave primaria uuid.", "Identidad única de cada fila."),
            ("UQ_Usuarios_Correo", "Índice único en Correo.", "RN-08 y autenticación sin ambigüedad."),
            ("UQ_Equipos_CodigoPatrimonial", "Índice único en CodigoPatrimonial.", "RN-07 y búsqueda por código."),
            ("IX_Usuarios_Area", "Índice no único en Area.", "Filtro por área en usuarios y reportes."),
            ("IX_Equipos_Estado", "Índice no único en Estado.", "Consulta de disponibles y prestados."),
            ("IX_Prestamos_Equipo_Estado", "Índice compuesto (EquipoId, Estado).", "Verificación de préstamo activo (RN-01)."),
            ("IX_Prestamos_Usuario_Fecha", "Índice compuesto (UsuarioId, FechaPrestamo).", "Historial por colaborador y fecha."),
            ("IX_Prestamos_EquipoActivo", "Índice único parcial (EquipoId) WHERE Estado = 'Activo'.", "Impide dos préstamos activos del mismo equipo incluso con concurrencia."),
            ("IX_Solicitudes_EquipoPendiente", "Índice único parcial (EquipoId) WHERE Estado = 'Pendiente'.", "Una sola solicitud pendiente por equipo."),
            ("IX_Solicitudes_Prestamo", "Índice único parcial (PrestamoId) WHERE PrestamoId IS NOT NULL.", "Una solicitud aprobada por préstamo."),
            ("CK_Prestamos_Fechas", "CHECK FechaDevolucion > FechaPrestamo.", "RN-04 aplicada también en PostgreSQL."),
            ("CK_Solicitudes_Aprobacion", "CHECK de coherencia entre Estado y PrestamoId.", "Aprobada exige préstamo; Pendiente/Rechazada lo mantienen nulo."),
            ("CK_Usuarios / CK_Equipos", "CHECK de rol, correo, estado y código canónicos.", "Defensa en profundidad de los catálogos."),
            ("FK_Prestamos_Usuarios / Equipos", "Tres claves foráneas con ON DELETE RESTRICT.", "Conservar el historial y evitar huérfanos."),
        ],
        [5.4, 6.2, 5.2],
        "Índices y restricciones de integridad.",
        fuente=7.3,
    )
    par(doc,
        "El borrado restringido protege el historial: no se puede eliminar un usuario o un equipo que tenga préstamos. "
        "La unicidad de correo y código patrimonial se valida en el servicio y se refuerza con índices únicos, de modo "
        "que una condición de carrera tampoco genere duplicados. El estado del equipo se deriva del ciclo del préstamo: "
        "Disponible → Prestado al registrar, y Prestado → Disponible al devolver; Mantenimiento y Baja son estados "
        "administrativos que no permiten préstamo. La migración SolicitudesAuditoria incorpora las dos tablas de "
        "extensión, los índices únicos parciales y las reglas CHECK; se aplicó sobre la base existente sin borrar datos.")
    codigo(doc, [
        "ALTER TABLE \"Prestamos\"",
        "  ADD CONSTRAINT \"FK_Prestamos_Usuarios_UsuarioId\"",
        "  FOREIGN KEY (\"UsuarioId\") REFERENCES \"Usuarios\" (\"Id\") ON DELETE RESTRICT;",
        "",
        "ALTER TABLE \"Prestamos\"",
        "  ADD CONSTRAINT \"FK_Prestamos_Equipos_EquipoId\"",
        "  FOREIGN KEY (\"EquipoId\") REFERENCES \"Equipos\" (\"Id\") ON DELETE RESTRICT;",
        "",
        "ALTER TABLE \"Prestamos\"",
        "  ADD CONSTRAINT \"FK_Prestamos_Usuarios_ResponsableId\"",
        "  FOREIGN KEY (\"ResponsableId\") REFERENCES \"Usuarios\" (\"Id\") ON DELETE RESTRICT;",
        "",
        "CREATE UNIQUE INDEX \"IX_Usuarios_Correo\" ON \"Usuarios\" (\"Correo\");",
        "CREATE UNIQUE INDEX \"IX_Equipos_CodigoPatrimonial\" ON \"Equipos\" (\"CodigoPatrimonial\");",
        "CREATE UNIQUE INDEX \"IX_Prestamos_EquipoActivo\" ON \"Prestamos\" (\"EquipoId\")",
        "  WHERE \"Estado\" = 'Activo';",
        "CREATE UNIQUE INDEX \"IX_Solicitudes_EquipoPendiente\" ON \"Solicitudes\" (\"EquipoId\")",
        "  WHERE \"Estado\" = 'Pendiente';",
        "ALTER TABLE \"Solicitudes\" ADD CONSTRAINT \"CK_Solicitudes_Aprobacion\"",
        "  CHECK ((\"Estado\" = 'Aprobada' AND \"PrestamoId\" IS NOT NULL)",
        "      OR (\"Estado\" <> 'Aprobada' AND \"PrestamoId\" IS NULL));",
    ], "Restricciones de integridad en PostgreSQL")

    doc.add_heading("2.4 Seguridad y control de acceso", level=2)
    par(doc,
        "La autenticación es real. El usuario se busca por correo, la contraseña se verifica con BCrypt y se emite un "
        "JWT firmado con HMAC-SHA256 que incluye identificador, nombre, correo, rol y área. El token se envía en el "
        "encabezado Authorization: Bearer y la API lo valida en cada petición. Las rutas del frontend se protegen con "
        "RutaPrivada y las acciones se ocultan o deshabilitan según el rol, pero la decisión definitiva siempre ocurre "
        "en el servidor. El portal público no consulta la base de datos: su vista previa es estática y los datos reales "
        "solo se obtienen con un token válido.")
    tabla(
        doc,
        ["Control", "Implementación", "Efecto"],
        [
            ("Hash de contraseñas", "BCrypt con sal por usuario.", "La base no almacena contraseñas en claro."),
            ("Contraseña temporal", "DebeCambiarPassword = true al crear la cuenta.", "El primer ingreso obliga al cambio."),
            ("Token JWT", "Claims sub, email, name, role y area; expiración de 480 minutos.", "Sesión sin estado y autorización por rol."),
            ("Autorización", "[Authorize] y [Authorize(Roles = \"Administrador,Responsable\")].", "La API responde 401 o 403 aunque se invoque directamente."),
            ("Alcance por rol", "Las consultas de préstamos y solicitudes filtran por UsuarioId cuando el rol es Colaborador.", "El colaborador no ve registros de otras cuentas; el gestor sí."),
            ("Auditoría", "Tabla Movimientos con actor, fecha, entidad, acción y detalle; endpoint solo para gestores.", "Las operaciones relevantes quedan trazadas."),
            ("Integridad", "Índices únicos parciales para préstamo activo y solicitud pendiente; CHECK de estados y fechas.", "La base rechaza duplicados y estados inválidos."),
            ("CORS", "Orígenes permitidos: localhost:5173 y 127.0.0.1:5173.", "Solo el frontend autorizado consume la API."),
            ("Errores", "Middleware uniforme con mensaje y código; sin trazas internas al cliente.", "No se filtran detalles de infraestructura."),
            ("Cierre de sesión", "Eliminación del token y redirección al login; evento sesion-expirada ante 401.", "La sesión se corta de forma consistente."),
        ],
        [3.4, 8.4, 4.8],
        "Controles de seguridad implementados.",
    )
    par(doc,
        "La contraseña temporal se entrega al administrador que crea la cuenta y se usa una sola vez para ingresar. "
        "El cambio exige mínimo ocho caracteres, mayúscula, minúscula, número y símbolo, y no permite repetir la "
        "contraseña actual. El sistema no almacena la clave temporal después del cambio; solo conserva su hash BCrypt "
        "actualizado.")

    doc.add_heading("2.5 Catálogo de la API REST", level=2)
    par(doc,
        "La API expone 26 operaciones agrupadas en siete controladores. Todas las rutas, excepto el inicio de sesión, "
        "requieren token. Swagger documenta los DTO, los códigos de respuesta y los permisos.")
    tabla(
        doc,
        ["Método", "Ruta", "Rol requerido", "Descripción"],
        [
            ("POST", "/api/auth/login", "Público", "Valida credenciales y devuelve token y usuario."),
            ("POST", "/api/auth/cambiar-clave", "Autenticado", "Cambia la contraseña actual o la temporal."),
            ("GET", "/api/usuarios", "Autenticado", "Lista usuarios con búsqueda, área, rol y estado."),
            ("POST", "/api/usuarios", "Administrador", "Registra un usuario con contraseña temporal."),
            ("PUT", "/api/usuarios/{id}", "Administrador", "Actualiza datos del usuario."),
            ("PATCH", "/api/usuarios/{id}/activo", "Administrador", "Habilita o deshabilita la cuenta (RN-09)."),
            ("GET", "/api/equipos", "Autenticado", "Consulta inventario con búsqueda, categoría y estado."),
            ("GET", "/api/equipos/todos", "Autenticado", "Devuelve todos los equipos para selectores."),
            ("GET", "/api/equipos/{id}", "Autenticado", "Consulta el detalle de un equipo."),
            ("POST", "/api/equipos", "Administrador, Responsable", "Registra un equipo."),
            ("PUT", "/api/equipos/{id}", "Administrador, Responsable", "Actualiza un equipo."),
            ("PATCH", "/api/equipos/{id}/estado", "Administrador, Responsable", "Cambia el estado operativo."),
            ("DELETE", "/api/equipos/{id}", "Administrador", "Elimina un equipo sin historial (RN-06)."),
            ("GET", "/api/prestamos", "Autenticado", "Historial paginado con filtros y búsqueda."),
            ("GET", "/api/prestamos/{id}", "Autenticado", "Consulta el detalle de un préstamo."),
            ("POST", "/api/prestamos", "Administrador, Responsable", "Registra un préstamo y actualiza el equipo."),
            ("PATCH", "/api/prestamos/{id}/devolver", "Administrador, Responsable", "Registra la devolución (RN-10)."),
            ("GET", "/api/solicitudes", "Autenticado (alcance por rol)", "Lista solicitudes; el Colaborador solo ve las propias."),
            ("GET", "/api/solicitudes/{id}", "Autenticado (propia o gestor)", "Consulta el detalle de una solicitud."),
            ("POST", "/api/solicitudes", "Autenticado", "Registra una solicitud para el usuario de la sesión."),
            ("PATCH", "/api/solicitudes/{id}/aprobar", "Administrador, Responsable", "Aprueba y genera el préstamo en una transacción."),
            ("PATCH", "/api/solicitudes/{id}/rechazar", "Administrador, Responsable", "Rechaza con observación obligatoria."),
            ("GET", "/api/movimientos", "Administrador, Responsable", "Consulta la auditoría de operaciones."),
            ("GET", "/api/reportes/resumen", "Autenticado (alcance por rol)", "Devuelve los indicadores y agregados del dashboard."),
            ("GET", "/api/reportes/prestamos.csv", "Administrador, Responsable", "Exporta el historial filtrado en CSV."),
            ("GET", "/api/reportes/equipos.csv", "Administrador, Responsable", "Exporta el inventario filtrado en CSV."),
        ],
        [1.8, 6.2, 4.0, 4.6],
        "Catálogo de endpoints de la API.",
        fuente=7.5,
    )

    doc.add_heading("2.6 Estándares de codificación", level=2)
    par(doc,
        "Los estándares buscan que el código sea legible, consistente y fácil de mantener. Se aplicaron en todo el "
        "proyecto y se verificaron durante la revisión final.")
    for texto in [
        "Backend: PascalCase para clases, métodos y propiedades; camelCase para parámetros y variables; interfaces con prefijo I; una clase por archivo.",
        "Separación estricta: entidades en Domain, DTO en Application, repositorios en Infrastructure y controladores en API; nunca se expone una entidad directamente.",
        "Reglas de negocio en servicios, no en controladores; validación de datos con DataAnnotations y validaciones de dominio con excepciones propias.",
        "Errores uniformes: 400 para datos inválidos, 401 sin token, 403 sin permiso, 404 no encontrado, 409 regla de negocio y 500 error controlado.",
        "Frontend: componentes en PascalCase, hooks con prefijo use, servicios en camelCase, estilos por bloque y nombres de clases en español coherentes.",
        "Textos visibles en español, mensajes que explican la causa y la solución, y formatos de fecha y números adaptados a Perú.",
        "Autorización y alcance: los controladores leen rol e identificador del token; las consultas de Colaborador filtran por UsuarioId.",
        "Auditoría: las operaciones relevantes registran un Movimiento con actor, entidad, acción, fecha y detalle, sin exponer SQL al cliente.",
        "Comentarios solo donde aportan intención (reglas, transacciones y decisiones), no para repetir el código.",
        "Documentación XML en controladores y servicios; Swagger como contrato visible; README con instalación, cuentas y scripts.",
    ]:
        vineta(doc, texto)


# --------------------------------------------------------------------------
# 3. Módulos de entrada
# --------------------------------------------------------------------------
def seccion_3(doc):
    doc.add_heading("3. MÓDULOS DE ENTRADA", level=1)
    par(doc,
        "Los módulos de entrada permiten registrar y actualizar la información del sistema. Todos comparten los mismos "
        "componentes de campo, ayuda, error y confirmación, y aplican validaciones en el navegador y en el servidor. "
        "La interfaz evita enviar datos inválidos; la API los rechaza aunque la petición no provenga de la interfaz.")

    doc.add_heading("3.1 Portal público y acceso", level=2)
    par(doc,
        "El sistema cuenta con un portal público de inicio en / que se puede abrir sin sesión. Presenta la propuesta de "
        "valor, las seis funciones principales, el flujo de trabajo en tres pasos, las medidas de seguridad y un acceso "
        "corporativo. Desde el portal se llega a /login; si el usuario ya tiene una sesión activa, la cabecera ofrece "
        "«Ir al panel». El portal comparte la identidad visual, la tipografía y el tema claro/oscuro de la aplicación. "
        "La Figura 31 del Anexo E muestra la portada pública y la Figura 32 su adaptación a móvil.")
    par(doc,
        "La pantalla de acceso divide la composición en dos zonas: a la izquierda, la identidad de TechAsset y una "
        "fotografía de un espacio de trabajo; a la derecha, el formulario. El correo corporativo y la contraseña son "
        "obligatorios; el botón muestra el estado «Verificando credenciales...» mientras espera la respuesta. Si las "
        "credenciales fallan, se muestra un mensaje genérico que no revela si el correo existe. El enlace «Volver al "
        "portal» permite regresar al inicio sin perder el contexto y, si el usuario llegó desde una ruta privada, "
        "después del acceso regresa a esa ruta.")
    figura(doc, CAPTURAS / "01-login.png", "Pantalla de acceso con identidad TechAsset, enlace al portal y ayuda visible.", ancho=16.2)
    par(doc, "Decisiones de diseño del acceso", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    for texto in [
        "Validación inmediata del formato del correo y del campo vacío, con foco automático en el primer error.",
        "Aviso de Bloq Mayús activado, porque la contraseña distingue mayúsculas de minúsculas.",
        "Control para mostrar u ocultar la contraseña y enlace para limpiar los campos.",
        "Enlace de soporte y correo de contacto visibles, sin exponer información de cuentas.",
        "Experiencia consistente en escritorio y móvil, con objetivos táctiles amplios y contraste suficiente.",
    ]:
        vineta(doc, texto)
    figura(doc, CAPTURAS / "02-login-error.png", "Error de autenticación anunciado con role=alert.", ancho=16.2)

    doc.add_heading("3.2 Gestión de usuarios", level=2)
    par(doc,
        "El módulo de usuarios permite consultar el directorio y, solo al Administrador, registrar, editar, habilitar o "
        "deshabilitar cuentas. El formulario solicita nombres, apellidos, correo corporativo, área, rol y contraseña "
        "temporal. El correo debe pertenecer a @innovatech.pe y ser único; la contraseña temporal debe cumplir la "
        "política de seguridad y se marca la cuenta para cambio obligatorio.")
    figura(doc, CAPTURAS / "06-usuarios.png", "Directorio de usuarios con rol, área, estado y acciones.", ancho=16.2)
    figura(doc, CAPTURAS / "07-usuarios-validacion.png", "Validación del formulario de usuario antes de enviar.", ancho=16.2)
    tabla(
        doc,
        ["Campo", "Validación en frontend", "Validación en backend", "Mensaje / código"],
        [
            ("Nombres", "Obligatorio, mínimo 3 y máximo 100 caracteres.", "Required + StringLength(3, 100).", "«Escriba los nombres (mínimo 3 caracteres)» / 400"),
            ("Apellidos", "Obligatorio, mínimo 3 y máximo 100 caracteres.", "Required + StringLength(3, 100).", "«Escriba los apellidos (mínimo 3 caracteres)» / 400"),
            ("Correo", "Formato nombre.apellido@innovatech.pe; único.", "EmailAddress + RegularExpression + ExisteCorreoAsync.", "«Use el formato nombre.apellido@innovatech.pe» / 409"),
            ("Área", "Selección obligatoria del catálogo.", "Pertenencia a CatalogoTechAsset.Areas.", "«Seleccione un área» / 400"),
            ("Rol", "Selección obligatoria del catálogo.", "Pertenencia a CatalogoTechAsset.Roles.", "«Seleccione un rol» / 400"),
            ("Contraseña temporal", "8+ caracteres, mayúscula, minúscula, número y símbolo.", "RegularExpression y hash BCrypt.", "«Mínimo 8 caracteres con mayúscula, minúscula, número y símbolo» / 400"),
        ],
        [2.8, 5.2, 5.2, 5.0],
        "Validaciones del formulario de usuarios.",
        fuente=7.5,
    )
    par(doc,
        "Al crear la cuenta, el sistema devuelve 201 y muestra un toast con el nombre del usuario; el administrador "
        "entrega la contraseña temporal por un canal seguro. La edición no permite cambiar la contraseña ni el estado "
        "desde el mismo formulario: el estado se controla con una acción separada para que el cambio sea explícito. "
        "El Administrador no puede deshabilitar su propia cuenta y el sistema impide deshabilitar usuarios con "
        "préstamos activos.")

    doc.add_heading("3.3 Gestión de equipos", level=2)
    par(doc,
        "El inventario registra código patrimonial, nombre, categoría, marca y estado. El código es único y se "
        "normaliza a mayúsculas; la categoría y el estado provienen de catálogos cerrados para evitar valores "
        "inconsistentes. El estado Prestado no se elige manualmente: se asigna cuando se registra un préstamo y se "
        "libera cuando se registra la devolución.")
    figura(doc, CAPTURAS / "08-equipos.png", "Inventario con búsqueda, filtros, estado y acciones por equipo.", ancho=16.2)
    figura(doc, CAPTURAS / "09-equipos-validacion.png", "Validación del formulario de equipo.", ancho=16.2)
    par(doc,
        "El cambio de estado se realiza en un diálogo pequeño que muestra el código y el nombre del equipo. Si el "
        "equipo tiene un préstamo activo, la operación se bloquea con un mensaje que indica registrar primero la "
        "devolución. La eliminación solo está disponible para el Administrador y se rechaza si existe historial de "
        "préstamos (RN-06); en ese caso se sugiere marcarlo como Baja en lugar de borrarlo.")
    tabla(
        doc,
        ["Estado", "Significado", "Se asigna por", "Permite préstamo"],
        [
            ("Disponible", "Equipo listo para asignación.", "Registro, devolución o cambio administrativo.", "Sí"),
            ("Prestado", "Equipo asignado a un colaborador.", "Registro de un préstamo (automático).", "No (ya está prestado)"),
            ("Mantenimiento", "Equipo fuera de servicio temporal.", "Cambio administrativo.", "No (RN-02)"),
            ("Baja", "Equipo retirado del inventario.", "Cambio administrativo.", "No (RN-03)"),
        ],
        [2.6, 6.0, 6.2, 3.4],
        "Estados del equipo y efecto en el préstamo.",
    )

    doc.add_heading("3.4 Registro de préstamos", level=2)
    par(doc,
        "El formulario de préstamo es el módulo de entrada principal. Solicita colaborador activo, equipo disponible, "
        "fecha de préstamo, fecha de devolución y motivo. Solo muestra colaboradores con rol Colaborador y equipos en "
        "estado Disponible; el responsable que registra se obtiene del token, no se elige en el formulario. Al guardar, "
        "el equipo pasa a Prestado y el préstamo queda en estado Activo.")
    figura(doc, CAPTURAS / "14-nuevo-prestamo.png", "Formulario de nuevo préstamo con equipos disponibles y reglas visibles.", ancho=16.2)
    figura(doc, CAPTURAS / "15-nuevo-prestamo-validacion.png", "Errores de validación del préstamo antes del envío.", ancho=16.2)
    figura(doc, CAPTURAS / "16-nuevo-prestamo-ok.png", "Confirmación del préstamo registrado con su código y fechas.", ancho=16.2)
    par(doc,
        "La operación se ejecuta en una transacción: se inserta el préstamo y se actualiza el equipo. Si una de las dos "
        "escrituras falla, la transacción se revierte y no queda un préstamo sin efecto en el inventario. El código del "
        "préstamo se genera como PR- seguido de seis caracteres del identificador, para que sea legible y estable.")
    tabla(
        doc,
        ["Campo / regla", "Frontend", "Backend", "Resultado"],
        [
            ("Colaborador", "Selección obligatoria de usuario activo con rol Colaborador.", "Verifica existencia y Activo; rechaza inactivos.", "400 / 409"),
            ("Equipo", "Solo equipos en estado Disponible.", "Verifica estado y que no exista préstamo activo (RN-01).", "409"),
            ("Fecha de préstamo", "Obligatoria; puede ser histórica para registrar movimientos.", "DateOnly válida; no se restringe al futuro.", "400"),
            ("Fecha de devolución", "Debe ser posterior a la fecha de préstamo (RN-04).", "Comparación estricta DateOnly.", "409"),
            ("Motivo", "Obligatorio, entre 5 y 300 caracteres, con contador.", "StringLength y validación en el servicio.", "400"),
            ("Responsable", "No editable: se toma de la sesión.", "ResponsableId desde el claim; rol autorizado (RN-05).", "403"),
        ],
        [3.0, 5.6, 5.5, 3.9],
        "Validaciones del registro de préstamos.",
        fuente=7.5,
    )

    doc.add_heading("3.5 Registro de devoluciones", level=2)
    par(doc,
        "La devolución se registra desde el historial o desde el detalle del préstamo. El diálogo recuerda que el "
        "equipo volverá a Disponible y exige una observación de al menos cinco caracteres (RN-10). Al confirmar, se "
        "actualiza el préstamo a Devuelto, se guarda la fecha real y la observación, y el equipo recupera el estado "
        "Disponible en la misma transacción. Un préstamo ya devuelto no puede devolverse otra vez.")
    figura(doc, CAPTURAS / "13-prestamo-devolucion.png", "Registro de devolución con observación obligatoria (RN-10).", ancho=15.2)

    doc.add_heading("3.6 Validación en dos capas", level=2)
    par(doc,
        "La validación en dos capas es una decisión de calidad, no una duplicación innecesaria. El frontend mejora la "
        "experiencia porque evita viajes innecesarios y explica el error junto al campo; el backend protege la "
        "integridad porque cualquier cliente puede invocar la API directamente. Las dos capas comparten el mismo "
        "lenguaje y los mismos códigos, pero no el mismo código: el frontend usa funciones puras y el backend usa "
        "DataAnnotations y reglas de dominio.")
    tabla(
        doc,
        ["Regla", "Frontend", "Backend", "Código HTTP"],
        [
            ("Campos obligatorios", "Validación antes de enviar y foco en el primer error.", "DataAnnotations + ModelState.", "400"),
            ("Formato de correo y dominio", "Expresión regular y mensaje específico.", "EmailAddress + RegularExpression.", "400"),
            ("Fechas del préstamo", "Comparación de fechas y mínimo del calendario.", "Comparación DateOnly en el servicio.", "409"),
            ("Disponibilidad del equipo", "Solo lista equipos Disponibles.", "Verifica estado y préstamo activo (RN-01).", "409"),
            ("Permisos por rol", "Oculta o deshabilita acciones.", "[Authorize(Roles)] en el controlador.", "401 / 403"),
            ("Unicidad", "Aviso previo en el formulario.", "Consulta en repositorio e índice único.", "409"),
        ],
        [4.2, 6.0, 6.0, 2.2],
        "Reglas verificadas en frontend y backend.",
    )
    codigo(doc, [
        "// Application/DTOs/TechAssetDtos.cs (extracto)",
        "public class CrearPrestamoDto",
        "{",
        "    [Required(ErrorMessage = \"Seleccione al colaborador.\")]",
        "    public Guid UsuarioId { get; set; }",
        "",
        "    [Required(ErrorMessage = \"Indique la fecha de devolución.\")]",
        "    public DateOnly FechaDevolucion { get; set; }",
        "",
        "    [StringLength(300, MinimumLength = 5,",
        "        ErrorMessage = \"La observación debe tener entre 5 y 300 caracteres.\")]",
        "    public string Observacion { get; set; } = string.Empty;",
        "}",
    ], "Validación declarativa del DTO de entrada")
    codigo(doc, [
        "// utils/validaciones.js (extracto)",
        "if (!valores.fechaDevolucion) {",
        "  errores.fechaDevolucion = \"Indique la fecha de devolución.\";",
        "} else if (valores.fechaPrestamo && valores.fechaDevolucion <= valores.fechaPrestamo) {",
        "  errores.fechaDevolucion = \"La devolución debe ser posterior al préstamo (RN-04).\";",
        "}",
    ], "Validación equivalente en el cliente")

    doc.add_heading("3.7 Solicitud y aprobación de equipos", level=2)
    par(doc,
        "El flujo de solicitud permite que el Colaborador pida un equipo sin recibir acceso directo al registro de "
        "préstamos. El formulario solicita equipo disponible, fecha de préstamo, fecha de devolución y motivo. La "
        "solicitud queda en estado Pendiente y no reserva el equipo; el Responsable de Tecnología la revisa y decide. "
        "Si aprueba, el sistema crea el préstamo, marca el equipo como Prestado y vincula la solicitud al préstamo "
        "dentro de una transacción. Si rechaza, exige una observación y el equipo permanece disponible.")
    par(doc,
        "La aprobación vuelve a comprobar la disponibilidad porque entre la solicitud y la revisión el equipo pudo "
        "haber sido prestado. El índice único parcial de préstamo activo y el índice de solicitud pendiente por equipo "
        "refuerzan la regla incluso ante dos peticiones concurrentes. La Figura 33 del Anexo F muestra la bandeja del "
        "Responsable, la Figura 34 el diálogo de aprobación, la Figura 35 la solicitud aprobada con su préstamo y la "
        "Figura 41 la confirmación que recibe el Colaborador.")
    tabla(
        doc,
        ["Validación", "Frontend", "Backend", "Resultado"],
        [
            ("Equipo", "Solo equipos en estado Disponible.", "Verifica existencia, estado y ausencia de préstamo activo.", "409"),
            ("Fechas", "Préstamo no anterior a hoy; devolución posterior.", "Comparación DateOnly en el servicio.", "409"),
            ("Motivo", "Entre 5 y 300 caracteres con contador.", "StringLength + validación de dominio.", "400"),
            ("Solicitud pendiente", "Aviso si el equipo ya tiene una.", "Consulta ExistePendientePorEquipoAsync + índice único parcial.", "409"),
            ("Aprobación", "Solo visible para Administrador/Responsable.", "Authorize(Roles) y revalidación de disponibilidad.", "403 / 409"),
            ("Rechazo", "Observación obligatoria.", "Longitud mínima y estado Pendiente.", "409"),
            ("Propiedad", "El Colaborador solo ve sus solicitudes.", "Filtro UsuarioId y verificación en el detalle.", "403"),
        ],
        [3.4, 5.0, 6.2, 2.2],
        "Validaciones del flujo de solicitudes.",
        fuente=7.4,
    )
    codigo(doc, [
        "await unitOfWork.EjecutarAsync(async () =>",
        "{",
        "    await prestamoRepository.AgregarAsync(prestamo);",
        "    await equipoRepository.ActualizarAsync(equipo);",
        "    await solicitudRepository.ActualizarAsync(solicitud);",
        "    await movimientoService.RegistrarAsync(",
        "        \"Solicitud\", solicitud.Id, \"Aprobar\", detalle, revisor.Id, nombreRevisor);",
        "    return true;",
        "});",
    ], "Transacción de aprobación: préstamo, equipo, solicitud y auditoría")


# --------------------------------------------------------------------------
# 4. Reutilización y refinamiento
# --------------------------------------------------------------------------
def seccion_4(doc):
    doc.add_heading("4. REUTILIZACIÓN Y REFINAMIENTO", level=1)
    par(doc,
        "La reutilización se planificó desde el diseño: en lugar de construir cada pantalla con su propia tabla, su "
        "propio modal y sus propios campos, se extrajeron componentes con una interfaz clara. El refinamiento se "
        "aplicó después de tener los módulos funcionando, cuando las duplicaciones y los olores de código se hicieron "
        "visibles. El resultado es un frontend más pequeño, coherente y fácil de extender.")

    doc.add_heading("4.1 Organización del frontend", level=2)
    par(doc,
        "El frontend se organiza por responsabilidad. Las páginas componen la vista y manejan el estado local; los "
        "hooks encapsulan la carga de datos y el ciclo cargando/error/recargar; los servicios traducen las operaciones "
        "a rutas HTTP; el cliente API centraliza fetch, el token, los errores y la descarga de archivos; las utilidades "
        "contienen catálogos, formato y validaciones puras.")
    codigo(doc, [
        "Página (Usuarios.jsx)",
        "   ↓ usa",
        "Hook (useUsuarios.js)  →  estado: datos, cargando, error, recargar",
        "   ↓ llama",
        "Servicio (usuarioService.js)  →  rutas y parámetros",
        "   ↓ usa",
        "Cliente API (api.js)  →  fetch + JWT + manejo de ErrorApi",
        "   ↓ HTTP/JSON",
        "API ASP.NET Core  →  Servicio  →  Repositorio  →  PostgreSQL",
    ])
    par(doc,
        "Esta separación permite que una página no sepa si los datos vienen de la API o de una caché futura, y que un "
        "cambio en la forma de autenticar se realice en un solo archivo. También facilita reemplazar una tabla por "
        "tarjetas en móvil sin tocar la lógica de negocio.")

    doc.add_heading("4.2 Componentes reutilizables", level=2)
    par(doc,
        "Se construyeron 22 componentes compartidos. Los más importantes son los campos de formulario, la tabla "
        "genérica, el modal accesible, las etiquetas de estado y las tarjetas de indicador. Cada componente recibe "
        "datos y eventos por props, no conoce la API y puede usarse en cualquier módulo.")
    figura(doc, FIGURAS / "componentes.png", "Mapa de componentes compartidos por los módulos.", ancho=16.0)
    tabla(
        doc,
        ["Componente", "Propósito", "Reutilización"],
        [
            ("Boton", "Botón con variantes, icono, estado de carga y tamaños.", "Todos los módulos."),
            ("CampoTexto", "Entrada con etiqueta, ayuda, error, sufijo y autofoco.", "Login, usuarios, equipos, préstamos y filtros."),
            ("CampoSelect", "Selector nativo con etiqueta, ayuda y error.", "Áreas, roles, categorías, estados y equipos."),
            ("CampoArea", "Área de texto con contador y validación.", "Motivo del préstamo y observación de devolución."),
            ("Modal", "Diálogo accesible con foco atrapado, Escape y retorno de foco.", "Altas, ediciones, estados, devoluciones y detalles."),
            ("ModalAyuda", "Ayuda contextual con atajos, reglas y accesibilidad.", "Barra superior y menú lateral."),
            ("TablaDatos", "Tabla configurable por columnas y render; tarjetas en móvil.", "Usuarios, equipos, préstamos y reportes."),
            ("Paginacion", "Rango, total, página anterior y siguiente.", "Historial de préstamos."),
            ("EstadoVacio", "Mensaje y acción cuando no hay resultados.", "Todas las consultas."),
            ("Cargando", "Esqueletos de filas durante la carga.", "Todas las consultas."),
            ("TarjetaIndicador", "Indicador con valor, detalle, icono y tono.", "Dashboard y reportes."),
            ("BarrasDatos", "Barras proporcionales con etiqueta y valor.", "Dashboard y reportes."),
            ("EncabezadoPagina", "Título, descripción y acciones.", "Todas las páginas internas."),
            ("EtiquetaEquipo", "Estado del equipo con color y punto.", "Inventario, préstamo y reportes."),
            ("EtiquetaPrestamo", "Estado del préstamo con color y punto.", "Historial y dashboard."),
            ("EtiquetaRol", "Rol del usuario con color.", "Directorio y barra superior."),
            ("EtiquetaSolicitud", "Estado de la solicitud con color.", "Solicitudes y detalle."),
            ("Iconos", "Set SVG propio y consistente.", "Toda la interfaz."),
            ("Sidebar / Topbar", "Navegación, sesión, tema, ayuda y estado de la API.", "Layout interno."),
            ("RutaPrivada", "Protección de rutas y redirección al login.", "Todas las rutas privadas."),
            ("AppLayout", "Estructura común con menú, cabecera y contenido.", "Todas las páginas internas."),
            ("Confirmaciones", "Patrón de confirmación para acciones destructivas.", "Equipos, devoluciones y estados."),
        ],
        [3.4, 10.0, 4.0],
        "Componentes reutilizables del frontend.",
        fuente=7.4,
    )

    doc.add_heading("4.3 Hooks personalizados", level=2)
    par(doc,
        "Los hooks encapsulan el patrón de carga de datos: estado de datos, cargando, error, versión y función de "
        "recarga. Gracias a ellos, las páginas no repiten useEffect ni manejo de cancelación; solo declaran filtros y "
        "consumen el resultado. El patrón también evita actualizaciones sobre componentes desmontados.")
    tabla(
        doc,
        ["Hook", "Responsabilidad", "Usado por"],
        [
            ("useUsuarios", "Lista usuarios según texto, área, rol y estado; recarga.", "Usuarios, selects de colaboradores."),
            ("useEquipos", "Lista equipos según texto, categoría y estado.", "Equipos, reportes y selects."),
            ("usePrestamos", "Historial paginado y filtrado; conserva la página.", "Préstamos y dashboard."),
            ("useResumen", "Indicadores y agregados del dashboard.", "Dashboard y reportes."),
            ("useCatalogos", "Carga paralela de usuarios y equipos para formularios.", "Nuevo préstamo."),
            ("useSolicitudes", "Lista solicitudes paginadas con filtros y recarga.", "Solicitudes y dashboard."),
            ("useMovimientos", "Lista la auditoría con filtros y paginación.", "Movimientos."),
            ("useTema", "Tema claro/oscuro persistido en localStorage.", "Aplicación completa."),
            ("AuthContext", "Sesión, token, usuario, login, logout y cambio de clave.", "Rutas y layout."),
            ("ToastContext", "Notificaciones de éxito y error con cierre automático.", "Todas las acciones."),
        ],
        [3.4, 9.6, 5.6],
        "Hooks y contextos del frontend.",
        fuente=7.8,
    )

    doc.add_heading("4.4 Servicios y cliente API", level=2)
    par(doc,
        "El cliente api.js es el único lugar que conoce la URL base, el token y el formato de error. Expone operaciones "
        "obtener, crear, actualizar, reemplazar, eliminar y descargar; agrega el encabezado Authorization, interpreta "
        "el JSON, lanza ErrorApi con estado y errores por campo, y emite el evento sesion-expirada cuando la API "
        "responde 401. Los servicios de dominio solo construyen rutas y parámetros.")
    tabla(
        doc,
        ["Servicio", "Operaciones principales"],
        [
            ("api.js", "URL base, token, fetch, ErrorApi, descarga de blobs y evento de sesión expirada."),
            ("authService.js", "Inicio de sesión y cambio de contraseña."),
            ("usuarioService.js", "Listar, crear, actualizar y cambiar estado activo."),
            ("equipoService.js", "Listar, obtener todos, crear, actualizar, cambiar estado y eliminar."),
            ("prestamoService.js", "Listar, obtener, crear, devolver y resumen de indicadores."),
            ("solicitudService.js", "Listar, crear, aprobar y rechazar solicitudes."),
            ("movimientoService.js", "Consultar la auditoría de operaciones."),
            ("reporteService.js", "Resumen y descarga de préstamos e inventario en CSV."),
        ],
        [4.0, 12.0],
        "Servicios del frontend.",
    )

    doc.add_heading("4.5 Catálogo centralizado y DTO", level=2)
    par(doc,
        "Los valores de rol, área, categoría y estado se definen una sola vez en CatalogoTechAsset (backend) y en "
        "constantes.js (frontend). Esto evita cadenas duplicadas, errores de tipeo y comportamientos distintos entre "
        "módulos. Los DTO separan la entrada de la salida y permiten validar con DataAnnotations sin contaminar las "
        "entidades.")
    codigo(doc, [
        "public static class CatalogoTechAsset",
        "{",
        "    public const string RolAdministrador = \"Administrador\";",
        "    public const string RolResponsable   = \"Responsable\";",
        "    public const string RolColaborador   = \"Colaborador\";",
        "",
        "    public static readonly IReadOnlyList<string> Categorias = new[]",
        "    {",
        "        \"Laptop\", \"Computadora de escritorio\", \"Monitor\", \"Impresora\",",
        "        \"Tablet\", \"Proyector\", \"Equipo de red\"",
        "    };",
        "",
        "    public const string EquipoDisponible   = \"Disponible\";",
        "    public const string EquipoPrestado     = \"Prestado\";",
        "    public const string EquipoMantenimiento = \"Mantenimiento\";",
        "    public const string EquipoBaja         = \"Baja\";",
        "}",
    ], "Catálogo único de valores del dominio")

    doc.add_heading("4.6 Refinamientos aplicados", level=2)
    par(doc,
        "El refinamiento se aplicó con el sistema funcionando, comparando versiones y midiendo el costo de cada cambio. "
        "La tabla resume las mejoras más relevantes y su efecto en la mantenibilidad.")
    tabla(
        doc,
        ["Antes", "Después", "Beneficio"],
        [
            ("Cada página llamaba a fetch y repetía el manejo del token.", "Cliente api.js único con ErrorApi y evento de sesión.", "Un solo punto para autenticación, errores y descargas."),
            ("Tablas HTML duplicadas en usuarios, equipos y préstamos.", "TablaDatos configurable por columnas y render.", "Menos código, mismo comportamiento y vista móvil consistente."),
            ("Etiquetas de estado repetidas con colores inline.", "EtiquetaEquipo, EtiquetaPrestamo y EtiquetaRol.", "Colores y semántica unificados; cambios en un solo lugar."),
            ("Validaciones mezcladas con el JSX de cada página.", "Funciones puras en utils/validaciones.js.", "Pruebas más simples y reutilización entre formularios."),
            ("Listas de áreas, roles y categorías escritas en cada archivo.", "Catálogo centralizado en constantes.js y CatalogoTechAsset.", "Eliminación de valores inconsistentes y errores de tipeo."),
            ("Modales con lógica de foco y Escape repetida.", "Modal accesible con foco atrapado y retorno.", "Accesibilidad uniforme y menos duplicación."),
            ("Estados de carga y vacío resueltos de forma distinta.", "Cargando, EstadoVacio y esqueletos compartidos.", "Experiencia consistente en todas las consultas."),
            ("Controladores con reglas y mapeos manuales.", "Servicios, DTO y mapeos en Application.", "Controladores delgados y reglas testeables."),
            ("Dos escrituras separadas al crear un préstamo.", "UnitOfWork con transacción de base de datos.", "Consistencia entre préstamo y estado del equipo."),
            ("Consultas globales para todos los roles.", "Filtro por propietario y guardas de ruta.", "El Colaborador solo ve sus préstamos y solicitudes."),
            ("Aprobación con escrituras separadas.", "Transacción que crea el préstamo, actualiza el equipo, vincula la solicitud y audita.", "Todo o nada en la aprobación."),
            ("Operaciones sin trazabilidad.", "Tabla Movimientos y consulta de auditoría.", "Cada evento conserva actor, fecha y detalle."),
            ("Consultas sin paginación en el historial.", "Paginación en servidor con total y páginas.", "Respuestas acotadas y navegación clara."),
        ],
        [5.0, 7.0, 4.6],
        "Refinamientos aplicados y su beneficio.",
        fuente=7.5,
    )
    par(doc,
        "Un ejemplo concreto es la tabla. La primera versión tenía tres componentes casi iguales, con encabezados y "
        "celdas repetidas. Se reemplazaron por TablaDatos, que recibe un arreglo de columnas con clave, título, clase y "
        "función de render. Las páginas ahora declaran solo lo que cambia: cómo se muestra una celda. En móvil, el "
        "mismo componente convierte cada fila en una tarjeta usando el atributo data-etiqueta, sin duplicar la vista.")
    par(doc,
        "Otro ejemplo es la validación. Las funciones validarUsuario, validarEquipo, validarPrestamo y "
        "validarDevolucion devuelven un objeto de errores y no dependen de React. Eso permitió reutilizarlas en distintos "
        "formularios y mantener los mensajes alineados con el backend. La misma lógica de fechas y longitudes se "
        "replica en el servidor con DataAnnotations y reglas de dominio.")

    doc.add_heading("4.7 Métricas y beneficios", level=2)
    par(doc,
        "Las métricas se obtuvieron del repositorio y del reporte de compilación. No pretenden medir productividad, "
        "sino documentar el tamaño del entregable y el efecto de la reutilización.")
    tabla(
        doc,
        ["Métrica", "Valor"],
        [
            ("Archivos C# (sin migraciones, obj ni bin)", "48 archivos · 2 808 líneas"),
            ("Archivos del frontend (JSX, JS, CSS)", "62 archivos · 9 489 líneas"),
            ("Componentes compartidos", "22"),
            ("Hooks y contextos", "10"),
            ("Servicios del frontend", "8"),
            ("Endpoints documentados", "26"),
            ("Módulos empaquetados por Vite", "82"),
            ("Tamaño del bundle", "JS 400.94 kB (113.14 kB gzip) · CSS 58.25 kB (11.02 kB gzip)"),
            ("Compilación del backend", "0 errores · 0 advertencias"),
            ("Pruebas de API conformes", "50 de 50"),
        ],
        [8.0, 8.0],
        "Métricas del entregable.",
    )
    par(doc,
        "El beneficio principal no es la reducción de líneas, sino la previsibilidad del cambio. Agregar un filtro al "
        "historial implicó modificar el hook, el servicio y la barra de filtros; no fue necesario tocar la tabla, el "
        "modal ni las etiquetas. Corregir un color de estado se hizo en un componente y se reflejó en inventario, "
        "préstamos, dashboard y reportes. Esa es la evidencia práctica de la reutilización.")


# --------------------------------------------------------------------------
# 5. Módulos de salida
# --------------------------------------------------------------------------
def seccion_5(doc):
    doc.add_heading("5. MÓDULOS DE SALIDA", level=1)
    par(doc,
        "Los módulos de salida permiten recuperar la información registrada y presentarla de forma útil. TechAsset "
        "ofrece consultas con filtros, búsqueda, paginación, detalle, dashboard, reportes y exportación. Todas las "
        "consultas se resuelven en el servidor y respetan el rol de la sesión.")

    doc.add_heading("5.1 Consultas y filtros", level=2)
    par(doc,
        "El historial de préstamos es la consulta más completa: permite buscar por equipo, código patrimonial o "
        "colaborador; filtrar por estado, área, equipo y rango de fechas; ordenar los activos primero y paginar. Los "
        "criterios se guardan en la URL, de modo que una búsqueda se puede compartir o recuperar al volver a la "
        "página. La consulta se traduce a LINQ y se ejecuta en PostgreSQL con ILIKE para búsquedas sin distinción de "
        "mayúsculas.")
    figura(doc, CAPTURAS / "10-prestamos.png", "Historial de préstamos con filtros y paginación.", ancho=16.2)
    figura(doc, CAPTURAS / "11-prestamos-filtrados.png", "Filtros combinados por estado y área, conservados en la URL.", ancho=16.2)
    par(doc,
        "El inventario permite buscar por código, nombre o marca y filtrar por categoría y estado. El directorio de "
        "usuarios permite buscar por nombre, apellido o correo y filtrar por área, rol y estado activo. En los tres "
        "casos, el resultado muestra el número de coincidencias y un estado vacío con una acción para limpiar los "
        "filtros o registrar un nuevo elemento.")

    doc.add_heading("5.2 Búsqueda y paginación", level=2)
    par(doc,
        "La paginación se resuelve en el servidor: la API recibe pagina y tamanoPagina, calcula el total y devuelve "
        "solo la página solicitada. El frontend muestra el rango visible, el total y los botones anterior/siguiente. "
        "Esto evita cargar todo el historial y mantiene la respuesta acotada aunque la tabla crezca.")
    tabla(
        doc,
        ["Elemento", "Implementación", "Efecto"],
        [
            ("Búsqueda", "Texto libre con ILIKE sobre nombre, código y colaborador.", "Coincidencias parciales sin distinguir mayúsculas."),
            ("Filtros", "Estado, área, equipo, categoría, rol y rango de fechas.", "Combinaciones guardadas en la URL."),
            ("Orden", "Activos primero, luego fecha de préstamo y registro descendente.", "Lo pendiente aparece primero."),
            ("Paginación", "Skip/Take, total y totalPaginas en la respuesta.", "Respuestas acotadas y navegación clara."),
            ("Estado vacío", "Mensaje contextual y acción para limpiar o crear.", "El usuario nunca queda sin salida."),
            ("Conteo", "Total de coincidencias y rango visible.", "Transparencia sobre lo que se está viendo."),
        ],
        [3.2, 9.4, 4.2],
        "Componentes de búsqueda y paginación.",
    )

    doc.add_heading("5.3 Dashboard e indicadores", level=2)
    par(doc,
        "El dashboard presenta los seis indicadores solicitados y dos gráficos de distribución. Los valores se calculan "
        "en el servidor con una sola consulta agregada, para que todos los usuarios vean las mismas cifras y no se "
        "dupliquen reglas en el cliente. La tarjeta de «Área con mayor uso» se destaca porque responde a una pregunta "
        "de gestión: qué área concentra la demanda de equipos.")
    figura(doc, CAPTURAS / "03-dashboard.png", "Dashboard con los seis indicadores y la distribución del inventario.", ancho=16.2)
    tabla(
        doc,
        ["Indicador", "Definición", "Fuente", "Valor de demostración"],
        [
            ("Total de equipos", "Equipos registrados en el sistema.", "COUNT(Equipos)", "18"),
            ("Equipos disponibles", "Equipos listos para préstamo.", "COUNT(Estado = Disponible)", "8"),
            ("Equipos prestados", "Equipos asignados actualmente.", "COUNT(Estado = Prestado)", "8"),
            ("Equipos en mantenimiento", "Equipos fuera de servicio.", "COUNT(Estado = Mantenimiento)", "1"),
            ("Total de préstamos", "Préstamos registrados (activos y devueltos).", "COUNT(Prestamos)", "17"),
            ("Área con mayor uso", "Área que registra más préstamos.", "GROUP BY Area ORDER BY COUNT DESC", "Desarrollo (4)"),
        ],
        [3.6, 6.4, 5.0, 2.6],
        "Indicadores del dashboard y su cálculo.",
        fuente=7.5,
    )
    par(doc,
        "El panel también muestra una alerta con los préstamos activos pendientes de devolución y un acceso directo al "
        "historial filtrado. Esa alerta convierte un dato pasivo en una tarea concreta: revisar, devolver y mantener el "
        "inventario actualizado.")

    doc.add_heading("5.4 Reportes y gráficos", level=2)
    par(doc,
        "La pantalla de reportes reúne los indicadores, la distribución de equipos por estado, los préstamos por área, "
        "el ranking de equipos más utilizados y dos listados: equipos disponibles y equipos prestados. Los gráficos son "
        "barras proporcionales construidas con HTML y CSS, accesibles por texto y sin dependencias externas.")
    figura(doc, CAPTURAS / "17-reportes.png", "Reportes con indicadores, distribuciones y ranking de equipos.", ancho=16.2)
    par(doc,
        "El ranking de equipos más utilizados se calcula agrupando los préstamos por equipo y ordenando de forma "
        "descendente. El área con mayor uso se obtiene agrupando por el área del solicitante. Ambos cálculos se hacen "
        "en el servidor y se devuelven como listas de etiqueta y total, lo que mantiene el frontend simple y permite "
        "reutilizar los mismos datos en el dashboard y en los reportes.")

    doc.add_heading("5.5 Exportación de datos", level=2)
    par(doc,
        "Los reportes se pueden descargar en CSV desde la barra de acciones. La API genera el archivo con separador "
        "punto y coma, codificación UTF-8 con BOM y encabezados legibles, para que Excel en español lo abra "
        "correctamente. La exportación respeta los filtros aplicados y no requiere una consulta distinta a la del "
        "historial.")
    tabla(
        doc,
        ["Reporte", "Endpoint", "Contenido", "Formato"],
        [
            ("Préstamos", "/api/reportes/prestamos.csv", "Código, equipo, código patrimonial, solicitante, área, fechas, estado y observación.", "CSV UTF-8 con BOM"),
            ("Inventario", "/api/reportes/equipos.csv", "Código patrimonial, equipo, categoría, marca, estado y cantidad de préstamos.", "CSV UTF-8 con BOM"),
        ],
        [2.6, 6.4, 6.4, 3.4],
        "Reportes exportables.",
    )
    codigo(doc, [
        "Codigo;Equipo;CodigoPatrimonial;Solicitante;Area;FechaPrestamo;FechaDevolucion;Estado",
        "PR-6B1A2C;Laptop Dell Latitude 5440;TA-0001;Ana Torres Vega;Desarrollo;2026-11-17;2026-11-22;Activo",
        "PR-2F9D41;Laptop HP EliteBook 840;TA-0002;Carla Mendoza Ríos;Marketing;2026-11-12;2026-11-17;Devuelto",
    ], "Extracto del CSV de préstamos")

    doc.add_heading("5.6 Detalle y trazabilidad", level=2)
    par(doc,
        "Cada préstamo tiene una vista de detalle con el colaborador, su área, el equipo, el código patrimonial, las "
        "fechas de préstamo, devolución prevista y devolución real, el estado, el responsable que lo registró, la fecha "
        "de registro y las observaciones. Esta vista responde a RF-17 y permite auditar quién hizo qué y cuándo.")
    figura(doc, CAPTURAS / "12-prestamo-detalle.png", "Detalle del préstamo con trazabilidad completa.", ancho=15.6)
    par(doc,
        "El detalle también explica la regla vigente: mientras el préstamo esté activo, el equipo permanece en estado "
        "Prestado y no puede asignarse a otra persona (RN-01). Si el préstamo ya fue devuelto, se muestra la fecha real "
        "y la observación de devolución, lo que completa el ciclo de vida del movimiento.")

    doc.add_heading("5.7 Historial por rol y auditoría", level=2)
    par(doc,
        "Las consultas respetan el rol de la sesión. El Administrador y el Responsable ven el historial global; el "
        "Colaborador ve únicamente los préstamos y solicitudes asociados a su cuenta. El filtro se aplica en la "
        "consulta SQL, no solo en la interfaz: una petición directa a /api/prestamos con un token de Colaborador "
        "también devuelve solo sus registros. Los reportes y la exportación CSV quedan restringidos a los gestores.")
    tabla(
        doc,
        ["Consulta", "Administrador", "Responsable", "Colaborador"],
        [
            ("/api/prestamos", "Global", "Global", "Solo propios"),
            ("/api/solicitudes", "Global", "Global", "Solo propias"),
            ("/api/reportes/resumen", "Global", "Global", "Solo sus préstamos"),
            ("/api/reportes/*.csv", "Sí", "Sí", "403"),
            ("/api/usuarios", "Sí", "Sí", "403"),
            ("/api/movimientos", "Sí", "Sí", "403"),
        ],
        [6.4, 3.4, 3.4, 3.4],
        "Alcance de las consultas por rol.",
        fuente=7.8,
    )
    par(doc,
        "La auditoría se consulta en la página Movimientos, con búsqueda por texto, entidad y acción. Cada fila "
        "muestra la fecha, la entidad, la acción, el detalle y el responsable. Los eventos se generan al registrar o "
        "devolver un préstamo, al crear una solicitud y al aprobarla o rechazarla. No existe un endpoint para editar "
        "o borrar movimientos: la auditoría es de solo lectura desde la aplicación.")
    par(doc,
        "Las Figuras 36, 38 y 42 del Anexo F muestran la auditoría, la bandeja de solicitudes del Colaborador y su "
        "historial propio. La Figura 43 evidencia la adaptación del inventario al rol de consulta.")


# --------------------------------------------------------------------------
# 6. Integración
# --------------------------------------------------------------------------
def seccion_6(doc):
    doc.add_heading("6. INTEGRACIÓN DE MÓDULOS", level=1)
    par(doc,
        "La integración se verificó de extremo a extremo: una acción en React viaja a la API, se valida en Application, "
        "se persiste en PostgreSQL y regresa a la interfaz como confirmación. No hay datos simulados en el frontend ni "
        "reglas duplicadas en los controladores; la base es la fuente de verdad.")

    doc.add_heading("6.1 Flujo integral", level=2)
    figura(doc, FIGURAS / "flujo_prestamo.png", "Flujo integral de una operación de entrada y salida.", ancho=16.2)
    par(doc,
        "El flujo del préstamo resume la integración. El responsable completa el formulario; React valida y envía un "
        "POST con el token; el controlador verifica el rol y el DTO; el servicio aplica las reglas; el repositorio "
        "inserta el préstamo y actualiza el equipo dentro de una transacción; PostgreSQL confirma; la API devuelve 201 "
        "con el DTO completo; React muestra el banner, el toast y el acceso al historial. Si cualquier paso falla, el "
        "error se propaga con un mensaje útil y no se confirma la transacción.")

    doc.add_heading("6.2 Integración frontend y API", level=2)
    par(doc,
        "El frontend conoce la URL de la API mediante VITE_API_URL, con valor por defecto http://localhost:5143/api. El "
        "cliente api.js agrega el token desde localStorage, interpreta el JSON y convierte los errores en ErrorApi. "
        "Cuando la API responde 401 en una ruta protegida, se emite el evento sesion-expirada y el contexto cierra la "
        "sesión; cuando responde 403, la interfaz muestra el mensaje de permiso sin cerrar la sesión.")
    tabla(
        doc,
        ["Mecanismo", "Implementación", "Evidencia"],
        [
            ("URL base", "VITE_API_URL o http://localhost:5143/api.", "Login y todas las consultas."),
            ("Token", "Authorization: Bearer <token> en cada petición.", "Topbar «API y PostgreSQL en línea»."),
            ("CORS", "Política AllowFrontend para localhost:5173 y 127.0.0.1:5173.", "Consultas desde la SPA."),
            ("Errores", "ErrorApi con estado y errores por campo; mensajes del backend.", "Login, formularios y reglas."),
            ("Sesión expirada", "Evento global y redirección al login.", "Interceptor de 401."),
            ("Descargas", "Blob con token y nombre de archivo.", "Reportes CSV."),
        ],
        [3.4, 9.4, 4.0],
        "Puntos de integración frontend-API.",
    )

    doc.add_heading("6.3 Integración API y persistencia", level=2)
    par(doc,
        "Los controladores reciben DTO, validan el modelo y delegan en los servicios. Los servicios usan interfaces de "
        "repositorio y una unidad de trabajo; la infraestructura implementa esas interfaces con EF Core. El registro de "
        "dependencias se configura en Program.cs y la migración se aplica al iniciar la API, de modo que el sistema "
        "quede operativo con una base vacía.")
    codigo(doc, [
        "builder.Services.AddScoped<IUsuarioRepository, UsuarioRepository>();",
        "builder.Services.AddScoped<IEquipoRepository, EquipoRepository>();",
        "builder.Services.AddScoped<IPrestamoRepository, PrestamoRepository>();",
        "builder.Services.AddScoped<IUsuarioService, UsuarioService>();",
        "builder.Services.AddScoped<IEquipoService, EquipoService>();",
        "builder.Services.AddScoped<IPrestamoService, PrestamoService>();",
        "builder.Services.AddScoped<IReporteService, ReporteService>();",
        "builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();",
    ], "Registro de dependencias por capa")
    par(doc,
        "La separación permitió incorporar la transacción sin cambiar los controladores ni el frontend: se agregó "
        "IUnitOfWork, se implementó con BeginTransactionAsync y se envolvieron las dos escrituras del préstamo y de la "
        "devolución. El resto del sistema siguió igual, lo que confirma el valor de la arquitectura.")

    doc.add_heading("6.4 Base de datos y migraciones", level=2)
    par(doc,
        "La base TechAssetDB se creó con PostgreSQL 18. La migración InitialCreate define las tres tablas del núcleo, los índices "
        "únicos de correo y código patrimonial, los índices de consulta y las claves foráneas con borrado restringido. "
        "Al iniciar la API se ejecuta Database.Migrate() y se crea el administrador inicial si la tabla está vacía.")
    tabla(
        doc,
        ["Elemento", "Configuración"],
        [
            ("Motor", "PostgreSQL 18, base TechAssetDB."),
            ("Cadena de conexión", "Host=localhost;Port=5432;Database=TechAssetDB;Username=postgres;Password=postgres."),
            ("Migración", "InitialCreate (20261117222029) aplicada automáticamente."),
            ("Tablas", "Usuarios, Equipos, Prestamos."),
            ("Índices únicos", "Usuarios.Correo, Equipos.CodigoPatrimonial."),
            ("Índices de consulta", "Equipos.Estado, Prestamos(EquipoId, Estado), Prestamos(UsuarioId, FechaPrestamo)."),
            ("Borrado", "RESTRICT en las tres relaciones de Prestamos."),
            ("Datos iniciales", "Administrador admin@innovatech.pe / Admin.2026*."),
        ],
        [4.4, 11.6],
        "Configuración de la base de datos.",
    )

    doc.add_heading("6.5 Evidencias de integración", level=2)
    par(doc,
        "La barra superior muestra el estado de la conexión: «API y PostgreSQL en línea» cuando la consulta de resumen "
        "responde, «Verificando conexión...» mientras espera y «Sin conexión con la API» si falla. Esa señal es una "
        "evidencia visual de que el frontend está consumiendo datos reales y no un arreglo local.")
    figura(doc, CAPTURAS / "23-swagger.png", "Swagger documenta los 26 endpoints y sus permisos.", ancho=16.0)
    tabla(
        doc,
        ["Verificación", "Resultado"],
        [
            ("API en ejecución", "http://localhost:5143 · Swagger 200"),
            ("SPA en ejecución", "http://localhost:5173 · login 200"),
            ("Autenticación", "Login con admin, Administrador, Responsable, Colaborador y clave temporal."),
            ("Origen de datos", "Consultas visibles en los logs de EF Core y en PostgreSQL."),
            ("Registros", "18 equipos, 13 usuarios y 17 préstamos de demostración."),
            ("Pruebas", "50 escenarios de API y 12 comprobaciones de integridad conformes."),
        ],
        [6.0, 10.0],
        "Evidencias de integración verificadas.",
    )
    par(doc,
        "El código completo se publicó en https://github.com/CRAXCAT/TechAsset. La Figura 45 del Anexo H muestra la "
        "portada del repositorio con el README, la estructura del proyecto y la rama main; el repositorio es público y "
        "no requiere autenticación para su consulta.")

    doc.add_heading("6.6 Consistencia de las operaciones", level=2)
    par(doc,
        "Las operaciones que afectan dos tablas se ejecutan dentro de una transacción. Al registrar un préstamo se "
        "inserta el préstamo y se actualiza el equipo a Prestado; al devolver, se actualiza el préstamo y el equipo a "
        "Disponible. Si la segunda escritura falla, la primera se revierte. La unidad de trabajo comparte el mismo "
        "DbContext scoped de la petición, por lo que ambas operaciones participan de la misma transacción.")
    codigo(doc, [
        "await unitOfWork.EjecutarAsync(async () =>",
        "{",
        "    await prestamoRepository.AgregarAsync(prestamo);",
        "    await equipoRepository.ActualizarAsync(equipo);",
        "    return true;",
        "});",
    ], "Transacción de registro de préstamo")
    par(doc,
        "La validación de reglas ocurre antes de abrir la transacción. Así se evita mantener bloqueos durante "
        "comprobaciones que pueden resolverse con una consulta de lectura. La restricción única de la base sigue siendo "
        "la última defensa ante condiciones de carrera.")

    doc.add_heading("6.7 Aprobación transaccional", level=2)
    par(doc,
        "La aprobación de una solicitud es la operación de integración más exigente porque afecta tres tablas y un "
        "registro de auditoría. El servicio comprueba que la solicitud siga Pendiente, que el equipo esté Disponible y "
        "que no exista un préstamo activo; luego abre una transacción y ejecuta el alta del préstamo, el cambio del "
        "equipo a Prestado, la vinculación de la solicitud con el préstamo y el movimiento de auditoría. Si una parte "
        "falla, la transacción se revierte y no queda un préstamo sin solicitud ni un equipo marcado sin préstamo.")
    tabla(
        doc,
        ["Paso", "Operación", "Garantía"],
        [
            ("1", "Verificar solicitud Pendiente.", "No se aprueba dos veces (S-05)."),
            ("2", "Revalidar equipo disponible y sin préstamo activo.", "Si otro proceso lo ocupó, responde 409 (S-15)."),
            ("3", "Insertar el préstamo Activo.", "Índice único parcial por equipo activo (DB-01)."),
            ("4", "Actualizar el equipo a Prestado.", "El estado y el préstamo quedan consistentes."),
            ("5", "Vincular la solicitud con PrestamoId y el revisor.", "CHECK de aprobación (DB-05/DB-06)."),
            ("6", "Registrar el movimiento de auditoría.", "Actor, fecha y detalle del evento."),
            ("7", "Confirmar la transacción.", "Todo o nada; error controlado si falla."),
        ],
        [1.4, 7.4, 8.0],
        "Pasos de la aprobación transaccional.",
        fuente=7.6,
    )
    par(doc,
        "La prueba S-15 demuestra la revalidación: se crea una solicitud para un equipo, se ocupa el equipo con un "
        "préstamo directo y luego se intenta aprobar la solicitud; la API responde 409 y el equipo conserva el "
        "préstamo directo. Las pruebas DB-01, DB-05, DB-06 y DB-07 demuestran que la base también rechaza las "
        "combinaciones inválidas aunque se intente saltar el servicio.")


# --------------------------------------------------------------------------
# 7. Evaluación funcional
# --------------------------------------------------------------------------
def cargar_pruebas():
    ruta = BASE / "pruebas-api.json"
    if not ruta.exists():
        return []
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    return datos.get("resultados", [])


def cargar_integridad():
    ruta = BASE / "pruebas-integridad.json"
    if not ruta.exists():
        return []
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    return datos.get("resultados", [])


def seccion_7(doc):
    doc.add_heading("7. EVALUACIÓN FUNCIONAL", level=1)
    par(doc,
        "La evaluación combina pruebas automatizadas de API, escenarios de interfaz con capturas y una matriz de "
        "trazabilidad. El objetivo es demostrar que el sistema cumple los requerimientos y las reglas, no solo que "
        "compila o que las pantallas se ven bien.")

    doc.add_heading("7.1 Estrategia de pruebas", level=2)
    par(doc,
        "Se definieron cuatro niveles. Las pruebas de API verifican contratos, validaciones, permisos y reglas con "
        "peticiones reales; las pruebas de interfaz recorren los flujos principales con Playwright y generan capturas; "
        "la revisión de integración comprueba que los datos persistan y que las consultas reflejen los cambios. Cada "
        "escenario tiene un código, una entrada, un resultado esperado y un resultado obtenido.")
    tabla(
        doc,
        ["Nivel", "Herramienta", "Alcance", "Resultado"],
        [
            ("API", "Python urllib + JSON", "Autenticación, permisos, validaciones, RN, filtros, solicitudes y reportes.", "50/50 conformes"),
            ("Integridad", "psql + transacciones revertidas", "Índices parciales, CHECK, claves foráneas y estados.", "12/12 rechazos correctos"),
            ("Interfaz", "Playwright + Chromium", "Login, dashboard, formularios, solicitudes, aprobación, auditoría, filtros y móvil.", "40 capturas"),
            ("Compilación", "dotnet build / npm run build", "Backend y frontend.", "0 errores; 82 módulos"),
        ],
        [2.6, 5.2, 7.0, 2.8],
        "Niveles de verificación.",
    )

    doc.add_heading("7.2 Pruebas de API", level=2)
    par(doc,
        "Se ejecutaron 50 escenarios agrupados en cinco categorías. La tabla resume el alcance y el resultado; el "
        "detalle completo, con la entrada y el código HTTP obtenido, se presenta en el Anexo C.")
    tabla(
        doc,
        ["Categoría", "Escenarios", "Códigos", "Cobertura", "Resultado"],
        [
            ("Autenticación y permisos", "8", "A-01 a A-08", "Login, token, roles, alcance por rol y acceso a usuarios, reportes y auditoría.", "8/8"),
            ("Usuarios", "2", "U-01 a U-02", "Correo duplicado (RN-08) y dominio no permitido.", "2/2"),
            ("Equipos", "4", "E-01 a E-04", "Código duplicado (RN-07), categoría inválida, estado Prestado manual y borrado con historial (RN-06).", "4/4"),
            ("Préstamos", "20", "R-01 a R-20", "Alta, reglas, devolución, filtros, historial propio, reportes y exportación.", "20/20"),
            ("Solicitudes", "16", "S-01 a S-16", "Creación, duplicados, aprobación, rechazo, concurrencia y alcance por rol.", "16/16"),
            ("Total", "50", "—", "Reglas, validaciones, consultas, solicitudes y auditoría.", "50/50"),
        ],
        [3.4, 2.0, 3.0, 6.6, 1.8],
        "Resumen de pruebas de API por categoría.",
        fuente=7.8,
    )
    codigo(doc, [
        "PS> python docs/scripts/pruebas_api.py",
        "OK  A-01 HTTP 200 -> admin@innovatech.pe · Administrador",
        "OK  A-02 HTTP 401 -> Correo o contraseña incorrectos.",
        "OK  E-01 HTTP 409 -> Ya existe un equipo con ese código patrimonial (RN-07).",
        "OK  R-01 HTTP 201 -> PR-980CF5 · Activo",
        "OK  R-02 HTTP 409 -> El equipo ya tiene un préstamo activo (RN-01).",
        "OK  R-09 HTTP 400 -> Revise los datos enviados...",
        "OK  R-10 HTTP 200 -> PR-980CF5 · Devuelto",
        "OK  S-04 HTTP 200 -> SOL-545EE7 · Aprobada",
        "OK  S-08 HTTP 200 -> SOL-71980B · Rechazada",
        "...",
        "Resultado: 50/50 escenarios conformes",
    ], "Salida resumida de la ejecución")

    doc.add_heading("7.3 Pruebas de interfaz", level=2)
    par(doc,
        "Los escenarios de interfaz recorren los flujos que un evaluador usaría en una demostración. Cada uno se "
        "ejecutó en Chromium con un viewport de escritorio y, en los casos móviles, con un viewport de 390 × 844. Las "
        "capturas se generaron de forma automatizada para que sean reproducibles.")
    tabla(
        doc,
        ["Escenario", "Acción realizada", "Evidencia"],
        [
            ("Inicio de sesión", "Credenciales válidas y acceso al dashboard.", "Figura 5"),
            ("Error de acceso", "Contraseña incorrecta y mensaje genérico.", "Figura 6"),
            ("Portal público", "Portada, funciones, seguridad y acceso corporativo.", "Figuras 31 y 32"),
            ("Dashboard", "Indicadores, alerta y distribuciones.", "Figura 18"),
            ("Directorio", "Listado de usuarios con rol y estado.", "Figura 7"),
            ("Validación de usuario", "Envío vacío y errores por campo.", "Figura 8"),
            ("Alta de usuario", "Registro exitoso y confirmación visual.", "Figura 29"),
            ("Inventario", "Listado y filtros de equipos.", "Figura 9"),
            ("Validación de equipo", "Envío vacío y errores por campo.", "Figura 10"),
            ("Alta de equipo", "Registro exitoso y confirmación visual.", "Figura 30"),
            ("Historial", "Listado paginado de préstamos.", "Figura 16"),
            ("Filtros", "Estado y área combinados en la URL.", "Figura 17"),
            ("Detalle", "Trazabilidad del préstamo.", "Figura 20"),
            ("Devolución", "Observación obligatoria y confirmación.", "Figura 14"),
            ("Nuevo préstamo", "Formulario, validación y alta exitosa.", "Figuras 11 a 13"),
            ("Reportes", "Indicadores, gráficos y listados.", "Figura 19"),
            ("Ayuda", "Atajos y reglas.", "Figura 25"),
            ("Modo oscuro", "Contraste y jerarquía visual.", "Figura 26"),
            ("Móvil", "Login y dashboard adaptados.", "Figuras 27 y 28"),
            ("Cambio de clave", "Contraseña temporal obligatoria.", "Figura 23"),
            ("Restricción por rol", "Responsable sin permiso de usuarios.", "Figura 24"),
            ("Bandeja de solicitudes", "Pendientes primero; acciones de revisión.", "Figura 33"),
            ("Aprobación de solicitud", "Observación y generación del préstamo.", "Figuras 34 y 35"),
            ("Auditoría", "Movimientos con actor, fecha y detalle.", "Figura 36"),
            ("Dashboard del Colaborador", "Solicitudes pendientes e historial propio.", "Figura 37"),
            ("Mis solicitudes", "Estados Pendiente, Aprobada y Rechazada.", "Figura 38"),
            ("Nueva solicitud", "Formulario y validación de campos.", "Figuras 39 y 40"),
            ("Solicitud registrada", "Confirmación con código y fechas.", "Figura 41"),
            ("Mi historial", "Solo préstamos del Colaborador.", "Figura 42"),
            ("Equipos del Colaborador", "Consulta y acción Solicitar.", "Figura 43"),
            ("Detalle de solicitud", "Trazabilidad y vínculo con el préstamo.", "Figura 44"),
        ],
        [4.4, 8.4, 4.0],
        "Escenarios de interfaz y evidencia.",
        fuente=7.6,
    )
    figura(doc, CAPTURAS / "19-cambiar-clave.png", "Cambio obligatorio de la contraseña temporal.", ancho=16.0)
    figura(doc, CAPTURAS / "20-usuarios-responsable.png", "El rol Responsable consulta usuarios, pero no puede gestionarlos (RN-09).", ancho=16.0)

    doc.add_heading("7.4 Trazabilidad de requerimientos", level=2)
    par(doc,
        "La matriz relaciona cada requerimiento con la sección donde se implementa, la figura que lo evidencia y los "
        "escenarios de prueba que lo cubren. Esto permite verificar la cobertura sin recorrer todo el informe.")
    tabla(
        doc,
        ["RF", "Sección", "Evidencia", "Pruebas"],
        [
            ("RF-01", "3.2", "Figuras 7, 8 y 29", "A-04, U-01, U-02"),
            ("RF-02", "3.2", "Figura 7", "A-04, U-01"),
            ("RF-03", "3.2 / 5.1", "Figura 7", "A-03"),
            ("RF-04", "3.2", "Figura 7", "A-05, R-07"),
            ("RF-05", "3.3", "Figuras 9, 10 y 30", "E-01, E-02"),
            ("RF-06", "3.3", "Figura 9", "E-01, E-03"),
            ("RF-07", "5.1", "Figura 9", "R-12"),
            ("RF-08", "3.3", "Figura 9", "E-03"),
            ("RF-09", "3.4", "Figuras 11 a 13", "R-01 a R-08, R-15"),
            ("RF-10", "3.5", "Figura 14", "R-09 a R-11"),
            ("RF-11", "5.1 / 5.7", "Figuras 16, 17 y 42", "R-13, R-14, R-19"),
            ("RF-12", "5.1 / 5.3", "Figuras 16 y 18", "R-13"),
            ("RF-13", "5.3", "Figura 18", "R-16"),
            ("RF-14", "5.4", "Figuras 18 y 19", "R-16"),
            ("RF-15", "5.4", "Figura 19", "R-16"),
            ("RF-16", "5.4", "Figura 19", "R-16"),
            ("RF-17", "5.6 / 5.7", "Figuras 20 y 36", "R-10, R-11, S-16"),
        ],
        [1.5, 2.6, 5.0, 7.7],
        "Matriz de trazabilidad de requerimientos.",
        fuente=7.6,
    )
    tabla(
        doc,
        ["Extensión", "Sección", "Evidencia", "Pruebas"],
        [
            ("EF-01 Solicitud de equipo", "3.7", "Figuras 39 a 41", "S-01, S-02, S-06"),
            ("EF-02 Aprobación/rechazo", "3.7 / 6.7", "Figuras 33 a 35 y 44", "S-03 a S-08, S-15"),
            ("EF-03 Historial por rol", "5.7", "Figuras 37, 38, 42 y 43", "R-19, S-10, A-06, A-07"),
            ("EF-04 Auditoría", "5.7", "Figura 36", "S-16, A-08, DB-09 a DB-12"),
            ("EF-05 Portal público", "3.1 / Anexo E", "Figuras 31 y 32", "Revisión de interfaz"),
        ],
        [4.2, 3.0, 6.2, 3.4],
        "Trazabilidad de las ampliaciones funcionales.",
        fuente=7.6,
    )

    doc.add_heading("7.5 Cobertura de reglas de negocio", level=2)
    par(doc,
        "Las diez reglas tienen al menos una prueba negativa y una positiva cuando corresponde. Las pruebas negativas "
        "verifican que la API rechace la operación con el código correcto; las positivas confirman que la operación "
        "válida se completa y persiste.")
    tabla(
        doc,
        ["Regla", "Prueba negativa", "Prueba positiva", "Resultado"],
        [
            ("RN-01", "R-02: segundo préstamo del mismo equipo.", "R-01: primer préstamo válido.", "Conforme"),
            ("RN-02", "R-03: equipo en Mantenimiento.", "R-12: equipo disponible tras devolución.", "Conforme"),
            ("RN-03", "R-04: equipo en Baja.", "—", "Conforme"),
            ("RN-04", "R-05: devolución el mismo día.", "R-01: fechas válidas.", "Conforme"),
            ("RN-05", "R-15: préstamo con rol Colaborador.", "R-01: préstamo con Administrador.", "Conforme"),
            ("RN-06", "E-04: eliminación con historial.", "—", "Conforme"),
            ("RN-07", "E-01: código patrimonial duplicado.", "E-02: alta con código nuevo.", "Conforme"),
            ("RN-08", "U-01: correo duplicado.", "A-01: alta y login del administrador.", "Conforme"),
            ("RN-09", "A-05: Responsable deshabilita usuario.", "R-07: Administrador deshabilita y rehabilita.", "Conforme"),
            ("RN-10", "R-09: devolución sin observación.", "R-10: devolución con observación.", "Conforme"),
            ("RN-11", "S-02: solicitud duplicada para el equipo.", "S-01: primera solicitud pendiente.", "Conforme"),
            ("RN-12", "DB-05/DB-06: aprobación sin préstamo o pendiente con préstamo.", "S-04: aprobación con préstamo vinculado.", "Conforme"),
            ("RN-13", "A-06/A-07: Colaborador intenta usuarios o CSV.", "R-19/S-10: solo ve sus registros.", "Conforme"),
            ("RN-14", "A-08: Colaborador intenta la auditoría.", "S-16: Administrador consulta movimientos.", "Conforme"),
        ],
        [1.5, 6.5, 6.6, 2.2],
        "Cobertura de las reglas de negocio.",
        fuente=7.6,
    )

    doc.add_heading("7.6 Resultados y análisis", level=2)
    par(doc,
        "Los 50 escenarios de API y las 12 comprobaciones de integridad resultaron conformes. No se encontraron defectos "
        "críticos en la versión evaluada. Durante el desarrollo se identificaron y corrigieron situaciones que quedaron "
        "documentadas como parte del refinamiento:")
    tabla(
        doc,
        ["Hallazgo", "Causa", "Corrección aplicada"],
        [
            ("El préstamo duplicaba entidades al insertar.", "Se asignaban las navegaciones Usuario, Equipo y Responsable además de las claves foráneas.", "Se conservaron solo las claves; el mapeo de respuesta recibe las entidades cargadas."),
            ("El estado Prestado podía asignarse manualmente.", "El formulario de equipo ofrecía todos los estados.", "Se excluyó Prestado y el servicio lo rechaza; solo se asigna al crear un préstamo."),
            ("La eliminación de equipos rompía el historial.", "No existía verificación de préstamos asociados.", "Se bloqueó con RN-06 y se sugiere el estado Baja."),
            ("El historial global exponía registros de otros colaboradores.", "La consulta no filtraba por propietario.", "Se agregó filtro por UsuarioId, guardas de ruta y 403 en usuarios, reportes y auditoría."),
            ("La aprobación no existía y el registro directo no era suficiente.", "El caso atribuye al Responsable la función de aprobar préstamos.", "Se añadió Solicitud, aprobación transaccional y vínculo con el préstamo."),
            ("No había trazabilidad de las operaciones.", "Solo se conservaba el historial de préstamos.", "Se agregó Movimientos y su consulta de solo lectura para gestores."),
            ("Dos solicitudes pendientes podían competir por el mismo equipo.", "La verificación era solo lógica.", "Se agregó un índice único parcial por equipo pendiente (DB-07)."),
            ("Las dos escrituras del préstamo no eran atómicas.", "Cada repositorio confirmaba por separado.", "Se agregó UnitOfWork y una transacción para préstamo, equipo, solicitud y auditoría."),
        ],
        [5.2, 5.6, 6.0],
        "Hallazgos y correcciones del refinamiento.",
        fuente=7.4,
    )
    par(doc,
        "El análisis de resultados muestra que las reglas con mayor riesgo son las que combinan estado, fechas y "
        "concurrencia: RN-01 a RN-04 y RN-11. Por eso se probaron con entradas directas a la API y con transacciones "
        "revertidas en PostgreSQL, no solo desde la interfaz. También se verificó que los permisos se apliquen en el "
        "servidor: el Colaborador recibe 403 al intentar usuarios, exportaciones o auditoría, y solo obtiene sus "
        "propios préstamos y solicitudes; el Responsable puede revisar solicitudes, pero no administrar cuentas.")


# --------------------------------------------------------------------------
# 8. Usabilidad
# --------------------------------------------------------------------------
def seccion_8(doc):
    doc.add_heading("8. USABILIDAD Y GUÍA DE USO", level=1)
    par(doc,
        "La interfaz se evaluó con la guía combinada de Jakob Nielsen y Ben Shneiderman. No se trata de una lista "
        "decorativa: cada principio se relaciona con una decisión concreta y con una figura que la evidencia.")

    doc.add_heading("8.1 Nielsen y Shneiderman", level=2)
    tabla(
        doc,
        ["Principio", "Implementación en TechAsset", "Evidencia"],
        [
            ("Visibilidad del estado", "Indicadores, esqueletos de carga, toasts, estado de la API y botones «Guardando...».", "Figuras 13 y 18"),
            ("Consistencia y estándares", "Mismo layout, componentes, colores y lenguaje en todos los módulos.", "Todas las figuras"),
            ("Hablar el lenguaje del usuario", "«Inventario», «Préstamo», «Devolución», «Disponible», «Mantenimiento».", "Figuras 9, 11 y 18"),
            ("Control y libertad", "Cancelar, cerrar con Escape, limpiar filtros, volver y deshacer la selección.", "Figuras 7, 11 y 16"),
            ("Prevención de errores", "Validación doble, catálogos cerrados, equipos disponibles y confirmación de estados.", "Figuras 8, 10 y 12"),
            ("Reconocimiento antes que recuerdo", "Ayudas, reglas visibles, ejemplos de correo y filtros persistentes en la URL.", "Figuras 5, 11 y 25"),
            ("Eficiencia y simplicidad", "Una tarea principal por pantalla, atajos y accesos rápidos.", "Figuras 18 y 25"),
            ("Diseño minimalista", "Jerarquía tipográfica, espacio en blanco y una acción primaria por vista.", "Todas las figuras"),
            ("Mensajes que explican y solucionan", "Error junto al campo, causa y condición para corregirlo.", "Figuras 6, 8 y 14"),
            ("Prevenir y confirmar acciones destructivas", "Confirmación antes de eliminar, devolver o cambiar estado.", "Figuras 9 y 14"),
            ("Ayuda y documentación", "Ayuda contextual, atajos, reglas y README.", "Figura 25"),
            ("Accesibilidad", "Foco visible, etiquetas, aria-live, teclado, contraste y modo oscuro.", "Figuras 25 a 28"),
        ],
        [4.4, 9.6, 2.8],
        "Guía de Nielsen y Shneiderman aplicada.",
        fuente=7.4,
    )
    par(doc,
        "La aplicación de la guía se verificó con acciones concretas: recorrer el formulario solo con Tab, cerrar el "
        "modal con Escape, comprobar que el foco vuelve al botón de origen, leer los errores con un lector de pantalla "
        "y cambiar el tema sin perder la sesión. Esas comprobaciones son parte de la evaluación de usabilidad y no "
        "solo del diseño visual.")

    doc.add_heading("8.2 Ayuda y atajos", level=2)
    par(doc,
        "La ayuda está disponible desde la barra superior, el menú lateral y la tecla ?. Incluye los atajos Alt+I, Alt+U, "
        "Alt+E, Alt+P, Alt+R, /, ? y Esc, las reglas del préstamo y criterios de accesibilidad. Los atajos se desactivan "
        "mientras el foco está en un campo de texto para no interferir con la escritura.")
    figura(doc, CAPTURAS / "05-ayuda.png", "Ayuda contextual con atajos, reglas y accesibilidad.", ancho=15.2)
    tabla(
        doc,
        ["Atajo", "Acción"],
        [
            ("Alt + I", "Ir al panel de control."),
            ("Alt + U", "Abrir usuarios."),
            ("Alt + E", "Abrir inventario de equipos."),
            ("Alt + S", "Abrir solicitudes."),
            ("Alt + P", "Abrir préstamos."),
            ("Alt + R", "Abrir reportes."),
            ("Alt + M", "Abrir movimientos."),
            ("/", "Enfocar el buscador de la página."),
            ("?", "Abrir la ayuda."),
            ("Esc", "Cerrar ventanas y confirmaciones."),
        ],
        [4.0, 12.0],
        "Atajos de teclado.",
    )

    doc.add_heading("8.3 Modo oscuro y diseño móvil", level=2)
    par(doc,
        "El tema claro u oscuro se conserva en localStorage y respeta la preferencia del sistema en la primera visita. "
        "El modo oscuro no invierte colores: redefine variables de fondo, superficie, texto, borde y estados para "
        "mantener el contraste. La vista móvil convierte la tabla en tarjetas, el menú en panel deslizante y los "
        "formularios en una columna, sin perder acciones ni mensajes. El portal público también se adapta a móvil "
        "(Figura 32). El menú cambia según el rol: el Colaborador ve Inicio, Equipos, Mis solicitudes y Mi historial; "
        "el Responsable y el Administrador ven además Usuarios, Préstamos, Nuevo préstamo, Reportes y Movimientos.")
    figura(doc, CAPTURAS / "04-dashboard-oscuro.png", "Modo oscuro del dashboard con contraste y jerarquía conservados.", ancho=16.2)
    figura(doc, CAPTURAS / "21-login-movil.png", "Acceso adaptado a móvil (390 × 844).", ancho=7.2)
    figura(doc, CAPTURAS / "22-dashboard-movil.png", "Dashboard en móvil con menú deslizante y tarjetas.", ancho=7.2)

    doc.add_heading("8.4 Flujo de uso recomendado", level=2)
    for texto in [
        "Abrir el portal público, revisar las funciones y elegir «Acceso corporativo».",
        "Ingresar con una cuenta corporativa; si es la primera vez, cambiar la contraseña temporal.",
        "Revisar el dashboard para conocer el inventario, los préstamos activos y el área con mayor uso.",
        "Consultar el inventario y filtrar por categoría o estado antes de asignar un equipo.",
        "Si el usuario es Colaborador, registrar una solicitud y esperar la revisión; si es Responsable, revisar la bandeja y aprobar o rechazar con observación.",
        "Registrar el préstamo directo cuando la operación sea presencial y el rol lo permita; verificar la confirmación.",
        "Consultar el historial para hacer seguimiento y registrar la devolución con observaciones.",
        "Revisar reportes y descargar el CSV cuando se necesite compartir la información.",
        "Usar la ayuda y los atajos para operar con mayor rapidez; cambiar el tema según la preferencia.",
    ]:
        vineta(doc, texto)

    doc.add_heading("8.5 Credenciales de demostración", level=2)
    par(doc,
        "Las cuentas siguientes se cargan con el script de datos. El administrador inicial se crea automáticamente si "
        "la base está vacía y las demás cuentas se generan con contraseña temporal. La cuenta con Temporal.2026* obliga "
        "a cambiar la clave en el primer ingreso.")
    tabla(
        doc,
        ["Cuenta", "Correo", "Contraseña", "Rol / propósito"],
        [
            ("Administrador inicial", "admin@innovatech.pe", "Admin.2026*", "Administrador · cuenta base del sistema."),
            ("Kevin Ccente", "kevin.ccente@innovatech.pe", "Tech.2026*", "Administrador · demostración principal."),
            ("Lucía Paredes", "lucia.paredes@innovatech.pe", "Tech.2026*", "Responsable · tecnología."),
            ("Pedro Ccahuana", "pedro.ccahuana@innovatech.pe", "Tech.2026*", "Responsable · soporte."),
            ("Rosa Quispe", "rosa.quispe@innovatech.pe", "Tech.2026*", "Colaborador · consulta."),
            ("Diego Flores", "diego.flores@innovatech.pe", "Temporal.2026*", "Colaborador · cambio obligatorio de clave."),
        ],
        [3.6, 5.6, 3.4, 5.4],
        "Cuentas de demostración.",
        fuente=7.8,
    )


# --------------------------------------------------------------------------
# 9. Conclusiones
# --------------------------------------------------------------------------
def seccion_9(doc):
    doc.add_heading("9. CONCLUSIONES Y RECOMENDACIONES", level=1)
    doc.add_heading("9.1 Conclusiones", level=2)
    for texto in [
        "TechAsset resuelve el problema de dispersión de la información con una fuente única de verdad para usuarios, equipos y préstamos, y con reglas verificadas en el servidor.",
        "Los 17 requerimientos funcionales y las 10 reglas de negocio del caso quedaron implementados y trazados a una sección, una figura y una prueba concreta; se añadieron cuatro reglas de integridad para solicitudes, alcance y auditoría.",
        "La arquitectura por capas permitió incorporar autenticación, transacciones, solicitudes y reportes sin reescribir los módulos; los controladores quedaron delgados y las reglas concentradas en Application.",
        "La reutilización de 22 componentes, 10 hooks y 8 servicios redujo la duplicación y hizo que los cambios de estilo, validación y comportamiento se appliquen en un solo lugar.",
        "La validación en dos capas mejoró la experiencia y la integridad: el usuario recibe ayuda inmediata y la API rechaza cualquier dato inválido aunque la petición no provenga de la interfaz.",
        "El flujo de solicitud, aprobación transaccional, historial por rol y auditoría cubre las funciones de los tres actores y evita que el Colaborador acceda a información de otras cuentas.",
        "La evaluación funcional con 50 escenarios de API, 12 comprobaciones de integridad y 40 capturas demuestra el funcionamiento integral y deja evidencia reproducible para la sustentación.",
    ]:
        vineta(doc, texto)

    doc.add_heading("9.2 Limitaciones", level=2)
    for texto in [
        "No se envían correos automáticos de bienvenida, recuperación de contraseña ni notificaciones de vencimiento.",
        "La exportación disponible es CSV; no se generan PDF ni reportes programados.",
        "El despliegue es local y no incluye contenedores, CI/CD ni monitoreo centralizado.",
        "La auditoría es de solo lectura desde la aplicación y no incluye firma digital ni retención automática; se conserva mientras no se elimine la base.",
        "Las pruebas automatizadas cubren la API, la integridad y los flujos de interfaz, pero no incluyen pruebas unitarias formales de todos los servicios ni una evaluación con usuarios reales.",
    ]:
        vineta(doc, texto)

    doc.add_heading("9.3 Trabajo futuro", level=2)
    tabla(
        doc,
        ["Mejora", "Beneficio esperado"],
        [
            ("Notificaciones por correo y recordatorios de devolución.", "Menos préstamos vencidos y mejor seguimiento."),
            ("Reportes en PDF y programación de envíos.", "Información lista para presentar a gerencia."),
            ("Exportación y retención de la auditoría.", "Archivo histórico consultable y política de conservación."),
            ("Notificaciones en tiempo real y recordatorios.", "Menos solicitudes olvidadas y devoluciones vencidas."),
            ("Pruebas unitarias con xUnit y cobertura.", "Detección temprana de regresiones en servicios y reglas."),
            ("Contenedores y CI/CD.", "Despliegue reproducible y entrega continua."),
            ("Integración con directorio corporativo o SSO.", "Menos cuentas manuales y mejor gobierno de identidades."),
            ("Aplicación móvil o PWA instalable.", "Acceso rápido desde el lugar donde se encuentra el equipo."),
        ],
        [8.0, 8.0],
        "Mejoras propuestas para una segunda versión.",
    )

    doc.add_heading("9.4 Reflexión final", level=2)
    par(doc,
        "La aplicación de estándares de construcción, validación de datos, reutilización de componentes, refinamiento, "
        "programación orientada a objetos e integración de módulos mejora la calidad porque reduce la ambigüedad y "
        "hace explícitas las reglas. Un estándar de nombres y una separación por capas permiten que otra persona "
        "encuentre el código y lo cambie sin miedo; una validación en dos capas evita que un dato inválido llegue a la "
        "base; un componente reutilizable garantiza que la misma acción se vea y se comporte igual en todas las "
        "pantallas; el refinamiento elimina duplicaciones que, con el tiempo, se convierten en defectos inconsistentes.")
    par(doc,
        "La mantenibilidad se beneficia de la cohesión y del bajo acoplamiento: los servicios dependen de interfaces, "
        "los controladores no conocen EF Core y el frontend no conoce SQL. La escalabilidad se beneficia de la API sin "
        "estado, la paginación en servidor, los índices y la posibilidad de reemplazar repositorios o agregar caché sin "
        "tocar la lógica de negocio. En conjunto, TechAsset no es solo un conjunto de pantallas que funcionan: es una "
        "solución construida para evolucionar, con evidencia de que cumple lo que promete.")


# --------------------------------------------------------------------------
# Referencias y anexos
# --------------------------------------------------------------------------
def referencias(doc):
    doc.add_heading("REFERENCIAS", level=1)
    entradas = [
        "Fowler, M. (2018). Refactoring: Improving the Design of Existing Code (2.ª ed.). Addison-Wesley.",
        "Gamma, E., Helm, R., Johnson, R. y Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.",
        "Microsoft. (2025). ASP.NET Core documentation. https://learn.microsoft.com/aspnet/core",
        "Microsoft. (2025). Entity Framework Core documentation. https://learn.microsoft.com/ef/core",
        "Nielsen, J. (1994). Usability Engineering. Morgan Kaufmann.",
        "OWASP Foundation. (2024). Password Storage Cheat Sheet y JSON Web Token Cheat Sheet. https://cheatsheetseries.owasp.org",
        "PostgreSQL Global Development Group. (2025). PostgreSQL 18 Documentation. https://www.postgresql.org/docs/18/",
        "Pressman, R. y Maxim, B. (2020). Ingeniería del software: un enfoque práctico (9.ª ed.). McGraw-Hill.",
        "React Team. (2025). React documentation. https://react.dev",
        "Shneiderman, B., Plaisant, C., Cohen, M., Jacobs, S. y Elmqvist, N. (2016). Designing the User Interface: Strategies for Effective Human-Computer Interaction (6.ª ed.). Pearson.",
        "Sommerville, I. (2016). Software Engineering (10.ª ed.). Pearson.",
    ]
    for entrada in entradas:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.8)
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.add_run(entrada)


def anexos(doc):
    doc.add_heading("ANEXOS", level=1)
    doc.add_heading("Anexo A. Estructura de carpetas", level=2)
    codigo(doc, [
        "TechAsset/",
        "├─ backend/TechAsset.Domain/Entities/Usuario.cs, Equipo.cs, Prestamo.cs, Solicitud.cs, Movimiento.cs",
        "├─ backend/TechAsset.Domain/Constantes/CatalogoTechAsset.cs",
        "├─ backend/TechAsset.Application/DTOs/TechAssetDtos.cs",
        "├─ backend/TechAsset.Application/Interfaces/ (repositorios, servicios, unidad de trabajo)",
        "├─ backend/TechAsset.Application/Services/ (Usuario, Equipo, Prestamo, Solicitud, Movimiento, Reporte, Auth)",
        "├─ backend/TechAsset.Infrastructure/Data/ (AppDbContext, UnitOfWork, InicializadorDatos)",
        "├─ backend/TechAsset.Infrastructure/Repositories/ (Usuario, Equipo, Prestamo, Solicitud, Movimiento)",
        "├─ backend/TechAsset.Infrastructure/Security/ (BCrypt, JWT)",
        "├─ backend/TechAsset.API/Controllers/ (Auth, Usuarios, Equipos, Prestamos, Solicitudes, Movimientos, Reportes)",
        "├─ backend/TechAsset.API/Middleware/ManejadorErroresMiddleware.cs",
        "├─ frontend/src/components/ui/ (22 componentes)",
        "├─ frontend/src/pages/ (Inicio, Login, Dashboard, Usuarios, Equipos, Solicitudes, NuevaSolicitud, Prestamos, NuevoPrestamo, Reportes, Movimientos, CambiarClave)",
        "├─ frontend/src/hooks/ (10 hooks y contextos)",
        "├─ frontend/src/services/ (api y 7 servicios)",
        "└─ docs/scripts/ (seed, reinicio, pruebas, capturas y generación del informe)",
    ])

    doc.add_heading("Anexo B. Instalación y ejecución", level=2)
    par(doc, "Requisitos", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    for texto in [
        ".NET SDK 10, Node.js 20 o superior y PostgreSQL 18 en el puerto 5432.",
        "Base TechAssetDB con usuario postgres; la cadena se configura en backend/TechAsset.API/appsettings.json.",
        "Opcional: Python 3.12 con python-docx, pymupdf, matplotlib y playwright para reproducir el informe y las capturas.",
    ]:
        vineta(doc, texto)
    par(doc, "Backend", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    codigo(doc, [
        "cd TechAsset/backend",
        "dotnet restore",
        "dotnet ef database update --project TechAsset.Infrastructure --startup-project TechAsset.API",
        "dotnet run --project TechAsset.API --launch-profile http",
        "# API: http://localhost:5143 · Swagger: http://localhost:5143/swagger",
    ])
    par(doc, "Frontend", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    codigo(doc, [
        "cd TechAsset/frontend",
        "npm install",
        "npm run dev",
        "# Portal: http://localhost:5173/ · Panel: http://localhost:5173/panel",
    ])
    par(doc, "Datos y verificación", negrita=True, tamano=9.8, color=AZUL_OSCURO, espacio=2)
    codigo(doc, [
        "python docs/scripts/reiniciar_datos.py   # limpia y recarga la demostración",
        "python docs/scripts/pruebas_api.py        # 50 escenarios de API",
        "python docs/scripts/pruebas_integridad.py # 12 comprobaciones en PostgreSQL",
        "python docs/scripts/capturas.py           # 23 capturas de interfaz\npython docs/scripts/capturas_altas.py     # 2 capturas de altas\npython docs/scripts/capturas_solicitudes.py # 12 capturas del flujo de solicitudes",
        "python docs/scripts/informe_techasset.py  # genera el DOCX",
    ])
    nota(doc,
         "El script de capturas crea un préstamo temporal para evidenciar el alta exitosa. Después de ejecutarlo se "
         "recomienda reiniciar los datos o eliminar ese préstamo para volver al conjunto base de 17 registros.")

    doc.add_heading("Anexo C. Escenarios de prueba ejecutados", level=2)
    par(doc,
        "La tabla reproduce los 50 escenarios de docs/pruebas-api.json, con la entrada utilizada, el código HTTP "
        "obtenido y el resultado. Todos los escenarios resultaron conformes.")
    filas = []
    for r in cargar_pruebas():
        filas.append((r["codigo"], r["escenario"], str(r["entrada"]), str(r["http"]), "Conforme" if r["cumple"] else "No conforme"))
    if filas:
        tabla(
            doc,
            ["Código", "Escenario", "Entrada", "HTTP", "Resultado"],
            filas,
            [1.4, 7.4, 4.8, 1.4, 1.8],
            "Escenarios de prueba de API ejecutados.",
            fuente=7.0,
        )
    else:
        par(doc, "No se encontró docs/pruebas-api.json; ejecute docs/scripts/pruebas_api.py para regenerarlo.")

    doc.add_page_break()
    doc.add_heading("Anexo D. Altas de usuario y equipo", level=2)
    par(doc,
        "Los escenarios mínimos «registrar usuario» y «registrar equipo» se ejecutaron con datos temporales y se "
        "capturaron antes de retirarlos del conjunto de demostración. La primera captura muestra el aviso de "
        "confirmación y el usuario creado con contraseña temporal; la segunda muestra el equipo TA-0099 con estado "
        "Disponible y cero préstamos. Ambos registros se eliminaron después de la captura para conservar los conteos "
        "del informe (13 usuarios y 18 equipos).")
    figura(doc, CAPTURAS / "24-alta-usuario.png",
           "Alta exitosa de un usuario con contraseña temporal y correo único.", ancho=16.2)
    figura(doc, CAPTURAS / "25-alta-equipo.png",
           "Alta exitosa de un equipo con código patrimonial único y estado Disponible.", ancho=16.2)

    doc.add_page_break()
    doc.add_heading("Anexo E. Portal público de inicio", level=2)
    par(doc,
        "El portal público se publica en la ruta / y no requiere sesión. Su cabecera permite navegar a Funciones, "
        "Cómo funciona y Seguridad, cambiar el tema claro/oscuro y entrar a /login. El cuerpo presenta la propuesta de "
        "valor, una vista previa del panel, seis tarjetas de funciones, tres pasos de uso y una banda de seguridad. Si "
        "el usuario ya inició sesión, la cabecera muestra su nombre, su rol y el botón «Ir al panel»; si no, muestra "
        "«Iniciar sesión». El portal no consulta datos reales: la vista previa es estática y los datos del inventario "
        "solo se muestran después de autenticarse.")
    figura(doc, CAPTURAS / "26-portal-publico.png",
           "Portal público de inicio con acceso corporativo y vista previa del panel.", ancho=16.4)
    figura(doc, CAPTURAS / "27-portal-movil.png",
           "Portal público adaptado a móvil (390 × 844).", ancho=7.2)

    doc.add_page_break()
    doc.add_heading("Anexo F. Solicitudes y auditoría", level=2)
    par(doc,
        "Este anexo reúne las evidencias del flujo que ejercita el Colaborador, del proceso de revisión del "
        "Responsable y de la auditoría. Las capturas se obtuvieron de la aplicación en ejecución y conservan el rol "
        "que realizó cada acción. La solicitud no reserva el equipo; la aprobación vuelve a verificar la "
        "disponibilidad y genera el préstamo en una transacción.")
    figura(doc, CAPTURAS / "28-solicitudes-admin.png",
           "Bandeja de solicitudes del Administrador: pendientes primero, estados y acciones.", ancho=16.2)
    figura(doc, CAPTURAS / "30-solicitud-aprobacion.png",
           "Diálogo de aprobación con observación y advertencia de transacción.", ancho=16.2)
    figura(doc, CAPTURAS / "31-solicitud-aprobada.png",
           "Solicitud aprobada con el préstamo generado y el vínculo visible.", ancho=16.2)
    figura(doc, CAPTURAS / "32-movimientos.png",
           "Auditoría de movimientos con actor, entidad, acción y detalle.", ancho=16.2)
    figura(doc, CAPTURAS / "33-dashboard-colaborador.png",
           "Dashboard del Colaborador con solicitudes pendientes y métricas propias.", ancho=16.2)
    figura(doc, CAPTURAS / "34-mis-solicitudes.png",
           "Bandeja de solicitudes del Colaborador limitada a sus propios registros.", ancho=16.2)
    figura(doc, CAPTURAS / "35-nueva-solicitud.png",
           "Formulario de nueva solicitud con equipos disponibles y reglas visibles.", ancho=16.2)
    figura(doc, CAPTURAS / "36-nueva-solicitud-validacion.png",
           "Validación del formulario de solicitud antes del envío.", ancho=16.2)
    figura(doc, CAPTURAS / "37-solicitud-registrada.png",
           "Confirmación de la solicitud registrada con su código y fechas.", ancho=16.2)
    figura(doc, CAPTURAS / "38-mi-historial.png",
           "Historial del Colaborador limitado a sus propios préstamos.", ancho=16.2)
    figura(doc, CAPTURAS / "39-equipos-colaborador.png",
           "Inventario en modo consulta con la acción Solicitar para equipos disponibles.", ancho=16.2)
    figura(doc, CAPTURAS / "29-solicitud-detalle.png",
           "Detalle de la solicitud con motivo, revisión y vínculo con el préstamo.", ancho=16.2)

    doc.add_page_break()
    doc.add_heading("Anexo G. Pruebas de integridad", level=2)
    par(doc,
        "Las comprobaciones de integridad se ejecutaron directamente en PostgreSQL con transacciones que terminan "
        "en ROLLBACK. Cada caso intenta una operación inválida y verifica que la base la rechace; el conjunto no "
        "modifica los datos de demostración. El script se encuentra en docs/scripts/pruebas_integridad.py.")
    integridad = cargar_integridad()
    if integridad:
        tabla(
            doc,
            ["Código", "Escenario", "Restricción", "Resultado"],
            [
                (
                    item["codigo"],
                    item["escenario"],
                    item["restriccion"],
                    "Rechazado" if item["rechazado"] else "No rechazado",
                )
                for item in integridad
            ],
            [1.4, 7.4, 5.6, 2.4],
            "Comprobaciones de integridad ejecutadas en PostgreSQL.",
            fuente=7.2,
        )
    else:
        par(doc, "No se encontró docs/pruebas-integridad.json; ejecute docs/scripts/pruebas_integridad.py.")

    doc.add_page_break()
    doc.add_heading("Anexo H. Repositorio público", level=2)
    par(doc,
        "El código fuente, el README, los scripts de datos y pruebas, las capturas y el informe se publicaron en un "
        "repositorio público de GitHub. La portada muestra la estructura del proyecto, la rama principal y el README "
        "con las instrucciones de ejecución y las cuentas de demostración. El repositorio no requiere autenticación "
        "para su consulta; la rama main concentra la versión entregada.")
    figura(doc, CAPTURAS / "40-github-repositorio.png",
           "Repositorio público del proyecto TechAsset en GitHub.", ancho=16.2)
    tabla(
        doc,
        ["Elemento", "Valor"],
        [
            ("Repositorio", "https://github.com/CRAXCAT/TechAsset"),
            ("Visibilidad", "Público"),
            ("Rama principal", "main"),
            ("Contenido", "Backend, frontend, README, scripts, capturas, figuras e informe PDF/DOCX."),
            ("Verificación", "Más de 200 archivos · aproximadamente 49 MB al momento de la publicación."),
        ],
        [3.6, 13.0],
        "Datos del repositorio público.",
        fuente=7.8,
    )


# --------------------------------------------------------------------------
# Documento
# --------------------------------------------------------------------------
def main():
    doc = Document()
    estilos(doc)
    pagina(doc)
    decoracion(doc)

    portada(doc)
    indice(doc)
    resumen(doc)
    doc.add_page_break()
    seccion_1(doc)
    doc.add_page_break()
    seccion_2(doc)
    doc.add_page_break()
    seccion_3(doc)
    doc.add_page_break()
    seccion_4(doc)
    doc.add_page_break()
    seccion_5(doc)
    doc.add_page_break()
    seccion_6(doc)
    doc.add_page_break()
    seccion_7(doc)
    doc.add_page_break()
    seccion_8(doc)
    doc.add_page_break()
    seccion_9(doc)
    doc.add_page_break()
    referencias(doc)
    doc.add_page_break()
    anexos(doc)

    marcar_secciones(doc)
    doc.core_properties.title = "TechAsset: Sistema de Gestión de Inventario y Préstamo de Equipos Tecnológicos"
    doc.core_properties.author = "Kevin Ccente Garcia"
    doc.core_properties.subject = "Caso práctico integrador · Construcción de Software · UPLA 2026-II"
    doc.save(SALIDA)
    print(f"Documento generado: {SALIDA.name}")
    print(f"Figuras: {contador['figura']} · Tablas: {contador['tabla']}")


if __name__ == "__main__":
    main()
