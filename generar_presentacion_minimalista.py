"""
=============================================================================
GENERADOR DE PRESENTACIÓN MINIMALISTA - POLÍMEROS INDUSTRIALES
Maestría en Ciencias Aplicadas — Fundamentos de Ingeniería de Materiales
Alumno: I.Q.S. Miguel Alejandro Díaz Gaytán
Docente: Dr. Julio César Armas Pérez
=============================================================================
Diseño: Minimalista, limpio, sobrio (estilo humano universitario).
Contenido:
  1. Portada formal sobria.
  2. Los 10 polímeros más utilizados (Termoplásticos y Termofijos).
  3. Detalle de 6 Termoplásticos comunes y usos reales.
  4. Detalle de 4 Termofijos comunes y usos reales.
  5. Las 4 Estructuras Moleculares (Lineal, Ramificado, Entrecruzado, Red).
  6. Clasificación de los 10 polímeros según su arquitectura molecular.
  7. Relación estructura macromolecular vs. propiedades mecánicas.
  8. Procesos Industriales I: Extrusión y Moldeo por Inyección.
  9. Procesos Industriales II: Soplado, Termoformado y Rotomoldeo.
  10. Procesos Industriales III: Compresión y Transferencia (Termofijos).
  11. Métodos de Reciclaje I: Las 7 Tecnologías / Rutas Industriales.
  12. Métodos de Reciclaje II: Los 7 Códigos SPI/ASTM D7611 y Reto de Termofijos.
  13. Resumen y Criterios de Selección en Ingeniería.
Notas al pie en cada diapositiva con citas exactas de Callister, Askeland y Shackelford.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------------------
# PALETA MINIMALISTA Y SOBRIA (PROFESIONAL, SIN SOBREDISENO)
# ---------------------------------------------------------------------------
COLOR_BG = RGBColor(255, 255, 255)            # Fondo blanco puro
COLOR_TITLE = RGBColor(30, 41, 59)            # Slate 800 (títulos)
COLOR_SUBTITLE = RGBColor(71, 85, 105)        # Slate 600
COLOR_ACCENT = RGBColor(37, 99, 235)          # Azul sobrio (destacados discretos)
COLOR_TEXT = RGBColor(51, 65, 85)             # Slate 700 (texto principal)
COLOR_MUTED = RGBColor(100, 116, 139)         # Slate 500 (notas al pie y metadatos)
COLOR_BOX_BG = RGBColor(248, 250, 252)        # Slate 50 (fondo de tarjetas)
COLOR_BOX_BORDER = RGBColor(226, 232, 240)    # Slate 200 (borde sutil)
COLOR_TBL_HEADER = RGBColor(30, 41, 59)       # Fondo encabezado tabla
COLOR_TBL_ROW_ALT = RGBColor(248, 250, 252)   # Fila alterna
COLOR_LINE = RGBColor(203, 213, 225)          # Línea separadora

FONT_MAIN = "Calibri"
FONT_HEADING = "Calibri"


def aplicar_fondo_blanco(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()
    return bg


def agregar_encabezado(slide, num_slide, titulo, subtitulo, total_slides=13):
    # Número de diapositiva discreto arriba a la derecha
    num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.2), Inches(0.3))
    tf_num = num_box.text_frame
    tf_num.word_wrap = False
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{num_slide:02d} / {total_slides:02d}"
    p_num.font.name = FONT_MAIN
    p_num.font.size = Pt(10)
    p_num.font.color.rgb = COLOR_MUTED

    # Título principal
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.5), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = titulo
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TITLE

    # Subtítulo descriptivo
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.98), Inches(10.5), Inches(0.35))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitulo
    p_s.font.name = FONT_MAIN
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = COLOR_SUBTITLE

    # Línea divisoria minimalista
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_LINE
    line.line.fill.background()


def agregar_pie_pagina(slide, fuente_texto):
    """Línea separadora y nota al pie formal con la referencia académica exacta."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_LINE
    line.line.fill.background()

    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.38))
    tf_f = foot_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = f"Fuente bibliográfica: {fuente_texto}"
    p_f.font.name = FONT_MAIN
    p_f.font.size = Pt(9)
    p_f.font.italic = True
    p_f.font.color.rgb = COLOR_MUTED


def crear_caja_texto(slide, left, top, width, height, titulo, puntos, fondo_resaltado=False):
    """Crea una caja de contenido limpia con borde sutil y lista de viñetas."""
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(241, 245, 249) if fondo_resaltado else COLOR_BOX_BG
    box.line.color.rgb = COLOR_ACCENT if fondo_resaltado else COLOR_BOX_BORDER
    box.line.width = Pt(1.2 if fondo_resaltado else 0.8)

    pad = Inches(0.2)
    tb = slide.shapes.add_textbox(left + pad, top + pad, width - (pad * 2), height - (pad * 2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    if titulo:
        p_t = tf.paragraphs[0]
        p_t.text = titulo
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_ACCENT if fondo_resaltado else COLOR_TITLE
        p_t.space_after = Pt(6)

    for i, punto in enumerate(puntos):
        p = tf.add_paragraph() if (titulo or i > 0) else tf.paragraphs[0]
        p.text = f"•  {punto}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT
        p.space_after = Pt(4)


def formatear_celda_tabla(cell, texto, es_header=False, bold=False, align=PP_ALIGN.LEFT, font_size=Pt(9.5)):
    cell.text = ""
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.06)
    tf.margin_bottom = Inches(0.06)
    p = tf.paragraphs[0]
    p.text = texto
    p.alignment = align
    p.font.name = FONT_MAIN
    p.font.size = font_size
    p.font.bold = bold or es_header
    p.font.color.rgb = RGBColor(255, 255, 255) if es_header else COLOR_TEXT


def crear_presentacion_minimalista(output_filepath):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # DIAPOSITIVA 01: PORTADA SOBRIA Y ACADÉMICA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s1)

    # Marco superior institucional sobrio
    inst_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(0.5))
    tf_inst = inst_box.text_frame
    p_inst = tf_inst.paragraphs[0]
    p_inst.text = "UNIVERSIDAD DE GUANAJUATO  |  DIVISIÓN DE CIENCIAS NATURALES Y EXACTAS"
    p_inst.font.name = FONT_MAIN
    p_inst.font.size = Pt(11)
    p_inst.font.bold = True
    p_inst.font.color.rgb = COLOR_ACCENT

    # Título
    tit_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(11.0), Inches(1.4))
    tf_tit = tit_box.text_frame
    tf_tit.word_wrap = True
    p_tit = tf_tit.paragraphs[0]
    p_tit.text = "Polímeros Industriales: Clasificación Estructural,\nProcesamiento y Tecnologías de Reciclaje"
    p_tit.font.name = FONT_HEADING
    p_tit.font.size = Pt(28)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_TITLE

    # Subtítulo
    sub_box = s1.shapes.add_textbox(Inches(1.2), Inches(3.7), Inches(11.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Fundamentos de Ingeniería de Materiales — Maestría en Ciencias Aplicadas"
    p_sub.font.name = FONT_MAIN
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = COLOR_SUBTITLE

    # Línea sutil
    l_port = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.35), Inches(10.9), Inches(0.02))
    l_port.fill.solid()
    l_port.fill.fore_color.rgb = COLOR_LINE
    l_port.line.fill.background()

    # Datos Alumno y Docente
    dat_box = s1.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(11.0), Inches(1.5))
    tf_dat = dat_box.text_frame
    
    p_doc = tf_dat.paragraphs[0]
    p_doc.text = "Docente: Dr. Julio César Armas Pérez"
    p_doc.font.name = FONT_MAIN
    p_doc.font.size = Pt(12)
    p_doc.font.bold = True
    p_doc.font.color.rgb = COLOR_TITLE
    p_doc.space_after = Pt(4)

    p_alu = tf_dat.add_paragraph()
    p_alu.text = "Alumno: I.Q.S. Miguel Alejandro Díaz Gaytán"
    p_alu.font.name = FONT_MAIN
    p_alu.font.size = Pt(12)
    p_alu.font.color.rgb = COLOR_TEXT
    p_alu.space_after = Pt(4)

    p_fec = tf_dat.add_paragraph()
    p_fec.text = "Marco Teórico: Textos canónicos de Callister, Askeland, Shackelford y Normas ASTM D7611 / ISO 15270"
    p_fec.font.name = FONT_MAIN
    p_fec.font.size = Pt(10.5)
    p_fec.font.italic = True
    p_fec.font.color.rgb = COLOR_MUTED

    agregar_pie_pagina(s1, "Elaboración propia con base en el temario de posgrado FIM (UGTO, 2026).")

    # =========================================================================
    # DIAPOSITIVA 02: LOS 10 POLÍMEROS MÁS UTILIZADOS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s2)
    agregar_encabezado(s2, 2, "Los 10 Polímeros Más Utilizados en la Industria",
                       "División de los materiales plásticos predominantes entre Termoplásticos (Commodities) y Termofijos")

    # Tabla resumen de los 10 polímeros
    rows, cols = 11, 5
    tbl_shape = s2.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.0))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(0.6)
    tbl.columns[1].width = Inches(2.9)
    tbl.columns[2].width = Inches(1.2)
    tbl.columns[3].width = Inches(1.8)
    tbl.columns[4].width = Inches(5.233)

    headers = ["#", "Polímero Industrial", "Sigla", "Familia Térmica", "Aplicaciones Reales / Productos Típicos"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_TBL_HEADER
        formatear_celda_tabla(cell, h, es_header=True, align=PP_ALIGN.CENTER if j in [0, 2, 3] else PP_ALIGN.LEFT)

    datos_pols = [
        ("1", "Polietileno de Alta Densidad", "HDPE", "Termoplástico", "Tuberías de agua/gas, envases de leche/detergente, bidones químicos, tarimas."),
        ("2", "Polietileno de Baja Densidad", "LDPE", "Termoplástico", "Películas para empaque (film), bolsas plásticas, recubrimientos de cables, juguetes flexibles."),
        ("3", "Polipropileno", "PP", "Termoplástico", "Parachoques automotrices, bisagras vivas, tapas roscadas, jeringas, envases para microondas."),
        ("4", "Policloruro de Vinilo", "PVC", "Termoplástico", "Tuberías sanitarias, marcos de ventanas, losetas de piso, bolsas de sangre (PVC plastificado)."),
        ("5", "Tereftalato de Polietileno", "PET", "Termoplástico", "Botellas de bebidas carbonatadas, charolas termoformadas, fibra textil de poliéster."),
        ("6", "Poliestireno", "PS / EPS", "Termoplástico", "Vasos desechables, carcasas de electrodomésticos, aislamiento térmico (unicel expandido)."),
        ("7", "Resinas Epóxicas", "Epoxi", "Termofijo", "Adhesivos estructurales aeroespaciales, encapsulado de microchips, palas eólicas de composite."),
        ("8", "Fenol-Formaldehído (Baquelita)", "PF", "Termofijo", "Mangos de sartenes, disyuntores eléctricos, discos de corte abrasivo, aislantes térmicos."),
        ("9", "Poliuretanos Reticulados", "PU", "Termofijo", "Espumas rígidas para aislamiento de refrigeradores, espumas para asientos, elastómeros de amortiguación."),
        ("10", "Poliéster Insaturado", "UPR", "Termofijo", "Plásticos reforzados con fibra de vidrio (PRFV): cascos de botes, tinacos, paneles de carrocería."),
    ]

    for i, fila in enumerate(datos_pols):
        bg_col = COLOR_TBL_ROW_ALT if (i % 2 == 1) else COLOR_BG
        for j, val in enumerate(fila):
            c = tbl.cell(i + 1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = bg_col
            al = PP_ALIGN.CENTER if j in [0, 2, 3] else PP_ALIGN.LEFT
            b = True if j == 1 else False
            formatear_celda_tabla(c, val, bold=b, align=al, font_size=Pt(9))

    agregar_pie_pagina(s2, "Shackelford Sec. 13.12 (p. 472); Askeland Tablas 16-1, 16-3 y 16-10; Callister Sec. 4.14 y Tabla 4.2.")

    # =========================================================================
    # DIAPOSITIVA 03: DETALLE DE LOS 6 TERMOPLÁSTICOS MÁS USADOS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s3)
    agregar_encabezado(s3, 3, "Termoplásticos Predominantes: Características y Usos Reales",
                       "Polímeros que funden al calentarse y solidifican al enfriarse reversiblemente (enlaces secundarios débiles entre cadenas)")

    ancho_card = Inches(3.75)
    alto_card = Inches(2.45)
    
    # Fila 1: PET, HDPE, PVC
    crear_caja_texto(s3, Inches(0.8), Inches(1.6), ancho_card, alto_card,
                     "1. PET (Tereftalato de Polietileno)",
                     ["Alta transparencia y rigidez mecánica.",
                      "Excelente barrera contra difusión de CO2 y O2.",
                      "Usos: Botellas de refresco, empaques blister y fibra textil poliéster.",
                      "Reciclabilidad: Código SPI #1 (el más reciclado a nivel global)."])

    crear_caja_texto(s3, Inches(4.79), Inches(1.6), ancho_card, alto_card,
                     "2. HDPE (Polietileno Alta Densidad)",
                     ["Estructura altamente lineal, empaquetamiento denso.",
                      "Alta resistencia al impacto y agentes químicos.",
                      "Temperatura de fusión: ~130 - 135 °C.",
                      "Usos: Galones de leche, tuberías de drenaje corrugadas, bidones industriales."])

    crear_caja_texto(s3, Inches(8.78), Inches(1.6), ancho_card, alto_card,
                     "3. PVC (Policloruro de Vinilo)",
                     ["Contiene átomos de cloro (~57% en masa) que otorgan autoextinguibilidad.",
                      "Rígido (tubos hidráulicos y perfiles de ventana) o Flexible (con plastificantes).",
                      "Resistente a la intemperie y envejecimiento biológico.",
                      "Usos: Conducción sanitaria, aislamiento de conductores eléctricos."])

    # Fila 2: LDPE, PP, PS
    crear_caja_texto(s3, Inches(0.8), Inches(4.2), ancho_card, alto_card,
                     "4. LDPE (Polietileno Baja Densidad)",
                     ["Cadenas altamente ramificadas (ramales cortos y largos).",
                      "Menor densidad y menor cristalinidad que HDPE; máxima flexibilidad.",
                      "Excelente ductilidad y resistencia al desgarre.",
                      "Usos: Bolsas de plástico, geomembranas, películas retráctiles (stretch)."])

    crear_caja_texto(s3, Inches(4.79), Inches(4.2), ancho_card, alto_card,
                     "5. PP (Polipropileno)",
                     ["Termoplástico de menor densidad (~0.90 g/cm³).",
                      "Excepcional resistencia a la fatiga mecánica por flexión repetida.",
                      "Punto de fusión más elevado que el PE (~165 °C, esterilizable).",
                      "Usos: Bisagras integradas, parachoques de autos, recipientes Tupperware."])

    crear_caja_texto(s3, Inches(8.78), Inches(4.2), ancho_card, alto_card,
                     "6. PS (Poliestireno)",
                     ["Amorfo y transparente con grupo fenilo voluminoso que rigidiza la cadena.",
                      "Comportamiento frágil por debajo de su Tg (~100 °C).",
                      "Espumable con gas pentano para producir Unicel (EPS).",
                      "Usos: Cajas de CD, cubiertos desechables, aislamiento de hieleras."])

    agregar_pie_pagina(s3, "Callister Cap. 4 (p. 116-118); Askeland Sec. 16-4 (Tablas 16-2 y 16-3); Shackelford Sec. 13.12 (p. 472).")

    # =========================================================================
    # DIAPOSITIVA 04: DETALLE DE LOS 4 TERMOFIJOS MÁS USADOS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s4)
    agregar_encabezado(s4, 4, "Termofijos Predominantes: Características y Usos Reales",
                       "Polímeros con enlaces covalentes cruzados permanentes: infusibles e insolubles, se degradan antes de fundir")

    w_card = Inches(5.7)
    h_card = Inches(2.45)

    crear_caja_texto(s4, Inches(0.8), Inches(1.6), w_card, h_card,
                     "7. Resinas Epóxicas (Epoxi)",
                     ["Monómeros con anillos oxirano (epóxido) curados con poliaminas.",
                      "Prácticamente nula contracción volumétrica durante el curado químico.",
                      "Adhesión y resistencia mecánica excepcionales a tracción y fatiga.",
                      "Estabilidad térmica y resistencia a reactivos químicos agresivos.",
                      "Usos reales: Adhesivos estructurales en aviación, matrices para fibra de carbono en palas eólicas y encapsulado de componentes electrónicos."],
                     fondo_resaltado=False)

    crear_caja_texto(s4, Inches(6.833), Inches(1.6), w_card, h_card,
                     "8. Fenol-Formaldehído (Baquelita)",
                     ["Primer polímero sintético comercial (Leo Baekeland, 1907).",
                      "Reacción de condensación con altísima densidad de entrecruzamiento de red.",
                      "Rigidez sobresaliente, gran dureza superficial y estabilidad dimensional.",
                      "Incombustible y excelente aislante eléctrico y térmico.",
                      "Usos reales: Mangos para ollas y sartenes, disyuntores eléctricos, discos de corte abrasivo aglomerados y tableros de circuitos impresos."],
                     fondo_resaltado=False)

    crear_caja_texto(s4, Inches(0.8), Inches(4.2), w_card, h_card,
                     "9. Poliuretanos Reticulados (PU Termofijo)",
                     ["Reacción de poliadición exotérmica entre polioles y diisocianatos.",
                      "Formulación ajustable: desde espumas microcelulares hasta sólidos rígidos.",
                      "Espumas rígidas: Celda cerrada con conductividad térmica ultra baja (k ≈ 0.022 W/m·K).",
                      "Elastómeros de PU: Resistencia superior a la abrasión y absorción de impacto.",
                      "Usos reales: Aislamiento térmico de refrigeradores domésticos, calzado de seguridad, piezas de amortiguación en suspensión automotriz."],
                     fondo_resaltado=False)

    crear_caja_texto(s4, Inches(6.833), Inches(4.2), w_card, h_card,
                     "10. Resinas de Poliéster Insaturado (UPR)",
                     ["Oligómero lineal con dobles enlaces reactivos disuelto en monómero de estireno.",
                      "El estireno actúa como agente de entrecruzamiento radicalario a temperatura ambiente.",
                      "Excelente balance costo-desempeño en conformado de piezas grandes.",
                      "Usos reales: Matriz polimérica en PRFV (Plástico Reforzado con Fibra de Vidrio) para cascos de embarcaciones, tanques cisterna y paneles de carrocería."],
                     fondo_resaltado=False)

    agregar_pie_pagina(s4, "Askeland Sec. 16-9 y 16-10 (Tablas 16-10 y 16-11, p. 592-595); Callister Sec. 4.7 y 14.13; Shackelford Sec. 13.8.")

    # =========================================================================
    # DIAPOSITIVA 05: LAS 4 ESTRUCTURAS MACROMOLECULARES FUNDAMENTALES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s5)
    agregar_encabezado(s5, 5, "Arquitectura Macromolecular: Las 4 Formas Estructurales",
                       "La disposición geométrica de las cadenas define el comportamiento mecánico, térmico y de solubilidad")

    w_4 = Inches(2.78)
    h_4 = Inches(5.0)

    crear_caja_texto(s5, Inches(0.8), Inches(1.6), w_4, h_4,
                     "1. Estructura Lineal",
                     ["Descripción:",
                      "Cadenas largas y continuas unidas únicamente por enlaces sencillos de extremo a extremo (como hebras de espagueti).",
                      "",
                      "Unión Intercadena:",
                      "Fuerzas secundarias débiles (Van der Waals o puentes de hidrógeno).",
                      "",
                      "Rasgos Clave:",
                      "• Gran facilidad de empaquetamiento molecular.",
                      "• Alta propensión a formar regiones cristalinas densas.",
                      "• Funden reversiblemente y se disuelven en solventes afines.",
                      "",
                      "Ejemplos:",
                      "HDPE, PVC, PET, Nylon 6,6."])

    crear_caja_texto(s5, Inches(3.78), Inches(1.6), w_4, h_4,
                     "2. Estructura Ramificada",
                     ["Descripción:",
                      "Cadenas principales de las cuales nacen ramificaciones laterales (cortas o largas) durante la síntesis.",
                      "",
                      "Unión Intercadena:",
                      "Fuerzas de Van der Waals entre cadenas separadas por ramas.",
                      "",
                      "Rasgos Clave:",
                      "• Las ramas actúan como impedimento estérico espacial.",
                      "• Dificultan el empaquetamiento regular de las cadenas.",
                      "• Menor densidad y menor punto de fusión que el lineal.",
                      "• Mayor flexibilidad y ductilidad.",
                      "",
                      "Ejemplos:",
                      "LDPE (ramificaciones largas y cortas), LLDPE."])

    crear_caja_texto(s5, Inches(6.78), Inches(1.6), w_4, h_4,
                     "3. Estructura Entrecruzada",
                     ["Descripción:",
                      "Cadenas lineales adyacentes unidas transversalmente en puntos específicos mediante enlaces covalentes.",
                      "",
                      "Unión Intercadena:",
                      "Enlaces químicos primarios transversales (ej. puentes de azufre -S-S-).",
                      "",
                      "Rasgos Clave:",
                      "• Las cadenas no pueden deslizar libremente una sobre otra.",
                      "• Deformación elástica reversible masiva (>200% a 800%).",
                      "• No funde; mantiene memoria de forma elástica.",
                      "",
                      "Ejemplos:",
                      "Caucho natural vulcanizado, elastómeros de polibutadieno."])

    crear_caja_texto(s5, Inches(9.78), Inches(1.6), w_4, h_4,
                     "4. Estructura de Red 3D",
                     ["Descripción:",
                      "Monómeros trifuncionales o polifuncionales que crecen formando una malla tridimensional continua.",
                      "",
                      "Unión Intercadena:",
                      "Toda la pieza macroscópica conforma una única macromolécula gigante.",
                      "",
                      "Rasgos Clave:",
                      "• Infusibles: se termodegradan sin pasar por estado líquido.",
                      "• Insolubles: sólo experimentan hinchamiento elástico.",
                      "• Máxima rigidez, dureza y estabilidad térmica dimensional.",
                      "",
                      "Ejemplos:",
                      "Resinas epoxi, Baquelita, Poliuretanos rígidos, UPR curado."])

    agregar_pie_pagina(s5, "Callister Sec. 4.7 (Figura 4.7, p. 111-112); Askeland Sec. 16-1 (Figura 16-1, p. 586); Shackelford Sec. 13.1 y 13.8.")

    # =========================================================================
    # DIAPOSITIVA 06: CLASIFICACIÓN DE LOS 10 POLÍMEROS POR ARQUITECTURA
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s6)
    agregar_encabezado(s6, 6, "Clasificación de los 10 Polímeros Según su Arquitectura Molecular",
                       "Asignación inequívoca de cada polímero industrial a su modelo estructural correspondiente")

    # Tabla directa de 10 polímeros vs arquitectura
    rows, cols = 11, 4
    tbl_s6 = s6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.0))
    t6 = tbl_s6.table
    t6.columns[0].width = Inches(2.8)
    t6.columns[1].width = Inches(2.2)
    t6.columns[2].width = Inches(2.0)
    t6.columns[3].width = Inches(4.733)

    hdrs6 = ["Polímero Industrial", "Arquitectura Molecular", "Comportamiento Térmico", "Razón Estructural / Mecanismo de Unión"]
    for j, h in enumerate(hdrs6):
        c = t6.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_TBL_HEADER
        formatear_celda_tabla(c, h, es_header=True, align=PP_ALIGN.CENTER if j in [1, 2] else PP_ALIGN.LEFT)

    data_s6 = [
        ("HDPE (Polietileno Alta Densidad)", "Lineal", "Termoplástico", "Cadenas rectas continuas; fácil cristalización por empaquetamiento."),
        ("PET (Tereftalato de Polietileno)", "Lineal", "Termoplástico", "Copolímero lineal por condensación; anillos fenilo aportan rigidez a la cadena."),
        ("PVC (Policloruro de Vinilo)", "Lineal", "Termoplástico", "Cadena vinílica lineal; interacción dipolar moderada por enlaces C-Cl."),
        ("PP (Polipropileno)", "Lineal (con grupos metilo)", "Termoplástico", "Cadena lineal principal; tacticidad isotáctica permite cristalización rápida."),
        ("PS (Poliestireno)", "Lineal (con anillos fenilo)", "Termoplástico", "Cadena lineal atáctica; volumen del fenilo bloquea empaquetamiento (amorfo)."),
        ("LDPE (Polietileno Baja Densidad)", "Ramificada", "Termoplástico", "Ramificaciones largas inducidas por alta presión impiden empaquetamiento."),
        ("Caucho Vulcanizado / Elastómeros", "Entrecruzada (Crosslinked)", "Elastómero Termofijo", "Puentes de azufre covalentes (-S-S-) unen cadenas lineales adyacentes."),
        ("Resinas Epóxicas", "De Red Tridimensional", "Termofijo", "Anillos oxirano reaccionan con aminas formando una malla 3D covalente."),
        ("Fenol-Formaldehído (Baquelita)", "De Red Tridimensional", "Termofijo", "Formaldehído actúa como puente trifuncional entre anillos fenólicos."),
        ("Poliuretano Rígido / Poliéster Insat.", "De Red Tridimensional", "Termofijo", "Entrecruzamiento continuo con monómeros multifuncionales en bloque."),
    ]

    for i, fila in enumerate(data_s6):
        bg_col = COLOR_TBL_ROW_ALT if (i % 2 == 1) else COLOR_BG
        for j, val in enumerate(fila):
            c = t6.cell(i + 1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = bg_col
            al = PP_ALIGN.CENTER if j in [1, 2] else PP_ALIGN.LEFT
            b = True if j in [0, 1] else False
            formatear_celda_tabla(c, val, bold=b, align=al, font_size=Pt(9.2))

    agregar_pie_pagina(s6, "Callister Sec. 4.7; Askeland Sec. 16-1 y 16-5; Shackelford Sec. 13.1 y 13.8.")

    # =========================================================================
    # DIAPOSITIVA 07: RELACIÓN ESTRUCTURA MOLECULAR - PROPIEDADES MECÁNICAS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s7)
    agregar_encabezado(s7, 7, "Relación Estructura Molecular — Propiedades Mecánicas",
                       "Cómo la arquitectura de las cadenas gobierna el módulo, la resistencia, la deformación y la fluencia")

    w_box7 = Inches(5.7)
    h_box7 = Inches(2.45)

    crear_caja_texto(s7, Inches(0.8), Inches(1.6), w_box7, h_box7,
                     "Lineal vs. Ramificado: Empaquetamiento y Cristalinidad",
                     ["Cadenas Lineales (ej. HDPE vs. LDPE):",
                      "• Las cadenas lineales se empaquetan sin estorbos, alcanzando hasta 70-80% de cristalinidad.",
                      "• Resultado mecánico: Mayor densidad, mayor módulo elástico (E ≈ 1.1 GPa), mayor límite elástico y resistencia a tracción.",
                      "Cadenas Ramificadas (ej. LDPE):",
                      "• Los ramales separan las cadenas, incrementando el volumen libre y bajando la cristalinidad al 40-50%.",
                      "• Resultado mecánico: Menor rigidez (E ≈ 0.2 GPa), menor límite elástico, pero elongación al quiebre muy superior (>500%)."])

    crear_caja_texto(s7, Inches(6.833), Inches(1.6), w_box7, h_box7,
                     "Fuerzas Intercadena vs. Deslizamiento Mecánico",
                     ["En polímeros Lineales y Ramificados:",
                      "• Las moléculas se mantienen unidas sólo por enlaces secundarios débiles (Van der Waals o puentes de H).",
                      "• Bajo esfuerzo mecánico sostenido, las cadenas pueden deslizarse irreversiblemente unas sobre otras (fenómeno de fluencia o creep).",
                      "• Al aplicar calor superando Tg y Tm, la agitación térmica supera a las fuerzas secundarias: el material funde y fluye.",
                      "• Justifica por qué se procesan fácilmente por extrusión e inyección."])

    crear_caja_texto(s7, Inches(0.8), Inches(4.2), w_box7, h_box7,
                     "Redes Tridimensionales: Rigidez Extrema y Fragilidad",
                     ["En polímeros de Red (Epoxis, Baquelita, Poliéster Insaturado):",
                      "• Los enlaces covalentes C-C y C-N unen toda la estructura en una red rígida continua.",
                      "• El deslizamiento molecular está totalmente impedido por la alta densidad de entrecruzamiento.",
                      "• Comportamiento mecánico: Módulo elástico muy elevado (E > 3 - 5 GPa), gran dureza superficial y nula fluencia bajo carga moderada.",
                      "• Consecuencia: No admiten deformación plástica significativa; exhiben fractura frágil sin cuello previo."])

    crear_caja_texto(s7, Inches(6.833), Inches(4.2), w_box7, h_box7,
                     "Estructuras Entrecruzadas: Elasticidad Reversible",
                     ["En Elastómeros Entrecruzados (Cauchos con vulcanización):",
                      "• Pocos enlaces cruzados distribuidos uniformemente entre cadenas ovilladas.",
                      "• Al aplicar esfuerzo de tracción, las cadenas se desenrollan fácilmente (bajo módulo inicial con deformaciones elásticas gigantescas de 200% a 800%).",
                      "• Al liberar el esfuerzo, la entropía conformacional y los puentes covalentes regresan las cadenas a su estado original.",
                      "• Los enlaces cruzados evitan el flujo viscoso permanente."])

    agregar_pie_pagina(s7, "Callister Cap. 4 (p. 116) y Cap. 8 (p. 250); Askeland Sec. 16-1 y 16-6 (Figuras 16-11 y 16-23); Shackelford Sec. 13.7.")

    # =========================================================================
    # DIAPOSITIVA 08: PROCESOS INDUSTRIALES I - EXTRUSIÓN E INYECCIÓN
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s8)
    agregar_encabezado(s8, 8, "Procesos Industriales de Transformación (I)",
                       "Las dos tecnologías continuas y cíclicas más utilizadas a nivel global para termoplásticos")

    w_proc = Inches(5.7)
    h_proc = Inches(5.0)

    crear_caja_texto(s8, Inches(0.8), Inches(1.6), w_proc, h_proc,
                     "1. Proceso de Extrusión (Proceso Continuo)",
                     ["Principio de Operación:",
                      "• Los pellets sólidos se alimentan por una tolva a un cilindro calefaccionado.",
                      "• Un tornillo helicoidal (husillo) hace avanzar el material a través de 3 zonas: alimentación (compactación), compresión (plastificación por fricción y calor) y dosificación.",
                      "• El polímero fundido y homogeneizado es forzado a presión a través de una matriz o dado abierto de sección geométrica constante.",
                      "• Al salir, el perfil se enfría inmediatamente mediante una tina de agua o aire forzado para solidificar su forma.",
                      "",
                      "Productos Fabricados Típicamente:",
                      "• Tuberías de conducción de agua, gas y drenaje (HDPE, PVC).",
                      "• Películas continuas para bolsas y empaque (extrusión de película soplada de LDPE).",
                      "• Perfiles de ventanas arquitectónicas, marcos y molduras.",
                      "• Filamentos para impresión 3D y recubrimiento aislante de cables eléctricos.",
                      "",
                      "Ventaja Técnica:",
                      "Máxima eficiencia económica para la producción en serie de longitudes continuas."])

    crear_caja_texto(s8, Inches(6.833), Inches(1.6), w_proc, h_proc,
                     "2. Moldeo por Inyección (Proceso Cíclico de Precisión)",
                     ["Principio de Operación:",
                      "• Análogo al die casting en metales. Es el proceso reina para piezas discretas complejas.",
                      "• El polímero se plastifica en un cilindro con tornillo recíproco o pistón hidráulico.",
                      "• El husillo actúa como pistón inyector, empujando a alta presión (>1000 bar) una dosis exacta de fundido a través de una boquilla hacia un molde cerrado.",
                      "• El molde metálico (acero o aluminio) se mantiene refrigerado por canales de agua para acelerar la solidificación de la pieza.",
                      "• El molde se abre mecánicamente y unos pines expulsores expulsan la pieza terminada.",
                      "",
                      "Productos Fabricados Típicamente:",
                      "• Carcasas de electrodomésticos, monitores y computadoras (PS, ABS).",
                      "• Componentes automotrices: tableros, parachoques y manijas (PP).",
                      "• Tapas roscadas para bebidas, contenedores médicos y jeringas descartables.",
                      "",
                      "Ventaja Técnica:",
                      "Tolerancias dimensionales milimétricas, excelente acabado superficial y ciclos rápidos (segundos)."])

    agregar_pie_pagina(s8, "Callister Sec. 14.13 (Figuras 14.30 y 14.31, p. 608-610); Askeland Sec. 16-11 (Figuras 16-25a/c y 16-26, p. 596-597).")

    # =========================================================================
    # DIAPOSITIVA 09: PROCESOS INDUSTRIALES II - SOPLADO, TERMOFORMADO, ROTOMOLDEO
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s9)
    agregar_encabezado(s9, 9, "Procesos Industriales de Transformación (II)",
                       "Técnicas avanzadas para recipientes huecos, piezas laminares y cuerpos volumétricos sin esfuerzos")

    w_3 = Inches(3.75)
    h_3 = Inches(5.0)

    crear_caja_texto(s9, Inches(0.8), Inches(1.6), w_3, h_3,
                     "3. Moldeo por Soplado (Blow Molding)",
                     ["Mecanismo:",
                      "1. Se extruye o inyecta un tubo caliente hueco denominado preforma o parisón.",
                      "2. Un molde bipartito se cierra alrededor del parisón atrapando sus extremos.",
                      "3. Se inyecta aire comprimido al interior, expandiendo el tubo como un globo contra las paredes de la cavidad fría.",
                      "4. Enfría rápidamente y expulsa el envase.",
                      "",
                      "Variantes:",
                      "• Extrusión-Soplado: Envases de leche, galones de detergente (HDPE).",
                      "• Inyección-Estirado-Soplado (ISBM): Botellas de PET orientadas bi-axialmente.",
                      "",
                      "Aplicaciones:",
                      "Botellas de refresco, bidones químicos, tanques de combustible de autos."])

    crear_caja_texto(s9, Inches(4.79), Inches(1.6), w_3, h_3,
                     "4. Termoformado (Thermoforming)",
                     ["Mecanismo:",
                      "1. Se parte de una lámina o film termoplástico previamente extruido.",
                      "2. Se calienta la lámina mediante radiadores infrarrojos hasta su estado gomoso (por encima de Tg).",
                      "3. La lámina ablandada se coloca sobre un molde y se succiona con vacío o se presiona con aire contra la matriz.",
                      "4. Se enfría en contacto con el molde y se recortan los sobrantes.",
                      "",
                      "Ventajas:",
                      "Costes de utillaje de moldes muy inferiores a la inyección.",
                      "",
                      "Aplicaciones:",
                      "Vasos y platos desechables (PS, PP), charolas para carne, blisters farmacéuticos, paneles interiores de refrigeradores."])

    crear_caja_texto(s9, Inches(8.78), Inches(1.6), w_3, h_3,
                     "5. Rotomoldeo (Moldeo Rotacional)",
                     ["Mecanismo:",
                      "1. Se introduce una carga de polímero en polvo fino en un molde hueco.",
                      "2. El molde se calienta dentro de un horno mientras gira simultáneamente sobre dos ejes perpendiculares a baja velocidad.",
                      "3. La fuerza centrífuga y la gravedad hacen que el plástico fundido recubra homogéneamente las paredes internas del molde.",
                      "4. Se enfría con aire/agua y se desmolda.",
                      "",
                      "Ventajas Únicas:",
                      "Piezas huecas gigantes sin costuras ni líneas de unión, espesor uniforme y libres de esfuerzos residuales.",
                      "",
                      "Aplicaciones:",
                      "Tinacos de agua (Rotoplas en HDPE), kayaks, juegos infantiles, grandes contenedores industriales."])

    agregar_pie_pagina(s9, "Askeland Sec. 16-11 (Figuras 16-25b/d y 16-27, p. 596-598); Callister Sec. 14.13 (p. 610).")

    # =========================================================================
    # DIAPOSITIVA 10: PROCESOS INDUSTRIALES III - TERMOFIJOS (COMPRESIÓN Y TRANSFERENCIA)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s10)
    agregar_encabezado(s10, 10, "Procesos Industriales de Transformación (III): Termofijos",
                       "Procesos donde la conformación geométrica y la reacción química de reticulación (curado) ocurren simultáneamente")

    crear_caja_texto(s10, Inches(0.8), Inches(1.6), w_proc, h_proc,
                     "6. Moldeo por Compresión (Estándar en Termofijos)",
                     ["Mecanismo de Fabricación:",
                      "• Una cantidad pesada de resina en polvo, gránulos o preforma compactada se coloca en la cavidad abierta de un molde inferior calentado.",
                      "• Se cierra el molde superior aplicando una elevada fuerza hidráulica.",
                      "• El calor del molde licúa temporalmente la resina mientras la presión la obliga a llenar todos los detalles de la cavidad.",
                      "• Se mantiene la temperatura y presión durante un tiempo determinado (tiempo de curado), durante el cual ocurre la reacción química exotérmica que forma los enlaces covalentes cruzados de la red 3D.",
                      "• Una vez finalizada la reticulación, la pieza es rígida e infusible.",
                      "",
                      "Diferencia Clave con Termoplásticos:",
                      "¡La pieza termofija se extrae del molde CALIENTE! No requiere enfriamiento en el molde porque ya no puede fundir y es dimensionalmente estable.",
                      "",
                      "Productos Fabricados:",
                      "Mangos aislantes para sartenes y planchas (Baquelita), carcasas de enchufes y disyuntores, discos abrasivos aglomerados."])

    crear_caja_texto(s10, Inches(6.833), Inches(1.6), w_proc, h_proc,
                     "7. Moldeo por Transferencia (Evolución de la Compresión)",
                     ["Mecanismo de Fabricación:",
                      "• Es una variante refinada del moldeo por compresión diseñada para piezas complejas o con insertos metálicos delicados.",
                      "• La resina sólida se precalienta en una cámara de transferencia separada de la cavidad principal.",
                      "• Un pistón hidráulico presiona el material fluidificado, haciéndolo fluir a través de canales de colada hacia las cavidades del molde caliente cerrado.",
                      "• La reticulación química finaliza dentro de la cavidad a temperatura de curado.",
                      "",
                      "Ventajas frente a la Compresión Directa:",
                      "• Distribución de presión mucho más homogénea en geometrías intrincadas.",
                      "• No desplaza pernos ni contactos metálicos embebidos en el molde.",
                      "• Menor formación de rebabas y acabados más limpios.",
                      "",
                      "Productos Fabricados:",
                      "Encapsulado de circuitos integrados y transistores, conectores multipin aeronáuticos, componentes de conmutación eléctrica."])

    agregar_pie_pagina(s10, "Callister Sec. 14.13 (Figura 14.29, p. 608-609); Askeland Sec. 16-11 (Figura 16-28, p. 598-599); Shackelford Sec. 13.8.")

    # =========================================================================
    # DIAPOSITIVA 11: MÉTODOS DE RECICLAJE I - LAS 7 TECNOLOGÍAS INDUSTRIALES
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s11)
    agregar_encabezado(s11, 11, "Clasificación del Reciclaje (I): Las 7 Rutas Tecnológicas",
                       "Jerarquía industrial de valorización y circularidad de polímeros (Normas ISO 15270 / ASTM D5033)")

    # 7 métodos en lista estructurada
    w_col11 = Inches(5.7)
    h_col11 = Inches(5.0)

    crear_caja_texto(s11, Inches(0.8), Inches(1.6), w_col11, h_col11,
                     "Rutas Mecánicas y de Circuito Cerrado",
                     ["1. Reciclaje Primario (Re-extrusión / Circuito Cerrado):",
                      "• Reprocesamiento mecánico inmediato de recortes, rebabas y mermas limpias dentro de la misma planta industrial.",
                      "• Se mezcla con resina virgen sin alterar las propiedades mecánicas finales del producto.",
                      "",
                      "2. Reciclaje Secundario (Mecánico Post-Consumo):",
                      "• Tratamiento de residuos plásticos provenientes de la recolección municipal o comercial.",
                      "• Etapas: Separación óptica/flotación ➔ Trituración en hojuelas (flakes) ➔ Lavado exhaustivo de contaminantes ➔ Secado ➔ Extrusión y peletizado.",
                      "• Limitación: Degeneración progresiva por cizalladura térmica (downcycling).",
                      "",
                      "3. Reciclaje por Disolución / Precipitación Selectiva:",
                      "• Separación física selectiva mediante solventes (ej. proceso CreaSolv).",
                      "• Disuelve selectivamente el polímero objetivo de empaques multicapa separándolo de aditivos, cargas y aluminio sin romper los enlaces covalentes."])

    crear_caja_texto(s11, Inches(6.833), Inches(1.6), w_col11, h_col11,
                     "Rutas Químicas, Térmicas y Biológicas",
                     ["4. Reciclaje Terciario Químico (Solvólisis / Despolimerización):",
                      "• Ruptura de enlaces químicos para regresar a monómeros u oligómeros originales con calidad de resina virgen (Food-Grade).",
                      "• Procesos: Glicólisis, metanólisis e hidrólisis (ampliamente usados en PET y poliamidas/nylons).",
                      "",
                      "5. Reciclaje Terciario Térmico (Pirólisis y Gasificación):",
                      "• Descomposición termo-catalítica a alta temperatura (>450 °C) en ausencia de oxígeno.",
                      "• Convierte mezclas difíciles de poliolefinas (PE/PP) en crudo sintético (aceite de pirólisis) o syngas para reintegrarse a la refinería.",
                      "",
                      "6. Reciclaje Cuaternario (Valorización Energética):",
                      "• Incineración controlada con recuperación de calor (Waste-to-Energy).",
                      "• Aprovecha el alto poder calorífico de los plásticos (~40 MJ/kg, similar al combustible diésel) para generar vapor o como combustible en hornos cementeros.",
                      "",
                      "7. Reciclaje Orgánico / Biológico (Compostaje Industrial):",
                      "• Biodegradación por microorganismos para biopolímeros certificados (PLA, PHA, almidón) transformándose en agua, CO2 y abono orgánico."])

    agregar_pie_pagina(s11, "Normas ISO 15270 (Reciclado y Recuperación de Plásticos); ASTM D5033; Hopewell et al., Phil. Trans. R. Soc. B (2009).")

    # =========================================================================
    # DIAPOSITIVA 12: MÉTODOS DE RECICLAJE II - CÓDIGOS SPI Y RETO DE TERMOFIJOS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s12)
    agregar_encabezado(s12, 12, "Clasificación del Reciclaje (II): Códigos SPI y el Reto de Termofijos",
                       "Sistema de codificación numérica universal de resinas (ASTM D7611) y estrategias de fin de ciclo para polímeros de red")

    # Tabla de los 7 Códigos SPI
    rows, cols = 8, 4
    tbl_s12 = s12.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.0))
    t12 = tbl_s12.table
    t12.columns[0].width = Inches(0.8)
    t12.columns[1].width = Inches(1.8)
    t12.columns[2].width = Inches(2.2)
    t12.columns[3].width = Inches(2.7)

    hdrs12 = ["Código", "Resina", "Reciclabilidad Mecánica", "Destino del Material Reciclado"]
    for j, h in enumerate(hdrs12):
        c = t12.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_TBL_HEADER
        formatear_celda_tabla(c, h, es_header=True, align=PP_ALIGN.CENTER if j in [0, 2] else PP_ALIGN.LEFT)

    data_s12 = [
        ("1", "PET", "Muy Alta", "Nuevas botellas (rPET), fibra textil polar, flejes."),
        ("2", "HDPE", "Alta", "Tuberías corrugadas, botes de basura, tarimas plásticas."),
        ("3", "PVC", "Baja / Compleja", "Separación difícil por cloro; conos viales, suelas."),
        ("4", "LDPE", "Media - Alta", "Bolsas de basura, mangueras de riego, madera plástica."),
        ("5", "PP", "Alta", "Cajas de batería, cepillos, cubetas, autopartes."),
        ("6", "PS", "Baja", "Baja densidad en EPS encarece flete; molduras, aislamiento."),
        ("7", "OTROS", "Muy Baja (Mezclas)", "Generalmente no reciclable mecánicamente; valorización energética o pirólisis."),
    ]

    for i, fila in enumerate(data_s12):
        bg_col = COLOR_TBL_ROW_ALT if (i % 2 == 1) else COLOR_BG
        for j, val in enumerate(fila):
            c = t12.cell(i + 1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = bg_col
            al = PP_ALIGN.CENTER if j in [0, 2] else PP_ALIGN.LEFT
            b = True if j in [0, 1] else False
            formatear_celda_tabla(c, val, bold=b, align=al, font_size=Pt(9))

    # Caja explicativa al lado derecho sobre el reto de los termofijos
    crear_caja_texto(s12, Inches(8.5), Inches(1.6), Inches(4.033), Inches(5.0),
                     "¿Por qué los Termofijos son Difíciles de Reciclar?",
                     ["El Origen Estructural del Problema:",
                      "• Los termoplásticos se reciclan mecánicamente simplemente aplicando calor para fundirlos y remoldearlos.",
                      "• En los polímeros Termofijos y de Red, los enlaces covalentes cruzados son permanentes: NO funden. Si se calientan, sufren pirólisis o combustión antes de licuarse.",
                      "",
                      "Estrategias Actuales para Termofijos:",
                      "1. Molienda Mecánica como Carga (Filler):",
                      "Se trituran en polvo ultrafino y se emplean como material de relleno inerte en asfalto, concreto o nuevas resinas vírgenes.",
                      "2. Quimiólisis / Solvólisis Avanzada:",
                      "Ataque con solventes a temperatura y catalizadores para romper selectivamente ciertos enlaces (ej. despolimerización de resinas epoxi para recuperar fibra de carbono virgen).",
                      "3. Desvulcanización en Cauchos:",
                      "Ruptura selectiva de enlaces S-S sin cortar la cadena principal de carbono.",
                      "4. Valorización Energética:",
                      "Aprovechamiento de su poder calorífico en incineración industrial."],
                     fondo_resaltado=True)

    agregar_pie_pagina(s12, "ASTM D7611 / SPI Resin Identification System; Callister Sec. 14.13; Askeland Sec. 16-1 y 16-9.")

    # =========================================================================
    # DIAPOSITIVA 13: RESUMEN Y CRITERIOS DE SELECCIÓN EN INGENIERÍA
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    aplicar_fondo_blanco(s13)
    agregar_encabezado(s13, 13, "Resumen y Criterios de Selección en Ingeniería de Materiales",
                       "Guía sinóptica para defender decisiones de diseño, procesamiento y fin de vida ante el comité evaluador")

    w_res = Inches(3.75)
    h_res = Inches(5.0)

    crear_caja_texto(s13, Inches(0.8), Inches(1.6), w_res, h_res,
                     "1. Selección Estructural",
                     ["Criterio de Carga y Rigidez:",
                      "• Si la pieza requiere alta rigidez, estabilidad dimensional y resistencia a fluencia a >100 °C: Seleccionar polímeros de Red (Epoxis, Baquelita).",
                      "• Si la pieza requiere ductilidad, tenacidad al impacto y bajo costo: Seleccionar termoplásticos lineales o ramificados (HDPE, PP, LDPE).",
                      "",
                      "Densidad y Empaquetamiento:",
                      "La presencia de ramificaciones (LDPE) o anillos aromáticos voluminosos (PS) reduce la cristalinidad e incrementa la transparencia óptica."])

    crear_caja_texto(s13, Inches(4.79), Inches(1.6), w_res, h_res,
                     "2. Selección del Proceso",
                     ["Geometría vs. Eficiencia:",
                      "• Perfiles continuos o tuberías ➔ Extrusión monohusillo o doble husillo.",
                      "• Piezas de precisión geométrica y alta serie ➔ Moldeo por Inyección.",
                      "• Cuerpos huecos (botellas, galones) ➔ Moldeo por Soplado.",
                      "• Piezas de lámina delgada y bajo utillaje ➔ Termoformado.",
                      "• Cuerpos huecos masivos sin esfuerzos ➔ Rotomoldeo.",
                      "• Piezas termoestables con insertos ➔ Compresión o Transferencia."])

    crear_caja_texto(s13, Inches(8.78), Inches(1.6), w_res, h_res,
                     "3. Enfoque de Sostenibilidad",
                     ["Estrategia de Reciclabilidad:",
                      "• Priorizar monomateriales termoplásticos de fácil reciclaje mecánico (PET #1, HDPE #2, PP #5).",
                      "• Evitar empaques multicapa no compatibles a menos que se justifique por barrera química.",
                      "• En componentes termoestables (composites epoxi/fibra), contemplar desde el diseño rutas de desmantelamiento y reciclaje químico selectivo.",
                      "",
                      "Conclusión:",
                      "La microestructura macromolecular dicta todas las opciones de procesamiento y fin de ciclo."])

    agregar_pie_pagina(s13, "Integración de conceptos de Callister (Caps. 4 y 14), Askeland (Cap. 16), Shackelford (Cap. 13) e ISO 15270.")

    # Guardar presentación
    prs.save(output_filepath)
    print(f"[OK] Presentación minimalista generada con éxito en: {output_filepath}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "presentacion_polimeros_procesos_reciclaje.pptx")
    crear_presentacion_minimalista(output_path)
