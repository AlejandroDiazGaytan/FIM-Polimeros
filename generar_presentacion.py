"""
=============================================================================
PIPELINE DE EXPOSICIÓN ACADÉMICA - FASE 1: GENERACIÓN DE PRESENTACIÓN
Maestría en Ciencias Aplicadas — Fundamentos de Ingeniería de Materiales
Docente: Dr. Julio César Armas Pérez
Alumno: Miguel Alejandro Díaz Gaytán
=============================================================================
Versión 3.0:
- Portada actualizada con datos del curso (Docente Dr. Julio César Armas Pérez,
  Alumno Miguel Alejandro Díaz Gaytán y logo oficial).
- Eliminación de pie de página formal ("expositor iqs..."), sustituido por
  numeración limpia y minimalista.
- Renderizado de ecuaciones en alta fidelidad (LaTeX a 300 DPI).
- Parseo automático de subíndices y superíndices nativos en PowerPoint
  (sin guiones bajos tipo M_n o m_0 en texto).
"""

import os
import re
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# PALETA DE COLOR Y ESTILO
# ---------------------------------------------------------------------------
COLOR_BG_DARK = RGBColor(15, 23, 42)          # Slate 900
COLOR_TEXT_LIGHT = RGBColor(248, 250, 252)    # Slate 50
COLOR_PRIMARY_NAVY = RGBColor(30, 41, 59)     # Slate 800
COLOR_BURGUNDY = RGBColor(153, 27, 27)        # Red 800
COLOR_GOLD = RGBColor(217, 119, 6)            # Amber 600 (para subtítulo de portada)
COLOR_COBALT = RGBColor(29, 78, 216)          # Blue 700
COLOR_CARD_BG = RGBColor(248, 250, 252)       # Slate 50
COLOR_CARD_BORDER = RGBColor(203, 213, 225)   # Slate 300
COLOR_CARD_ACCENT_BG = RGBColor(240, 249, 255) # Sky 50
COLOR_CARD_ACCENT_BORDER = RGBColor(147, 197, 253) # Sky 300
COLOR_EQ_BOX_BG = RGBColor(255, 255, 255)     # Blanco puro
COLOR_EQ_BOX_BORDER = RGBColor(186, 230, 253) # Borde suave azul
COLOR_TEXT_DARK = RGBColor(30, 41, 59)        # Slate 800
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500

FONT_HEADING = "Arial"
FONT_BODY = "Arial"


def render_latex_to_png(latex_formula, output_filepath, fontsize=15, color="#0F172A"):
    """
    Renderiza una fórmula matemática de LaTeX a un PNG transparente a 300 DPI
    usando la tipografía Computer Modern de matplotlib.
    """
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
    """
    Genera las imágenes de fórmulas analíticas para insertar en las diapositivas.
    """
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
    Parsea texto plano y agrega runs a un párrafo de python-pptx convirtiendo
    automáticamente patrones como M_n, m_0, T_g, DP_crítico a subíndices reales
    (run.font.subscript = True) y patrones como ^3.4 a superíndices reales.
    Elimina por completo el uso de guiones bajos visibles.
    """
    # Regex:
    # Grupo 1 y 2: Subíndices tipo M_n, m_0, T_g, M_w, M_c, f_j, m_j, ΔG_m, η_0, DP_crítico
    # Grupo 3: Superíndices tipo ^3.4, ^n, ^6
    pattern = r"([A-Za-zΔγη]+|DP)_([0-9a-záéíóúA-Z∞]+)|\^([0-9a-záéíóú·\.]+)"
    pos = 0
    for m in re.finditer(pattern, text):
        start, end = m.span()
        if start > pos:
            r = paragraph.add_run()
            r.text = text[pos:start]
            r.font.name = FONT_BODY
            r.font.size = base_font_size
            r.font.bold = bold
            r.font.color.rgb = color

        if m.group(1) is not None:
            # Base
            r_base = paragraph.add_run()
            r_base.text = m.group(1)
            r_base.font.name = FONT_BODY
            r_base.font.size = base_font_size
            r_base.font.bold = bold
            r_base.font.color.rgb = color

            # Subíndice
            r_sub = paragraph.add_run()
            r_sub.text = m.group(2)
            r_sub.font.name = FONT_BODY
            r_sub.font.size = base_font_size
            r_sub.font.bold = bold
            r_sub.font.color.rgb = color
            r_sub.font.subscript = True
        elif m.group(3) is not None:
            # Superíndice
            r_sup = paragraph.add_run()
            r_sup.text = m.group(3)
            r_sup.font.name = FONT_BODY
            r_sup.font.size = base_font_size
            r_sup.font.bold = bold
            r_sup.font.color.rgb = color
            r_sup.font.superscript = True

        pos = end

    if pos < len(text):
        r_end = paragraph.add_run()
        r_end.text = text[pos:]
        r_end.font.name = FONT_BODY
        r_end.font.size = base_font_size
        r_end.font.bold = bold
        r_end.font.color.rgb = color


def crear_presentacion(output_path=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if output_path is None:
        output_path = os.path.join(base_dir, "presentacion_polimeros_maestria.pptx")
    elif not os.path.isabs(output_path):
        output_path = os.path.join(base_dir, output_path)

    assets_dir = os.path.join(base_dir, "eq_assets")
    ecuaciones = generar_todas_las_ecuaciones(assets_dir)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def aplicar_fondo(slide, color=RGBColor(255, 255, 255)):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def agregar_header(slide, slide_num, titulo, subtitulo, categoria="MAESTRÍA EN CIENCIAS APLICADAS | CIENCIA E INGENIERÍA DE POLÍMEROS"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
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
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_PRIMARY_NAVY

        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.4))
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
        """Pie de diapositiva minimalista sin textos formales repetitivos."""
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

    def crear_tarjeta(slide, left, top, width, height, titulo, items, es_destacada=False, subtitulo_tarjeta=None, ruta_ecuacion=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_ACCENT_BG if es_destacada else COLOR_CARD_BG
        card.line.color.rgb = COLOR_CARD_ACCENT_BORDER if es_destacada else COLOR_CARD_BORDER
        card.line.width = Pt(1.5 if es_destacada else 1.0)

        espacio_eq = Inches(1.15) if ruta_ecuacion else Inches(0)
        padding = Inches(0.24)
        
        tb = slide.shapes.add_textbox(left + padding, top + padding, width - (padding * 2), height - espacio_eq - (padding * 2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = titulo
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(13.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_COBALT if es_destacada else COLOR_BURGUNDY

        if subtitulo_tarjeta:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitulo_tarjeta
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(9.5)
            p_sub.font.italic = True
            p_sub.font.color.rgb = COLOR_TEXT_MUTED
            p_sub.space_after = Pt(4)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.space_before = Pt(4)
            p_it.space_after = Pt(2)
            if isinstance(it, tuple):
                bold_part, regular_part = it
                # Viñeta en negrita
                parse_and_add_text_with_subscripts(p_it, f"• {bold_part}: ", base_font_size=Pt(10.5 if not es_destacada else 11), bold=True, color=COLOR_PRIMARY_NAVY)
                # Texto regular con subíndices reales
                parse_and_add_text_with_subscripts(p_it, regular_part, base_font_size=Pt(10 if not es_destacada else 10.5), bold=False, color=COLOR_TEXT_DARK)
            else:
                parse_and_add_text_with_subscripts(p_it, f"• {it}", base_font_size=Pt(10 if not es_destacada else 10.5), bold=False, color=COLOR_TEXT_DARK)

        if ruta_ecuacion and os.path.exists(ruta_ecuacion):
            eq_box_top = top + height - Inches(1.1)
            eq_box_height = Inches(0.95)
            eq_box_width = width - (padding * 2)
            eq_box_left = left + padding

            eq_plate = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, eq_box_left, eq_box_top, eq_box_width, eq_box_height)
            eq_plate.fill.solid()
            eq_plate.fill.fore_color.rgb = COLOR_EQ_BOX_BG
            eq_plate.line.color.rgb = COLOR_EQ_BOX_BORDER
            eq_plate.line.width = Pt(1.0)

            img_w = eq_box_width - Inches(0.2)
            slide.shapes.add_picture(ruta_ecuacion, eq_box_left + Inches(0.1), eq_box_top + Inches(0.1), width=img_w)

    # =======================================================================
    # DIAPOSITIVA 01: PORTADA ACADÉMICA (CON APRENDIZAJES DEL USUARIO)
    # =======================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide1, COLOR_BG_DARK)

    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.15), Inches(4.5))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = COLOR_BURGUNDY
    accent_bar.line.fill.background()

    tb_portada = slide1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(8.0), Inches(4.5))
    tf_p = tb_portada.text_frame
    tf_p.word_wrap = True

    p0 = tf_p.paragraphs[0]
    p0.text = "MAESTRÍA EN CIENCIAS APLICADAS — Fundamentos de Ingeniería de Materiales"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(12.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_GOLD
    p0.space_after = Pt(14)

    p1 = tf_p.add_paragraph()
    p1.text = "Ciencia e Ingeniería de Polímeros:\nEstructura, Termodinámica y Procesamiento"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_LIGHT
    p1.space_after = Pt(24)

    p2 = tf_p.add_paragraph()
    p2.text = "Docente: Dr. Julio César Armas Pérez"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(6)

    p3 = tf_p.add_paragraph()
    p3.text = "Alumno: Miguel Alejandro Díaz Gaytán"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(15)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(96, 165, 250)

    # Insertar el logo extraído de la portada que colocó el usuario
    logo_path = os.path.join(base_dir, "logo_portada.png")
    if os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(9.5), Inches(3.5), width=Inches(2.5))

    # =======================================================================
    # DIAPOSITIVA 02: ANÁLISIS DE LA PÁGINA 111 DEL CALLISTER
    # =======================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide2)
    agregar_header(slide2, 2, "Análisis de la Página 111 del Callister: Redes y Configuraciones",
                   "Transición crucial de la Sección 4.7 (Network Polymers) a la Sección 4.8 (Molecular Configurations)")
    
    crear_tarjeta(slide2, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Contenido Textual de la Página 111", [
                      ("Figura 4.7 (d)", "Esquema canónico de redes tridimensionales a partir de monómeros multifuncionales (funcionalidad > 2 enlaces covalentes activos)."),
                      ("Polímeros en Red", "Callister define materiales reticulados con rigidez térmica y mecánica: resinas epoxi, poliuretanos y fenol-formaldehído (baquelita)."),
                      ("Continuo Estructural", "Se enfatiza que polímeros lineales reales presentan grados finitos de ramificación o entrecruzamiento lateral."),
                      ("Inicio Sección 4.8", "La regularidad y simetría de los grupos laterales R (-Cl, -CH₃) gobierna las configuraciones espaciales."),
                      ("Arreglo Cabeza-Cola", "En pág. 112 formaliza la alternancia regular de sustituyentes R para minimizar repulsiones electrostáticas y estéricas.")
                  ], subtitulo_tarjeta="Enfoque Formal Cristalográfico (Callister, 7ª Ed.)")

    crear_tarjeta(slide2, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "Defensa de la Perspectiva Askeland (Cap. 16)", [
                      ("Física Reológica vs. Esquema Estático", "Callister reduce la red a un esquema de esferas y varillas; Askeland analiza la masa molecular entre entrecruzamientos (M_c) y el módulo elástico en meseta."),
                      ("Extinción de Relajación Reptacional", "Askeland (16-9) demuestra que los nudos covalentes eliminan el flujo viscoso irreversible, transformando el material en un sólido elástico no reciclable."),
                      ("Fenómeno de Gelificación", "Mientras Callister describe monómeros trifuncionales, Askeland analiza el punto de gel en reactores químicos, variable crítica para evitar la solidificación prematura."),
                      ("Conclusión Crítica", "Callister clasifica la geometría; Askeland proporciona la herramienta cuantitativa de ingeniería y reología.")
                  ], es_destacada=True, subtitulo_tarjeta="Confrontación Crítica con Askeland vs. Callister")
    agregar_footer_minimal(slide2, 2)

    # =======================================================================
    # DIAPOSITIVA 03: POLÍMEROS TERMOESTABLES VS TERMOFIJOS & Tg
    # =======================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide3)
    agregar_header(slide3, 3, "Termoestables vs. Termofijos: Termodinámica de la Transición Vítrea (T_g)",
                   "Diferenciación conceptual rigurosa y comportamiento de fases bajo temperatura")
    
    crear_tarjeta(slide3, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Diferenciación Conceptual y Terminología", [
                      ("Polímeros Termofijos", "Designa el mecanismo cinético de curado químico irreversible: calor, presión o catalizadores forman entrecruzamientos covalentes permanentes."),
                      ("Polímeros Termoestables", "Designa la respuesta fenomenológica en servicio: resistencia a la deformación bajo carga mecánica a temperaturas elevadas."),
                      ("Contraste Termoplástico", "Cadenas lineales o ramificadas unidas por fuerzas de Van der Waals; funden reversiblemente y permiten reciclado mecánico."),
                      ("Tratamiento Shackelford", "Shackelford (Cap. 13) los homogeniza bajo 'polímeros reticulados', omitiendo la cinética de gelificación en manufactura."),
                      ("Tratamiento Askeland", "Askeland (16-1 y 16-9) distingue cómo la densidad de entrecruzamiento dicta la transición vítrea y la viabilidad del conformado.")
                  ], subtitulo_tarjeta="Cinética de Curado vs. Estabilidad Funcional")

    crear_tarjeta(slide3, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "El Rol Fundamental de la Temperatura Vítrea (T_g)", [
                      ("Frontera Termodinámica T_g", "Temperatura en la cual el volumen libre permite la rotación coordinada de segmentos de 20-50 meros."),
                      ("Termoplásticos", "Bajo T_g: comportamiento vítreo rígido y frágil. Sobre T_g: estado gomoso. Sobre T_m: flujo viscoso moldeable."),
                      ("Termofijos & Red Covalente", "La elevada densidad de reticulación bloquea el flujo macromolecular; carecen de T_m medible."),
                      ("Degradación Térmica (T_d)", "Al calentar un termofijo por encima de su límite operativo, ocurre pirólisis y escisión covalente antes de fluir (T_d < T_m ficticia).")
                  ], es_destacada=True, subtitulo_tarjeta="Criterio Operativo en Ingeniería de Materiales",
                  ruta_ecuacion=ecuaciones["eq_slide03"])
    agregar_footer_minimal(slide3, 3)

    # =======================================================================
    # DIAPOSITIVA 04: GRUPOS FUNCIONALES DE QUÍMICA ORGÁNICA
    # =======================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide4)
    agregar_header(slide4, 4, "Química Orgánica Macromolecular: Grupos Funcionales Clave",
                   "Monomers precursores, reactividad de enlace y familias comerciales resultantes")
    
    crear_tarjeta(slide4, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.9),
                  "Vinílicos y Olefinas", [
                      (">C=C< (Alquenos)", "Etileno, propileno, cloruro de vinilo, estireno."),
                      ("Polimerización", "Adición radicalaria o por inserción catalítica con complejos Ziegler-Natta."),
                      ("Polímeros Clave", "PE (alta y baja densidad), PP, PVC, PS, PTFE (Teflón)."),
                      ("Propiedades", "Cadenas apolares o polares lineales; máximo volumen de producción petroquímica.")
                  ], subtitulo_tarjeta="Crecimiento en Cadena")

    crear_tarjeta(slide4, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.9),
                  "Ésteres, Amidas e Isocianatos", [
                      ("-OH y -COOH", "Reacción de esterificación que sintetiza PET y Policarbonato."),
                      ("-NH₂ y -COOH", "Enlace amida (-CONH-) que produce poliamidas (Nylon 6,6) y aramidas (Kevlar)."),
                      ("-N=C=O (Isocianato)", "Reacciona con polioles para generar enlaces uretano (-NH-COO-)."),
                      ("Subproductos", "Generación estequiométrica de moléculas pequeñas (H₂O, HCl) que deben retirarse.")
                  ], subtitulo_tarjeta="Crecimiento por Etapas")

    crear_tarjeta(slide4, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.9),
                  "Epóxidos, Fenoles y Siliconas", [
                      ("Oxirano (Epoxi)", "Anillo tenso C-O-C; apertura nucleofílica con poliaminas sin subproductos volátiles."),
                      ("Fenol-Formaldehído", "Resinas fenólicas (resol y novolaca); redes tridimensionales termoestables."),
                      ("-Si-O-Si- (Siloxanos)", "Polímeros inorgánicos/híbridos; extraordinaria flexibilidad y resistencia térmica."),
                      ("Aporte Askeland", "Askeland (16-2) liga la funcionalidad con la densidad de entrecruzamiento resultante.")
                  ], es_destacada=True, subtitulo_tarjeta="Termofijos y Redes")
    agregar_footer_minimal(slide4, 4)

    # =======================================================================
    # DIAPOSITIVA 05: DEFINICIÓN Y CÁLCULO DEL GRADO DE POLIMERIZACIÓN
    # =======================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide5)
    agregar_header(slide5, 5, "Grado de Polimerización (DP): Formulación y Cálculos Numéricos",
                   "Relación analítica entre masa macromolecular, unidad monomérica y arquitectura")
    
    crear_tarjeta(slide5, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Formulación Matemática y Copolímeros", [
                      ("Definición Formal", "Número medio de unidades repetitivas (meros) eslabonadas en la macromolécula."),
                      ("Ecuación Fundamental", "Relación directa entre el peso molecular promedio en número (M_n) y la masa de la unidad monomérica (m_0)."),
                      ("Masa Media en Copolímeros", "Pondera la fracción molar (f_j) y la masa (m_j) de cada comonómero en la cadena."),
                      ("Índice de Polidispersidad (PDI)", "Razón entre el peso ponderado (M_w) y el peso numérico (M_n); cuantifica la dispersión de longitudes."),
                      ("Caso de Estudio Numérico", "En PTFE (mero -CF₂-CF₂-, m_0 = 100 g/mol): con M_n = 250,000 g/mol se obtiene DP = 2,500.")
                  ], subtitulo_tarjeta="Fundamento Cuantitativo (Callister Ec. 4.6)",
                  ruta_ecuacion=ecuaciones["eq_slide05"])

    crear_tarjeta(slide5, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "Defensa Askeland: El DP como Umbral Mecánico", [
                      ("DP Crítico Mecánico", "Askeland (16-3) demuestra que por debajo de DP_crítico ~ 100-200, los polímeros carecen de resistencia útil (se comportan como ceras frágiles)."),
                      ("Entrelazamiento Físico", "Solo al superar la longitud crítica de cadena se consolidan los entrelazamientos intermoleculares que transmiten esfuerzo cortante."),
                      ("Trade-Off en Manufactura", "Un DP excesivo eleva exponencialmente la viscosidad del fundido, impidiendo el moldeo por inyección; se requiere un balance óptimo de fluidez y tenacidad."),
                      ("Crítica Epistemológica", "Callister enseña a resolver la ecuación; Askeland enseña a gobernar el reactor para fijar las propiedades mecánicas finales.")
                  ], es_destacada=True, subtitulo_tarjeta="Perspectiva Ingenieril (Askeland Sec. 16-3)")
    agregar_footer_minimal(slide5, 5)

    # =======================================================================
    # DIAPOSITIVA 06: CLASIFICACIÓN DEL PESO MOLECULAR
    # =======================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide6)
    agregar_header(slide6, 6, "Clasificación del Peso Molecular: Regímenes Bajo, Medio y Alto",
                   "Efecto determinante sobre la viscosidad, cinética térmica y desempeño mecánico")
    
    crear_tarjeta(slide6, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Regímenes de Peso Molecular", [
                      ("Bajo Peso (< 10,000 g/mol)", "Oligómeros, ceras y plastificantes. Sin entrelazamientos mecánicos estables; viscosidad baja y fragilidad extrema."),
                      ("Peso Medio (10,000 a 100,000 g/mol)", "Termoplásticos comerciales estándar. Óptimo balance entre resistencia a la tracción y fluidez para inyección."),
                      ("Alto y Ultra Alto Peso (> 100,000 a > 10⁶ g/mol)", "Polímeros de ingeniería y UHMWPE. Extraordinaria resistencia al desgaste, fatiga y tenacidad balística."),
                      ("Ecuación de Fox-Flory", "Describe cómo la concentración de extremos libres disminuye al aumentar M_n, estabilizando T_g hacia un valor asintótico T_g,∞.")
                  ], subtitulo_tarjeta="Clasificación Estructural de Cadenas",
                  ruta_ecuacion=ecuaciones["eq_slide06"])

    crear_tarjeta(slide6, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "Comportamiento Reológico y Procesabilidad (Askeland)", [
                      ("Ley de Viscosidad Cero-Corte", "La viscosidad en fundido escala con (M_w)^3.4 para masas superiores al entrelazamiento M_c; duplicar M_w multiplica la viscosidad por 10.5."),
                      ("Dilema de Procesamiento en UHMWPE", "Con pesos moleculares de 3-6 millones g/mol, el UHMWPE no puede fundirse ni inyectarse; exige sinterización por compresión en caliente."),
                      ("Contraste con Shackelford", "Shackelford se enfoca en técnicas de medición (GPC, osmometría); Askeland vincula la distribución de pesos con la reología en planta."),
                      ("Control del Creep", "A mayor peso molecular, el tiempo de relajación segmental aumenta y disminuye drásticamente la fluencia en frío bajo carga estática.")
                  ], es_destacada=True, subtitulo_tarjeta="Enfoque Mecánico-Reológico")
    agregar_footer_minimal(slide6, 6)

    # =======================================================================
    # DIAPOSITIVA 07: FORMA MOLECULAR VS CONFIGURACIÓN MOLECULAR
    # =======================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide7)
    agregar_header(slide7, 7, "Topología Macromolecular: Forma Molecular vs. Configuración",
                   "Frontera conceptual estricta: Conformación dinámica reversible vs. Estereoquímica inmutable")
    
    crear_tarjeta(slide7, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Forma Molecular (Conformación)", [
                      ("Origen Físico", "Rotación térmica libre alrededor de enlaces simples C-C, respetando el ángulo tetraédrico sp³ de 109.5°."),
                      ("Estado Termodinámico", "Cadena en ovillo estadístico aleatorio (random coil), gobernada por la maximización de la entropía conformacional."),
                      ("Modificación Externa", "Se altera dinámicamente mediante energía térmica o deformación cortante SIN romper ningún enlace químico."),
                      ("Elasticidad Entrópica", "Base del comportamiento del caucho: al estirarse disminuye la entropía; al retirar la carga recupera el ovillamiento espontáneamente.")
                  ], subtitulo_tarjeta="Dinámica Rotacional Reversible (Callister Sec. 4.6)",
                  ruta_ecuacion=ecuaciones["eq_slide07"])

    crear_tarjeta(slide7, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "Configuración Molecular (Estereoquímica)", [
                      ("Definición Rigurosa", "Arreglo geométrico fijo y permanente de átomos y grupos sustituyentes a lo largo del esqueleto covalente."),
                      ("Inmutabilidad", "NO puede modificarse mediante simple rotación térmica; exige ruptura y formación de nuevos enlaces covalentes."),
                      ("Arreglo Cabeza-Cola", "Configuración predominante frente a cabeza-cabeza para evitar la repulsión polar estérica."),
                      ("Criterio de Cristalinidad (Askeland)", "Askeland (16-5) enfatiza que solo configuraciones regulares permiten el empaquetamiento laminar en esferulitas."),
                      ("Conclusión Clave", "La conformación responde a la termodinámica del instante; la configuración es la huella química indeleble de la síntesis.")
                  ], es_destacada=True, subtitulo_tarjeta="Estructura Fija Inmutable (Callister Sec. 4.8 / Askeland 16-5)")
    agregar_footer_minimal(slide7, 7)

    # =======================================================================
    # DIAPOSITIVA 08: ISOMERISMO EN POLÍMEROS (TACTICIDAD Y GEOMÉTRICOS)
    # =======================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide8)
    agregar_header(slide8, 8, "Isomerismo Macromolecular: Tacticidad y Variaciones Geométricas",
                   "Efecto de la estereorregularidad sobre la cristalinidad y el módulo mecánico")
    
    crear_tarjeta(slide8, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Estereoisomerismo (Tacticidad)", [
                      ("Isotáctico", "Todos los grupos laterales R se ubican en el mismo lado del plano. Alta simetría → cristaliza con facilidad → alta T_m (ej. PP isotáctico T_m ≈ 165 °C)."),
                      ("Sindiotáctico", "Grupos laterales R alternan sus posiciones con rigurosa periodicidad espacial. Cristaliza más lentamente pero con alta estabilidad."),
                      ("Atáctico", "Distribución espacial caótica y aleatoria de los grupos R. Es totalmente incapaz de cristalizar (completamente amorfo, goma a T_g ≈ -10 °C)."),
                      ("Relevancia Histórica", "Antes de los catalizadores Ziegler-Natta, el polipropileno atáctico era una pasta sin valor técnico; la catálisis estereoespecífica creó un material estructural.")
                  ], subtitulo_tarjeta="Asimetría Espacial de Grupos Laterales")

    crear_tarjeta(slide8, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "Isomería Geométrica en Polidienos (Cis vs. Trans)", [
                      ("Cis-1,4-poliisopreno (Caucho Natural)", "Grupos -CH₃ y -H del mismo lado del doble enlace; genera una torsión espacial permanente que impide cristalizar a temperatura ambiente → elastómero superelástico."),
                      ("Trans-1,4-poliisopreno (Gutapercha)", "Grupos en lados opuestos del doble enlace; adopta una estructura en zigzag simétrica, cristaliza fácilmente y es un termoplástico rígido."),
                      ("Defensa Askeland (16-8)", "Askeland enfatiza cómo un simple cambio geométrico altera el módulo elástico en tres órdenes de magnitud."),
                      ("Comparación con Shackelford", "Shackelford cita la diferencia empíricamente; Askeland deduce la curva constitutiva esfuerzo-deformación desde la estereoquímica.")
                  ], es_destacada=True, subtitulo_tarjeta="Geometría de Dobles Enlaces C=C")
    agregar_footer_minimal(slide8, 8)

    # =======================================================================
    # DIAPOSITIVA 09: USO ESTRATÉGICO DE ADITIVOS
    # =======================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide9)
    agregar_header(slide9, 9, "Formulación y Uso Estratégico de Aditivos Industriales",
                   "Modificación deliberada para viabilidad de procesado y optimización de propiedades")
    
    crear_tarjeta(slide9, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Familias Principales de Aditivos", [
                      ("Plastificantes", "Compuestos de bajo peso molecular (ftalatos, ésteres) que aumentan el volumen libre y reducen drásticamente la T_g (ej. PVC rígido a flexible)."),
                      ("Cargas y Rellenos (Fillers)", "Carbonato de calcio (CaCO₃), talco, negro de humo y fibra de vidrio. Elevan el módulo elástico, bajan contracción y reducen el costo volumétrico."),
                      ("Estabilizadores Térmicos y UV", "Antioxidantes fenólicos y aminas impedidas (HALS). Neutralizan radicales libres e impiden la escisión fotolítica de cadenas."),
                      ("Retardantes de Llama", "Compuestos clorados, bromados o de fósforo que inhiben la reacción en cadena de combustión o generan carbonizado protector."),
                      ("Lubricantes y Desmoldeantes", "Estearatos metálicos y ceras que reducen la fricción viscosa interna y facilitan la expulsión del molde.")
                  ], subtitulo_tarjeta="Componentes de Formulación Comercial")

    crear_tarjeta(slide9, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "La Visión Integradora de Askeland (Sec. 16-11)", [
                      ("Polímero Virgen vs. Compuesto Comercial", "Askeland insiste en que un polímero virgen es un intermedio no comercializable; la formulación dicta el desempeño real en servicio."),
                      ("Sinergia Matriz-Refuerzo", "El negro de humo en cauchos no actúa como mero colorante, sino como agente de refuerzo que multiplica por 4 la resistencia al desgarro."),
                      ("Procesamiento Seguro de PVC", "Sin estabilizadores térmicos, el PVC experimenta deshidrocloración catalítica autocatalítica, degradando el polímero y corroyendo la extrusora."),
                      ("Criterio de Formulación", "Shackelford clasifica los aditivos descriptivamente; Askeland los trata como variables operativas indispensables en el diseño de ingeniería.")
                  ], es_destacada=True, subtitulo_tarjeta="Ingeniería de Formulación de Compuestos")
    agregar_footer_minimal(slide9, 9)

    # =======================================================================
    # DIAPOSITIVA 10: PROCESOS DE SÍNTESIS (VÍA PETROQUÍMICA)
    # =======================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide10)
    agregar_header(slide10, 10, "Procesos de Síntesis Macromolecular: La Vía Petroquímica",
                   "Ruta desde el craqueo de hidrocarburos hasta la polimerización en cadena y por etapas")
    
    crear_tarjeta(slide10, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Origen Petroquímico y Mecanismos", [
                      ("Alimentación Petroquímica", "Craqueo con vapor de naftas y gas licuado → olefinas básicas (etileno, propileno, butadieno) y aromáticos (benceno, tolueno, xilenos)."),
                      ("Polimerización por Adición", "Crecimiento en cadena (chain-growth) iniciado por radicales libres, aniones, cationes o sitios catalíticos coordinados. No hay subproductos."),
                      ("Etapas Cinéticas", "Iniciación → Propagación ultrarrápida (milisegundos) → Terminación (acoplamiento o desproporción)."),
                      ("Polimerización por Condensación", "Crecimiento por etapas (step-growth) entre monómeros polifuncionales. Se elimina estequiométricamente agua, HCl o metanol.")
                  ], subtitulo_tarjeta="Cinética y Mecanismos de Reacción",
                  ruta_ecuacion=ecuaciones["eq_slide10"])

    crear_tarjeta(slide10, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "El Desafío Ingenieril en Condensación (Askeland vs. Shackelford)", [
                      ("Ecuación de Carothers", "Para lograr pesos moleculares con resistencia mecánica útil (DP_n ≥ 100), la conversión química (p) debe exceder el 99.0%."),
                      ("Equilibrio Químico Reversible", "La policondensación es un equilibrio químico reversible. La hidrólisis inversa corta las cadenas salvo que se aplique alto vacío para desvolatilizar el subproducto."),
                      ("Sensibilidad Estequiométrica", "Askeland (16-2) enfatiza que una desviación estequiométrica de apenas 1% entre grupos reactivos fija un límite asintótico muy bajo al peso molecular."),
                      ("Confrontación Epistemológica", "Callister esquematiza las reacciones en pizarrón; Askeland expone la termodinámica del reactor de polimerización continuo.")
                  ], es_destacada=True, subtitulo_tarjeta="Ingeniería de Reactores de Polimerización")
    agregar_footer_minimal(slide10, 10)

    # =======================================================================
    # DIAPOSITIVA 11: SOLVENTES Y RELACIÓN CON LA SOLUBILIDAD
    # =======================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide11)
    agregar_header(slide11, 11, "Termodinámica de Soluciones Poliméricas y Solubilidad",
                   "Energía libre de mezcla, parámetro de Hildebrand y respuesta según la arquitectura")
    
    crear_tarjeta(slide11, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Termodinámica de Mezclas Macromoleculares", [
                      ("Energía Libre de Gibbs", "Relación fundamental ΔG_m = ΔH_m - T·ΔS_m. La disolución es termodinámicamente espontánea si ΔG_m < 0."),
                      ("Entropía de Mezcla Anómala", "Debido al confinamiento de miles de meros en una cadena covalente continua, ΔS_m es órdenes de magnitud menor que en micromoléculas."),
                      ("Dominio Entálpico", "Al ser T·ΔS_m ≈ 0, el signo de ΔG_m lo determina la entalpía de mezcla ΔH_m; se requiere una entalpía casi nula o negativa."),
                      ("Parámetro de Hildebrand (δ)", "Densidad de energía cohesiva. Criterio de compatibilidad: la diferencia |δ_polímero - δ_solvente| tiende a cero."),
                      ("Teoría de Flory-Huggins", "Parámetro de interacción adimensional χ; predice separación de fases cuando χ > 0.5 (mal solvente).")
                  ], subtitulo_tarjeta="Fundamento Termodinámico (Shackelford Sec. 13.4)",
                  ruta_ecuacion=ecuaciones["eq_slide11"])

    crear_tarjeta(slide11, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "Efecto de la Arquitectura: Disolución vs. Hinchamiento", [
                      ("Polímeros Lineales y Ramificados", "El solvente penetra, afloja enlaces secundarios de Van der Waals, hincha la matriz y finalmente disuelve las cadenas por completo en solución homogénea."),
                      ("Termoestables y Redes Reticuladas", "NO se disuelven en ningún solvente orgánico. Los enlaces covalentes cruzados impiden la dispersión macromolecular indefinida."),
                      ("Hinchamiento en Equilibrio (Flory-Rehner)", "El solvente es absorbido hasta que la presión osmótica de mezcla se equilibra exactamente con la fuerza elástica de retracción de la red reticular."),
                      ("Criterio Askeland en Corrosión (Cap. 23)", "Askeland utiliza el grado de hinchamiento como ensayo analítico en laboratorio para calcular experimentalmente la masa molar entre entrecruzamientos (M_c).")
                  ], es_destacada=True, subtitulo_tarjeta="Enfoque de Resistencia Química (Askeland)")
    agregar_footer_minimal(slide11, 11)

    # =======================================================================
    # DIAPOSITIVA 12: TRATAMIENTO A NIVEL INDUSTRIAL (PROCESAMIENTO)
    # =======================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide12)
    agregar_header(slide12, 12, "Procesamiento y Transformación a Nivel Industrial",
                   "Tecnologías de manufactura para termoplásticos y termofijos: Control reológico y térmico")
    
    crear_tarjeta(slide12, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9),
                  "Tecnologías de Conformado Industrial", [
                      ("Extrusión (Continuo)", "Plastificación en husillo forzando el paso a través de una hilera calibrada: perfiles continuos, tubería y película tubular soplada."),
                      ("Moldeo por Inyección (Cíclico)", "Alta presión (> 1,000 bar) inyectando el fundido en moldes refrigerados de acero para piezas tridimensionales de alta precisión."),
                      ("Moldeo por Soplado", "Expansión neumática de una preforma hueca fundida (párison) contra las paredes del molde: botellas, garrafones y tanques."),
                      ("Moldeo por Compresión y Transferencia", "Exclusivo para termoestables (resinas epoxi, fenólicos). La preforma cura químicamente en el molde caliente bajo alta presión.")
                  ], subtitulo_tarjeta="Clasificación por Naturaleza del Polímero",
                  ruta_ecuacion=ecuaciones["eq_slide12"])

    crear_tarjeta(slide12, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9),
                  "Variables Maestras Reológicas e Ingenieriles (Askeland 16-11)", [
                      ("Comportamiento Shear Thinning", "Los fundidos poliméricos disminuyen su viscosidad aparente con la tasa de cizalla (n < 1); Askeland enseña a diseñar los canales de inyección aprovechando este efecto."),
                      ("Cinética de Enfriamiento y Morfología", "El enfriamiento rápido (quenching) suprime la formación de esferulitas cristalinas dando polímeros amorfos y transparentes; el enfriamiento lento maximiza módulo y dureza."),
                      ("Control de Esfuerzos Residuales", "La contracción volumétrica diferencial en paredes gruesas genera tensiones internas y alabeo; se requiere optimizar la presión de sostenimiento."),
                      ("Defensa Askeland", "Frente a manuales empíricos, Askeland unifica la reología no-newtoniana con las leyes de transferencia de calor transitoria en molde.")
                  ], es_destacada=True, subtitulo_tarjeta="Ingeniería Reológica de Procesos")
    agregar_footer_minimal(slide12, 12)

    # =======================================================================
    # DIAPOSITIVA 13: CONCLUSIONES Y DEFENSA DEL ENFOQUE ASKELAND
    # =======================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    aplicar_fondo(slide13)
    agregar_header(slide13, 13, "Conclusiones y Defensa Epistemológica: El Modelo de Askeland",
                   "Síntesis comparativa final para la toma de decisiones en Ingeniería Química de Materiales")
    
    crear_tarjeta(slide13, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.9),
                  "William D. Callister", [
                      ("Fortaleza Canónica", "Excelente taxonomía estructural y descripciones cristalográficas formales."),
                      ("Página 111 Emblemática", "Redes tridimensionales y estereoisomería explicadas con pulcritud geométrica."),
                      ("Limitación Ingenieril", "Compartimentaliza la estructura y el procesamiento en capítulos distantes; enfoque marcadamente descriptivo y estático.")
                  ], subtitulo_tarjeta="Taxonomía y Estructura")

    crear_tarjeta(slide13, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.9),
                  "James F. Shackelford", [
                      ("Fortaleza Canónica", "Concisión conceptual, análisis termodinámico de mezclas y criterios de solubilidad."),
                      ("Selección de Materiales", "Capítulo 20 pionero en sustitución técnica de termoestables por termoplásticos de alto desempeño."),
                      ("Limitación Ingenieril", "Menor profundidad en reología de fundidos no-newtonianos y diseño mecánico ante fatiga/fluencia.")
                  ], subtitulo_tarjeta="Termodinámica y Selección")

    crear_tarjeta(slide13, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.9),
                  "Donald R. Askeland (Defensa)", [
                      ("Integración Total", "Unifica la reactividad química, la conformación estérica, la reología y el procesamiento industrial en un solo hilo conductor."),
                      ("Enfoque Fenomenológico", "Traduce el grado de polimerización y la T_g en curvas constitutivas esfuerzo-deformación y ventanas operativas de planta."),
                      ("Conclusión del Expositor", "Para el Ingeniero Químico e investigador, Askeland representa la herramienta teórica y metodológica superior.")
                  ], es_destacada=True, subtitulo_tarjeta="Prevalencia en Ingeniería Aplicada")
    agregar_footer_minimal(slide13, 13)

    # -----------------------------------------------------------------------
    # GUARDAR PRESENTACIÓN
    # -----------------------------------------------------------------------
    prs.save(output_path)
    print(f"[FASE 1 COMPLETADA] Presentación guardada exitosamente en: {os.path.abspath(output_path)}")
    return output_path


if __name__ == "__main__":
    crear_presentacion()
