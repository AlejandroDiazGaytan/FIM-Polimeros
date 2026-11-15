"""
=============================================================================
GENERADOR DE PRESENTACIÓN ARTESANAL Y RIGUROSA - CIENCIA DE POLÍMEROS
Maestría en Ciencias Aplicadas — Fundamentos de Ingeniería de Materiales
Docente: Dr. Julio César Armas Pérez
Alumno: Miguel Alejandro Díaz Gaytán
=============================================================================
"""

import os
import re
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# PALETA DE COLOR
# ---------------------------------------------------------------------------
COLOR_PRIMARY_NAVY = RGBColor(30, 41, 59)     # Slate 800
COLOR_BURGUNDY = RGBColor(153, 27, 27)        # Red 800
COLOR_COBALT = RGBColor(29, 78, 216)          # Blue 700
COLOR_CARD_BG = RGBColor(248, 250, 252)       # Slate 50
COLOR_CARD_BORDER = RGBColor(203, 213, 225)   # Slate 300
COLOR_CARD_ACCENT_BG = RGBColor(240, 249, 255) # Sky 50
COLOR_CARD_ACCENT_BORDER = RGBColor(147, 197, 253) # Sky 300
COLOR_EQ_BOX_BG = RGBColor(255, 255, 255)     # Blanco puro
COLOR_EQ_BOX_BORDER = RGBColor(186, 230, 253) # Borde suave azul
COLOR_NOTE_BG = RGBColor(241, 245, 249)       # Slate 100
COLOR_NOTE_BORDER = RGBColor(226, 232, 240)   # Slate 200
COLOR_TEXT_DARK = RGBColor(30, 41, 59)        # Slate 800
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500

FONT_HEADING = "Arial"
FONT_BODY = "Arial"


def render_latex_to_png(latex_formula, output_filepath, fontsize=15, color="#0F172A"):
    """Renderiza una fórmula matemática de LaTeX a PNG transparente a 300 DPI."""
    fig = plt.figure(figsize=(7.5, 1.2), dpi=300)
    fig.patch.set_alpha(0.0)
    plt.axis("off")
    plt.text(
        0.5,
        0.5,
        f"${latex_formula}$",
        fontsize=fontsize,
        color=color,
        ha="center",
        va="center",
        math_fontfamily="cm",
    )
    plt.tight_layout()
    plt.savefig(output_filepath, bbox_inches="tight", pad_inches=0.08, transparent=True, dpi=300)
    plt.close(fig)
    return output_filepath


def generar_todas_las_ecuaciones(assets_dir):
    os.makedirs(assets_dir, exist_ok=True)
    formulas = {
        "eq_slide03": r"T_g < T_{\mathrm{servicio}} < T_m \quad [\mathrm{Termopl\acute{a}stico}] \qquad T_{\mathrm{servicio}} < T_g < T_d \quad [\mathrm{Termofijo}]",
        "eq_slide05": r"DP = \frac{\bar{M}_n}{m_0} \qquad m_0 = \sum_{j} f_j \, m_j \qquad PDI = \frac{\bar{M}_w}{\bar{M}_n}",
        "eq_slide06": r"T_g = T_{g,\infty} - \frac{K}{\bar{M}_n} \quad [\mathrm{Fox\text{-}Flory}] \qquad \eta_0 \propto \bar{M}_w^{3.4} \quad (\bar{M}_w > M_c)",
        "eq_slide07": r"\langle r^2 \rangle^{1/2} = l \sqrt{N} \left( \frac{1 + \cos\theta}{1 - \cos\theta} \right)^{1/2} \quad (\theta = 109.5^\circ)",
        "eq_slide10": r"\overline{DP}_n = \frac{1}{1 - p} \quad \Rightarrow \quad p \geq 0.99 \ \mathrm{para} \ \overline{DP}_n \geq 100 \quad [\mathrm{Carothers}]",
        "eq_slide11": r"\Delta G_m = \Delta H_m - T \Delta S_m \qquad \delta = \sqrt{\frac{\Delta E_v}{V_m}} \qquad |\delta_{\mathrm{pol}} - \delta_{\mathrm{solv}}| \to 0",
        "eq_slide12": r"\tau = K \, \dot{\gamma}^n \quad (n < 1, \ \mathrm{pseudopl\acute{a}stico}) \qquad \eta(\dot{\gamma}) = K \, \dot{\gamma}^{n-1}",
    }
    rutas = {}
    for clave, latex in formulas.items():
        ruta = os.path.join(assets_dir, f"{clave}.png")
        render_latex_to_png(latex, ruta)
        rutas[clave] = ruta
    return rutas


def parse_and_add_text_with_subscripts(paragraph, text, base_font_size=Pt(10), bold=False, color=COLOR_TEXT_DARK):
    """
    Convierte automáticamente subíndices (M_n, m_0, T_g, DP_crítico, ΔG_m, δ_polímero),
    superíndices (^3.4, ^n) y términos directos (Mn, Mw, Tg) a formato nativo PPTX.
    Sustituye flechas -> por → y asteriscos * por ·.
    """
    clean_text = (
        text.replace("->", "→")
        .replace("*", "·")
        .replace("Delta G_m", "ΔG_m")
        .replace("Delta H_m", "ΔH_m")
        .replace("Delta S_m", "ΔS_m")
        .replace("Delta ", "Δ")
        .replace("delta_polímero", "δ_polímero")
        .replace("delta_solvente", "δ_solvente")
        .replace("delta_pol", "δ_pol")
        .replace("delta_solv", "δ_solv")
        .replace("eta_0", "η_0")
        .replace("punto_gamma", "punto_γ")
    )
    
    pattern = r"([A-Za-zΔγηδχτπ]+|DP)_([0-9a-záéíóúA-Z∞]+)|\^([0-9]+(?:\.[0-9]+)?|[a-zA-Z]+)|(\b[Mm]0\b|\b[Mm]n\b|\b[Mm]w\b|\b[Mm]c\b|\b[Tt]g\b|\b[Tt]m\b|\b[Tt]d\b)"
    pos = 0
    for m in re.finditer(pattern, clean_text):
        start, end = m.span()
        if start > pos:
            r = paragraph.add_run()
            r.text = clean_text[pos:start]
            r.font.name = FONT_BODY
            r.font.size = base_font_size
            r.font.bold = bold
            r.font.color.rgb = color

        if m.group(1) is not None:
            r_base = paragraph.add_run()
            r_base.text = m.group(1)
            r_base.font.name = FONT_BODY
            r_base.font.size = base_font_size
            r_base.font.bold = bold
            r_base.font.color.rgb = color

            r_sub = paragraph.add_run()
            r_sub.text = m.group(2)
            r_sub.font.name = FONT_BODY
            r_sub.font.size = base_font_size
            r_sub.font.bold = bold
            r_sub.font.color.rgb = color
            r_sub.font.subscript = True
        elif m.group(3) is not None:
            r_sup = paragraph.add_run()
            r_sup.text = m.group(3)
            r_sup.font.name = FONT_BODY
            r_sup.font.size = base_font_size
            r_sup.font.bold = bold
            r_sup.font.color.rgb = color
            r_sup.font.superscript = True
        elif m.group(4) is not None:
            tok = m.group(4)
            r_base = paragraph.add_run()
            r_base.text = tok[0]
            r_base.font.name = FONT_BODY
            r_base.font.size = base_font_size
            r_base.font.bold = bold
            r_base.font.color.rgb = color

            r_sub = paragraph.add_run()
            r_sub.text = tok[1:]
            r_sub.font.name = FONT_BODY
            r_sub.font.size = base_font_size
            r_sub.font.bold = bold
            r_sub.font.color.rgb = color
            r_sub.font.subscript = True

        pos = end

    if pos < len(clean_text):
        r_end = paragraph.add_run()
        r_end.text = clean_text[pos:]
        r_end.font.name = FONT_BODY
        r_end.font.size = base_font_size
        r_end.font.bold = bold
        r_end.font.color.rgb = color


def agregar_header(slide, titulo, subtitulo, categoria="MAESTRÍA EN CIENCIAS APLICADAS | CIENCIA E INGENIERÍA DE POLÍMEROS"):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.32))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = categoria.upper()
    p_cat.font.name = FONT_HEADING
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BURGUNDY

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = titulo
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY_NAVY

    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.38))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitulo
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED

    sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.72), Inches(11.733), Inches(0.02))
    sep.fill.solid()
    sep.fill.fore_color.rgb = COLOR_CARD_BORDER
    sep.line.fill.background()


def agregar_footer_minimal(slide, current_slide, total_slides=13):
    foot_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.0), Inches(1.0), Inches(0.35))
    tf = foot_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    p.text = f"{current_slide:02d} / {total_slides:02d}"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED


def crear_tarjeta_teorica(slide, left, top, width, height, titulo, subtitulo, items, ruta_ecuacion=None):
    """Crea la columna izquierda: tarjeta analítica y conceptual con viñetas rigurosas y ecuación."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1.0)

    padding = Inches(0.24)
    espacio_eq = Inches(1.05) if ruta_ecuacion else Inches(0)
    
    tb = slide.shapes.add_textbox(left + padding, top + padding, width - (padding * 2), height - espacio_eq - (padding * 2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p_t = tf.paragraphs[0]
    p_t.text = titulo
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_BURGUNDY

    if subtitulo:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitulo
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_after = Pt(4)

    for it in items:
        p_it = tf.add_paragraph()
        p_it.space_before = Pt(3.5)
        p_it.space_after = Pt(1.5)
        if isinstance(it, tuple):
            bold_part, regular_part = it
            parse_and_add_text_with_subscripts(p_it, f"• {bold_part}: ", base_font_size=Pt(10), bold=True, color=COLOR_PRIMARY_NAVY)
            parse_and_add_text_with_subscripts(p_it, regular_part, base_font_size=Pt(9.5), bold=False, color=COLOR_TEXT_DARK)
        else:
            parse_and_add_text_with_subscripts(p_it, f"• {it}", base_font_size=Pt(9.5), bold=False, color=COLOR_TEXT_DARK)

    if ruta_ecuacion and os.path.exists(ruta_ecuacion):
        eq_box_top = top + height - Inches(1.05)
        eq_box_height = Inches(0.9)
        eq_box_width = width - (padding * 2)
        eq_box_left = left + padding

        eq_plate = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, eq_box_left, eq_box_top, eq_box_width, eq_box_height)
        eq_plate.fill.solid()
        eq_plate.fill.fore_color.rgb = COLOR_EQ_BOX_BG
        eq_plate.line.color.rgb = COLOR_EQ_BOX_BORDER
        eq_plate.line.width = Pt(1.0)

        img_w = eq_box_width - Inches(0.2)
        slide.shapes.add_picture(ruta_ecuacion, eq_box_left + Inches(0.1), eq_box_top + Inches(0.08), width=img_w)


def crear_tarjeta_evidencia(slide, left, top, width, height, badge_texto, ruta_imagen, nota_titulo, nota_texto):
    """Crea la columna derecha: tarjeta de evidencia con recorte real del libro y nota de contraste."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_ACCENT_BG
    card.line.color.rgb = COLOR_CARD_ACCENT_BORDER
    card.line.width = Pt(1.2)

    padding = Inches(0.2)
    
    # 1. Badge superior
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + padding, top + Inches(0.16), width - (padding * 2), Inches(0.34))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(224, 242, 254) # Sky 100
    badge.line.color.rgb = RGBColor(186, 230, 253)
    badge.line.width = Pt(0.75)
    
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = badge_texto.upper()
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_COBALT

    # 2. Nota inferior de contraste / análisis
    nota_h = Inches(1.22)
    nota_top = top + height - nota_h - Inches(0.16)
    nota_w = width - (padding * 2)
    nota_left = left + padding

    nota_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, nota_left, nota_top, nota_w, nota_h)
    nota_box.fill.solid()
    nota_box.fill.fore_color.rgb = COLOR_NOTE_BG
    nota_box.line.color.rgb = COLOR_NOTE_BORDER
    nota_box.line.width = Pt(0.75)

    tf_n = nota_box.text_frame
    tf_n.word_wrap = True
    tf_n.margin_left = Inches(0.15)
    tf_n.margin_right = Inches(0.15)
    tf_n.margin_top = Inches(0.1)
    tf_n.margin_bottom = Inches(0.1)

    p_nt = tf_n.paragraphs[0]
    p_nt.text = nota_titulo
    p_nt.font.name = FONT_HEADING
    p_nt.font.size = Pt(9.5)
    p_nt.font.bold = True
    p_nt.font.color.rgb = COLOR_BURGUNDY
    p_nt.space_after = Pt(2)

    p_nx = tf_n.add_paragraph()
    parse_and_add_text_with_subscripts(p_nx, nota_texto, base_font_size=Pt(8.8), bold=False, color=COLOR_TEXT_DARK)

    # 3. Imagen central recortada del libro
    if ruta_imagen and os.path.exists(ruta_imagen):
        img_area_top = top + Inches(0.55)
        img_area_height = (nota_top - Inches(0.08)) - img_area_top
        img_area_width = width - (padding * 2)

        with Image.open(ruta_imagen) as im:
            iw, ih = im.size

        escala = min(img_area_width / iw, img_area_height / ih)
        disp_w = iw * escala
        disp_h = ih * escala

        disp_left = left + (width - disp_w) / 2
        disp_top = img_area_top + (img_area_height - disp_h) / 2

        slide.shapes.add_picture(ruta_imagen, disp_left, disp_top, width=disp_w, height=disp_h)


def construir_presentacion_artesanal():
    base_dir = "C:/Users/madia/Documents/antigravity/materiales"
    pptx_original = os.path.join(base_dir, "polimeros.pptx")
    pptx_actualizado = os.path.join(base_dir, "polimeros_actualizado.pptx")
    assets_dir = os.path.join(base_dir, "eq_assets")
    recortes_dir = os.path.join(base_dir, "recortes_libros")

    ecuaciones = generar_todas_las_ecuaciones(assets_dir)

    # Cargar la presentación existente para preservar la Portada (Slide 0) intacta
    prs = Presentation(pptx_original)
    
    # Eliminar todas las diapositivas excepto la Portada (Slide 0)
    sldIdLst = prs.slides._sldIdLst
    while len(sldIdLst) > 1:
        rId = sldIdLst[1].rId
        prs.part.drop_rel(rId)
        del sldIdLst[1]

    blank_layout = prs.slide_layouts[6]
    TOTAL_SLIDES = 13

    # Configuración geométrica de 2 columnas
    left_c1 = Inches(0.8)
    top_cards = Inches(1.85)
    width_c1 = Inches(5.65)
    height_cards = Inches(5.05)

    left_c2 = Inches(6.70)
    width_c2 = Inches(5.83)

    # =======================================================================
    # SLIDE 02: PÁGINA 111 DEL CALLISTER
    # =======================================================================
    s2 = prs.slides.add_slide(blank_layout)
    agregar_header(s2, "Análisis de la Página 111 del Callister: Redes y Configuraciones",
                   "Transición crucial de la Sección 4.7 (Network Polymers) a la Sección 4.8 (Molecular Configurations)")
    agregar_footer_minimal(s2, 2, TOTAL_SLIDES)

    items_s2 = [
        ("Estructura Tridimensional Completa", "Las unidades trifuncionales forman enlaces covalentes en las tres direcciones del espacio, anulando el desplazamiento macromolecular."),
        ("Punto de Gelificación (Gel Point)", "Transición de fase crítica donde la masa molar diverge a infinito (M_w → ∞); el polímero pasa irreversiblemente de líquido a red infusible."),
        ("Comportamiento Térmico Disyuntivo", "A diferencia de cadenas lineales que funden por rotura de enlaces secundarios de Van der Waals, las redes se degradan por pirólisis covalente."),
        ("Transición a la Sección 4.8", "Callister pasa de la arquitectura geométrica a las configuraciones moleculares que solo pueden alterarse rompiendo enlaces primarios."),
        ("Límite de Tenacidad", "Su alta densidad de entrecruzamiento genera módulos elásticos elevados a costa de fragilidad catastrófica por concentración de esfuerzos.")
    ]
    crear_tarjeta_teorica(s2, left_c1, top_cards, width_c1, height_cards,
                          "Fundamento Estructural y Transición Crítica",
                          "Análisis exegético de Callister (Pág. 111, Secciones 4.7 - 4.8)",
                          items_s2)

    crear_tarjeta_evidencia(s2, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Textual: Callister (Pág. 111, Fig. 4.7)",
                            os.path.join(recortes_dir, "callister_fig_4_7_completa.png"),
                            "Defensa Epistemológica Askeland:",
                            "Callister presenta una taxonomía estructural estática en la pág. 111; Askeland (16-1) conecta de inmediato esta red tridimensional con la cinética de curado y la imposibilidad de reciclaje termomecánico en reactores industriales.")

    # =======================================================================
    # SLIDE 03: TERMOESTABLES VS TERMOFIJOS & TG
    # =======================================================================
    s3 = prs.slides.add_slide(blank_layout)
    agregar_header(s3, "Termoplásticos vs. Termofijos: Termodinámica de la Transición Vítrea (T_g)",
                   "Relación fenomenológica entre volumen libre, temperatura vítrea y estabilidad térmica")
    agregar_footer_minimal(s3, 3, TOTAL_SLIDES)

    items_s3 = [
        ("Termoplásticos y T_g / T_m", "Cadenas lineales/ramificadas unidas por fuerzas de Van der Waals. Fluyen reversiblemente al calentarse. Operan bajo T_g (amorfos vítreos) o entre T_g y T_m (semicristalinos tenaces)."),
        ("Termofijos / Termoestables", "Red macromolecular continua con enlaces covalentes cruzados. No tienen T_m; su temperatura de degradación química (T_d) antecede cualquier transición de flujo."),
        ("Teoría del Volumen Libre", "Al enfriar a T_g, el volumen libre cae a la fracción crítica del 2.5%, congelando las rotaciones segmentarias de la cadena principal."),
        ("Reciclabilidad y Reología", "Termoplásticos son reprocesables por fusión mecánica; termofijos se descomponen irreversiblemente y requieren reciclaje químico o valorización energética.")
    ]
    crear_tarjeta_teorica(s3, left_c1, top_cards, width_c1, height_cards,
                          "Termodinámica Macromolecular y Fenomenología",
                          "Comportamiento de fases, viscoelasticidad y movilidad segmentaria",
                          items_s3, ruta_ecuacion=ecuaciones["eq_slide03"])

    crear_tarjeta_evidencia(s3, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Empírica: Askeland (Cap. 16, Fig. 16-11)",
                            os.path.join(recortes_dir, "fig_slide03_askeland_temperatura.png"),
                            "Contraste Askeland vs. Shackelford:",
                            "Shackelford define T_g mediante el cambio de pendiente del volumen específico dilatrométrico; Askeland aporta la gráfica maestra de módulo de elasticidad vs. temperatura, clave para la selección ingenieril bajo carga.")

    # =======================================================================
    # SLIDE 04: GRUPOS FUNCIONALES
    # =======================================================================
    s4 = prs.slides.add_slide(blank_layout)
    agregar_header(s4, "Química Orgánica Macromolecular: Grupos Funcionales Clave",
                   "Influencia de la reactividad monomérica y la polaridad en la cohesión interfacial")
    agregar_footer_minimal(s4, 4, TOTAL_SLIDES)

    items_s4 = [
        ("Enlaces Dobles Carbono-Carbono (C=C)", "Esqueleto de la polimerización vinílica (etileno, estireno, propileno). La apertura homolítica/heterolítica del enlace pi permite la adición en cadena sin subproductos."),
        ("Grupos Condensables (-OH, -COOH, -NH_2)", "Bases de la síntesis por pasos. Reaccionan entre monómeros bifuncionales formando ésteres y amidas con eliminación de pequeñas moléculas condensadas (H_2O, HCl)."),
        ("Densidad de Energía Cohesiva", "El grupo amida (-CO-NH-) en poliamidas aporta intensos puentes de hidrógeno intercadenas (E_coh > 30 kJ/mol), elevando drásticamente T_m y módulo elástico."),
        ("Anillos Fenileno en la Cadena", "La inclusión de anillos aromáticos en la columna vertebral (PET, PC) restringe la torsión conformacional, elevando notablemente la rigidez estructural y la T_g.")
    ]
    crear_tarjeta_teorica(s4, left_c1, top_cards, width_c1, height_cards,
                          "Clasificación y Reactividad Química",
                          "Fundamento orgánico según Callister (Tabla 4.2) y Askeland (Tabla 16-3)",
                          items_s4)

    crear_tarjeta_evidencia(s4, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Textual: Callister (Cap. 4, Tabla 4.2)",
                            os.path.join(recortes_dir, "callister_tabla_4_2_grupos.png"),
                            "Aporte Askeland vs. Callister:",
                            "Callister tabula los grupos orgánicos de manera descriptiva. Askeland vincula la presencia de grupos polares con la resistencia al ataque de solventes polares y la necesidad de secado previo del polímero fundido.")

    # =======================================================================
    # SLIDE 05: GRADO DE POLIMERIZACIÓN (DP)
    # =======================================================================
    s5 = prs.slides.add_slide(blank_layout)
    agregar_header(s5, "Grado de Polimerización (DP): Formulación y Cálculos Numéricos",
                   "Relación analítica entre masa macromolecular, unidad monomérica y arquitectura")
    agregar_footer_minimal(s5, 5, TOTAL_SLIDES)

    items_s5 = [
        ("Definición Analítica Formal", "Número medio de unidades repetitivas (meros) eslabonadas en la macromolécula: DP = M_n / m_0, donde M_n es el peso molecular promedio en número y m_0 la masa del mero."),
        ("Copolímeros y Mezcla de Meros", "En copolímeros, la masa molecular media de la unidad m_0 se calcula como suma ponderada de fracciones molares: m_0 = suma(f_j · m_j)."),
        ("Dispersidad Polimérica (PDI)", "El cociente PDI = M_w / M_n refleja la heterogeneidad de longitudes de cadena. PDI = 1.0 representa monodispersidad ideal; polímeros comerciales tienen PDI entre 1.5 y 10."),
        ("Ejemplo Numérico PTFE", "Para politetrafluoroetileno (mero -CF_2-CF_2-, m_0 = 100 g/mol) con M_n = 250,000 g/mol, el grado de polimerización es exactamente DP = 2,500 unidades.")
    ]
    crear_tarjeta_teorica(s5, left_c1, top_cards, width_c1, height_cards,
                          "Formulación Matemática y Distribución",
                          "Fundamento cuantitativo Callister Ec. 4.6 y Askeland Sec. 16-3",
                          items_s5, ruta_ecuacion=ecuaciones["eq_slide05"])

    crear_tarjeta_evidencia(s5, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Textual: Callister (Fig. 4.4) & Askeland",
                            os.path.join(recortes_dir, "callister_fig_4_4_mn_mw.png"),
                            "Defensa Askeland (El Umbral Mecánico):",
                            "Callister enseña a calcular algebraicamente el DP; Askeland demuestra que por debajo de DP_crítico ~ 100-200 el polímero carece de resistencia mecánica útil y se fractura como una cera frágil.")

    # =======================================================================
    # SLIDE 06: CLASIFICACIÓN DEL PESO MOLECULAR
    # =======================================================================
    s6 = prs.slides.add_slide(blank_layout)
    agregar_header(s6, "Clasificación del Peso Molecular: Regímenes Bajo, Medio y Alto",
                   "Umbrales de entrelazamiento mecánico, meseta de resistencia y reología de fundidos")
    agregar_footer_minimal(s6, 6, TOTAL_SLIDES)

    items_s6 = [
        ("Régimen de Bajo Peso Molecular (M_n < 10^4 g/mol)", "Oligómeros y parafinas. No alcanzan la longitud crítica de entrelazamiento físico (M_c); presentan fluencia plástica inmediata y baja resistencia mecánica."),
        ("Régimen de Peso Medio (10^4 < M_n < 10^5 g/mol)", "Rango comercial de moldeo por inyección y extrusión. La resistencia a la tracción y la tenacidad alcanzan una meseta asintótica gobernada por Fox-Flory."),
        ("Régimen de Alto Peso Molecular (M_n > 10^6 g/mol, UHMWPE)", "Máxima resistencia al desgaste y tenacidad extrema. Viscosidad hiperbólica en fundido (eta_0 proporcional a M_w^3.4) que impide moldeo convencional."),
        ("Ecuación de Fox-Flory", "Describe la dependencia de T_g con el número de extremos libres de cadena: T_g = T_g,infinito - K / M_n.")
    ]
    crear_tarjeta_teorica(s6, left_c1, top_cards, width_c1, height_cards,
                          "Regímenes Moleculares e Implicaciones",
                          "Transición de propiedades físicas según Callister y Askeland",
                          items_s6, ruta_ecuacion=ecuaciones["eq_slide06"])

    crear_tarjeta_evidencia(s6, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Empírica: Callister (Cap. 4, Fig. 4.3)",
                            os.path.join(recortes_dir, "callister_fig_4_3_distribucion_pm.png"),
                            "El Compromiso Ingenieril (Trade-Off):",
                            "Askeland enfatiza que maximizar peso molecular mejora las propiedades mecánicas y térmicas, pero incrementa exponencialmente la caída de presión en moldes de inyección, exigiendo un compromiso de diseño.")

    # =======================================================================
    # SLIDE 07: FORMA Y CONFIGURACIÓN MOLECULAR
    # =======================================================================
    s7 = prs.slides.add_slide(blank_layout)
    agregar_header(s7, "Topología Macromolecular: Forma Molecular vs. Configuración",
                   "Conformación por rotación de enlaces simples frente a arquitectura irreversible")
    agregar_footer_minimal(s7, 7, TOTAL_SLIDES)

    items_s7 = [
        ("Conformación (Forma Molecular)", "Arreglos espaciales adoptados exclusivamente por rotación en torno a enlaces simples carbono-carbono (sigma). Varía libremente con temperatura, cizalla y disolución."),
        ("Modelo del Ovillamiento Aleatorio (Random Coil)", "La cadena libremente articulada se contrae estocásticamente; la distancia cuadrática media extremo a extremo escala con <r^2>^1/2 = l · sqrt(N)."),
        ("Barreras Estéricas Rotacionales", "Grupos laterales voluminosos (como el anillo fenilo en PS) generan impedimento estérico, restringiendo las rotaciones C-C y elevando la rigidez conformacional."),
        ("Configuración Molecular", "Estructura química geométrica fija que solo puede alterarse mediante la rotura y recombinación de enlaces covalentes primarios.")
    ]
    crear_tarjeta_teorica(s7, left_c1, top_cards, width_c1, height_cards,
                          "Conformación, Entropía y Flexibilidad",
                          "Mecánica estadística del ovillo macromolecular (Callister Sec. 4.6)",
                          items_s7, ruta_ecuacion=ecuaciones["eq_slide07"])

    crear_tarjeta_evidencia(s7, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Textual: Callister (Cap. 4, Fig. 4.6)",
                            os.path.join(recortes_dir, "fig_slide07_callister_shape.png"),
                            "Orientación y Estiramiento Uniaxial:",
                            "Callister modela el ovillo estático en reposo. Askeland destaca que durante el estiramiento y soplado industrial, los ovillos se alinean paralelamente, elevando la resistencia en esa dirección hasta un 300%.")

    # =======================================================================
    # SLIDE 08: ISOMERISMO Y TACTICIDAD
    # =======================================================================
    s8 = prs.slides.add_slide(blank_layout)
    agregar_header(s8, "Isomerismo Macromolecular: Tacticidad y Variaciones Geométricas",
                   "Estereoisomería (tacticidad) e isomería geométrica (cis/trans) y su efecto en la cristalinidad")
    agregar_footer_minimal(s8, 8, TOTAL_SLIDES)

    items_s8 = [
        ("Estereoisomería y Tacticidad", "Configuración de grupos laterales R respecto al plano macromolecular: Isotáctico (mismo lado, altamente cristalino), Sindiotáctico (alternado regular), Atáctico (caótico, 100% amorfo)."),
        ("Catálisis de Coordinación Ziegler-Natta", "Permitió la síntesis estereoselectiva de polipropileno isotáctico cristalizable (T_m = 165 °C), superando al PP atáctico amorfo e inútil mecánicamente."),
        ("Isomería Geométrica (cis vs. trans)", "Presencia de dobles enlaces C=C rígidos con impedimento de rotación en la cadena principal: cis-isómero y trans-isómero."),
        ("Contraste cis vs. trans en Poliisopreno", "cis-Poliisopreno (Caucho Natural) es un elastómero gomoso (T_g = -70 °C); trans-Poliisopreno (Gutapercha) es un termoplástico rígido y semicristalino a 25 °C.")
    ]
    crear_tarjeta_teorica(s8, left_c1, top_cards, width_c1, height_cards,
                          "Control Estereoquímico y Cristalinidad",
                          "Fundamento de Callister Sec. 4.8 y Askeland Sec. 16-6",
                          items_s8)

    crear_tarjeta_evidencia(s8, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Comparativa: Askeland (Fig. 16-20)",
                            os.path.join(recortes_dir, "fig_slide08_askeland_cistrans_diagrama.png"),
                            "Lección Clave de Ciencia de Materiales:",
                            "Askeland muestra cómo un cambio geométrico en torno al doble enlace transforma un material elastomérico de llantas (cis) en una resina termoplástica dura usada en recubrimientos de pelotas de golf (trans).")

    # =======================================================================
    # SLIDE 09: USO DE ADITIVOS
    # =======================================================================
    s9 = prs.slides.add_slide(blank_layout)
    agregar_header(s9, "Formulación y Uso Estratégico de Aditivos Industriales",
                   "Modificación de procesabilidad, estabilidad química y reducción de costo")
    agregar_footer_minimal(s9, 9, TOTAL_SLIDES)

    items_s9 = [
        ("Plastificantes (Ftalatos, Adipatos)", "Moléculas de bajo peso molecular que se disuelven en la matriz polimérica; separan cadenas, incrementan el volumen libre y reducen drásticamente la T_g (ej. PVC rígido a manguera flexible)."),
        ("Cargas y Refuerzos (Fillers)", "Carbonato de calcio, talco, fibra de vidrio. Elevan el módulo elástico, la resistencia a la fluencia, la estabilidad dimensional y reducen el coste por volumen."),
        ("Estabilizantes Térmicos y Antioxidantes", "Capturan radicales libres peróxido durante el fundido a más de 200 °C, evitando la escisión oxidativa de la cadena."),
        ("Estabilizantes UV (HALS)", "Amoladores de amina estéricamente impedida y absorbentes benzotriazoles que inhiben la fotodegradación por radiación solar en exteriores."),
        ("Retardantes de Llama", "Compuestos halogenados o trihidrato de alúmina (Al(OH)_3) que liberan agua endotérmicamente suprimiendo la combustión.")
    ]
    crear_tarjeta_teorica(s9, left_c1, top_cards, width_c1, height_cards,
                          "Paquetes de Formulación Industrial",
                          "Clasificación según Callister Sec. 14.12 y Shackelford Sec. 13.5",
                          items_s9)

    crear_tarjeta_evidencia(s9, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Textual: Callister (Sec. 14.12)",
                            os.path.join(recortes_dir, "callister_sec_14_12_aditivos.png"),
                            "La Realidad Práctica (Shackelford 13.5):",
                            "Shackelford destaca que en la industria real un polímero puro casi nunca tiene viabilidad técnica sin su paquete de lubricantes de extrusión, antioxidantes y plastificantes formulados.")

    # =======================================================================
    # SLIDE 10: PROCESOS DE SÍNTESIS PETROQUÍMICA
    # =======================================================================
    s10 = prs.slides.add_slide(blank_layout)
    agregar_header(s10, "Procesos de Síntesis Macromolecular: La Vía Petroquímica",
                   "De las fracciones del petróleo (naftas/olefina) a la ingeniería de reactores")
    agregar_footer_minimal(s10, 10, TOTAL_SLIDES)

    items_s10 = [
        ("Cadena Petroquímica de Valor", "Craqueo con vapor de naftas y gas natural -> Olefinas ligeras (etileno, propileno, butadieno) y aromáticos (BTX). Síntesis de monómeros de pureza de polimerización (>99.9%)."),
        ("Polimerización por Adición (Cadena)", "Iniciación por radicales libres o catalizadores Ziegler-Natta / metalocenos. Crecimiento ultrarrápido en milisegundos sin formación de subproductos."),
        ("Polimerización por Condensación (Pasos)", "Reacción equilibrada entre monómeros difuncionales formando enlaces éster, amida o uretano, liberando pequeñas moléculas (H_2O, HCl)."),
        ("Ecuación de Carothers", "Demuestra la rigurosa exigencia estequiométrica: para obtener DP_n >= 100, la conversión fraccionaria de monómero debe ser superior al 99% (p >= 0.99).")
    ]
    crear_tarjeta_teorica(s10, left_c1, top_cards, width_c1, height_cards,
                          "Cinética y Mecanismos de Reacción",
                          "Termodinámica de síntesis y Carothers (Askeland Sec. 16-2)",
                          items_s10, ruta_ecuacion=ecuaciones["eq_slide10"])

    crear_tarjeta_evidencia(s10, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Textual: Askeland (Cap. 16, Fig. 16-6)",
                            os.path.join(recortes_dir, "askeland_fig_16_6_condensacion_pet.png"),
                            "Enfoque de Ingeniería Química (Askeland):",
                            "Askeland resalta el diseño del reactor de condensación: para desplazar el equilibrio hacia altos pesos moleculares en PET es indispensable operar a alto vacío y retirar continuamente el vapor de agua generado.")

    # =======================================================================
    # SLIDE 11: SOLVENTES Y SOLUBILIDAD
    # =======================================================================
    s11 = prs.slides.add_slide(blank_layout)
    agregar_header(s11, "Termodinámica de Soluciones Poliméricas y Solubilidad",
                   "Energía libre de mezcla, parámetro de Hildebrand y respuesta según la arquitectura")
    agregar_footer_minimal(s11, 11, TOTAL_SLIDES)

    items_s11 = [
        ("Termodinámica de Mezcla (Delta G_m)", "Para disolución espontánea: Delta G_m = Delta H_m - T · Delta S_m < 0. Debido al confinamiento de meros en cadenas enlazadas, la entropía de mezcla Delta S_m es órdenes de magnitud menor que en moléculas simples."),
        ("Dominio Entálpico y Parámetro de Hildebrand (delta)", "Delta H_m debe ser prácticamente nulo o negativo. Criterio de miscibilidad de Hildebrand: |delta_polímero - delta_solvente| → 0."),
        ("Teoría de Flory-Huggins", "Introduce el parámetro de interacción chi; predice separación espontánea de fases cuando chi supera el valor crítico de 0.5."),
        ("Disolución vs. Hinchamiento (Flory-Rehner)", "Polímeros lineales/ramificados se disuelven completamente; los termofijos entrecruzados NO se disuelven, solo se hinchan elásticamente hasta el equilibrio osmótico.")
    ]
    crear_tarjeta_teorica(s11, left_c1, top_cards, width_c1, height_cards,
                          "Termodinámica de Soluciones y Redes",
                          "Fundamento de Shackelford (Sec. 13.4) y Flory-Rehner",
                          items_s11, ruta_ecuacion=ecuaciones["eq_slide11"])

    crear_tarjeta_evidencia(s11, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Textual: Shackelford (Tabla 13.3)",
                            os.path.join(recortes_dir, "fig_slide11_shackelford_solubilidad.png"),
                            "Enfoque Shackelford vs. Askeland:",
                            "Shackelford formaliza matemáticamente los parámetros de solubilidad delta; Askeland (Cap. 23) utiliza el hinchamiento en solventes orgánicos para medir empíricamente la densidad de entrecruzamiento de elastómeros.")

    # =======================================================================
    # SLIDE 12: PROCESAMIENTO INDUSTRIAL
    # =======================================================================
    s12 = prs.slides.add_slide(blank_layout)
    agregar_header(s12, "Procesamiento y Transformación a Nivel Industrial",
                   "Reología no newtoniana (adelgazamiento por cizalla) y operaciones unitarias")
    agregar_footer_minimal(s12, 12, TOTAL_SLIDES)

    items_s12 = [
        ("Reología Pseudoplástica (Shear Thinning)", "Los fundidos poliméricos exhiben caída de viscosidad bajo alta velocidad de cizalla (tau = K · punto_gamma^n, con n < 1). En boquillas de inyección las cadenas se desenrollan y orientan, facilitando el llenado del molde."),
        ("Extrusión de Husillo", "Operación continua de transporte, compresión, fusión y bombeo a través de una matriz para producir perfiles, tubos, láminas y recubrimientos de cables."),
        ("Moldeo por Inyección", "Proceso cíclico para piezas complejas. Involucra plastificación por husillo reciprocante, inyección a alta presión y mantenimiento de empaque para compensar la contracción por cristalización."),
        ("Soplado y Termoformado", "Conformado neumático de preformas tubulares (parisons) para botellas de PET/PEAD y conformado de láminas delgadas al vacío para empaques.")
    ]
    crear_tarjeta_teorica(s12, left_c1, top_cards, width_c1, height_cards,
                          "Reología y Operaciones de Transformación",
                          "Manufactura industrial según Askeland Sec. 16-10 y Callister Cap. 14",
                          items_s12, ruta_ecuacion=ecuaciones["eq_slide12"])

    crear_tarjeta_evidencia(s12, left_c2, top_cards, width_c2, height_cards,
                            "Evidencia Gráfica: Askeland (Fig. 16-25)",
                            os.path.join(recortes_dir, "fig_slide12_askeland_procesamiento.png"),
                            "La Gran Fortaleza de Askeland:",
                            "Mientras Callister trata el procesamiento como un apéndice descriptivo, Askeland analiza la reología, las presiones de inyección y los perfiles térmicos como variables primarias de diseño de ingeniería.")

    # =======================================================================
    # SLIDE 13: CONCLUSIONES Y DEFENSA EPISTEMOLÓGICA
    # =======================================================================
    s13 = prs.slides.add_slide(blank_layout)
    agregar_header(s13, "Conclusiones y Defensa Epistemológica: El Modelo de Askeland",
                   "Síntesis epistemológica frente a Callister y Shackelford en la Ingeniería de Polímeros")
    agregar_footer_minimal(s13, 13, TOTAL_SLIDES)

    items_s13 = [
        ("La Trilogía Epistemológica", "Callister ofrece la taxonomía estructural y la cristalografía rigurosa; Shackelford brinda los fundamentos termodinámicos de volumen libre y energía de mezcla; Askeland integra la manufactura y la selección bajo servicio."),
        ("La Tesis del Ingeniero Químico", "En la industria no basta saber calcular el DP o definir un mero; el ingeniero químico debe anticipar la viscosidad de inyección, gobernar la transición vítrea y formular con aditivos funcionales."),
        ("Relación Estructura-Propiedad-Procesamiento", "Las propiedades no son fijas: dependen directamente de la historia térmica y de cizalla impartida en la máquina de transformación."),
        ("Sostenibilidad Macromolecular", "El diseño moderno de materiales poliméricos exige transitar del ciclo lineal a la reciclabilidad termomecánica y química cerrada.")
    ]
    crear_tarjeta_teorica(s13, left_c1, top_cards, width_c1, height_cards,
                          "Defensa Intelectual del Ingeniero de Materiales",
                          "Articulación dialéctica de los tres textos base para la maestría",
                          items_s13)

    crear_tarjeta_evidencia(s13, left_c2, top_cards, width_c2, height_cards,
                            "Cuadro Comparativo Maestro: Askeland (Tabla 16-1)",
                            os.path.join(recortes_dir, "askeland_tabla_16_1_categorias.png"),
                            "Cierre de la Defensa:",
                            "La Tabla 16-1 de Askeland resume la visión de esta exposición: la ingeniería de materiales triunfa cuando las decisiones macromoleculares garantizan la confiabilidad estructural y la viabilidad del procesamiento.")

    # Guardar en archivo actualizado
    prs.save(pptx_actualizado)
    print(f"Presentación actualizada generada con éxito en: {pptx_actualizado}")

    # Sobrescribir polimeros.pptx directamente
    try:
        prs.save(pptx_original)
        print(f"¡ÉXITO! 'polimeros.pptx' sobreescrito directamente.")
    except PermissionError:
        print(f"AVISO: 'polimeros.pptx' está actualmente abierto en PowerPoint. Se ha guardado en 'polimeros_actualizado.pptx'.")

    return pptx_actualizado


if __name__ == "__main__":
    construir_presentacion_artesanal()
