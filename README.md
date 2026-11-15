# FIM-Polímeros
## Maestría en Ciencias Aplicadas — Fundamentos de Ingeniería de Polímeros
**Universidad de Guanajuato**  
**Docente:** Dr. Julio César Armas Pérez  
**Alumno:** Miguel Alejandro Díaz Gaytán  

🌐 **Presentación Web Interactiva (GitHub Pages):**  
[https://alejandrodiazgaytan.github.io/FIM-Polimeros/](https://alejandrodiazgaytan.github.io/FIM-Polimeros/)

---

## 🎯 Descripción del Proyecto
Este repositorio contiene el ecosistema completo desarrollado para la preparación, estudio y defensa académica de la materia **Fundamentos de Ingeniería de Polímeros**, integrando el contraste crítico entre los tres textos canónicos: **Askeland**, **Callister** y **Shackelford**.

El proyecto abarca:
1. 🌐 **Página Web Interactiva Estilo Prezi (`index.html`)**: lienzo infinito 2D en alta resolución con navegación guiada (pan & zoom continuo), diagramación de árbol macromolecular, pre-renderizado semántico de ecuaciones y evidencias gráficas recortadas de los libros.
2. 📊 **Presentación en Diapositivas (`polimeros.pptx`)**: presentación en formato 16:9 con recortes bibliográficos, tipografía formal y formulación matemática analítica.
3. 🎙️ **Guion de Exposición y Síntesis de Voz Neuronal (`speech_exposicion.txt` & `audios_exposicion/`)**: guion en primera persona estructurado para la defensa oral ante el docente y pistas sintetizadas con redes neuronales (`edge-tts`).
4. 🤖 **Automatización en Python**: scripts para regenerar presentaciones, sintetizar voz y orquestar el flujo de trabajo (`pipeline_completo.py`, `generar_presentacion_artesanal.py`, `sintetizar_voz.py`).
5. 📚 **Capítulos Monográficos y Guía de Prompts (`capitulos_notebooklm/` & `GUIA_PROMPTS_NOTEBOOKLM.md`)**: material de estudio y batería de preguntas críticas para NotebookLM.

---

## 🧭 Contenido del Árbol Macromolecular
- **Composición Química y Reactividad:** grupos funcionales orgánicos, energía de cohesión intermolecular, mecanismos de polimerización por adición (sitios activos radicalarios) y condensación por pasos (ecuación de Carothers), y aditivos industriales.
- **Tamaño y Peso Molecular:** grado de polimerización ($DP$), promedios $\overline{M}_n$ y $\overline{M}_w$, índice de polidispersidad ($PDI$) y ecuación de Fox-Flory.
- **Forma Molecular (Conformación):** rotación en torno a enlaces $\sigma$, ovillamiento aleatorio (*random coil*) y orientación mecánica uniaxial.
- **Arquitectura y Topología:** lineal, ramificada, entrecruzada y en red tridimensional continua (*gel point* e infusibilidad).
- **Estados Isoméricos:** estereoisomería (tacticidad isotáctica, sindiotáctica y atáctica) e isomería geométrica (*cis* vs. *trans* en dienos / vulcanización).
- **Módulos de Ingeniería:** termodinámica de la transición vítrea ($T_g$) y termofijos, solubilidad de Hildebrand e hinchamiento de Flory-Rehner, reología pseudoplástica y procesamiento industrial (extrusión e inyección).

---

## 💻 Ejecución y Trabajo Remoto

### 1. Clonar Repositorio
```bash
git clone https://github.com/AlejandroDiazGaytan/FIM-Polimeros.git
cd FIM-Polimeros
```

### 2. Entorno de Python (Local o Remoto / Google Colab)
Instala las dependencias necesarias:
```bash
pip install python-pptx edge-tts matplotlib
```

### 3. Scripts Disponibles
- **Servidor local para la web:**
  ```bash
  python iniciar_servidor_web.py
  ```
- **Pipeline completo (Presentación + Speech + Voz):**
  ```bash
  python pipeline_completo.py
  ```
- **Generar presentación PowerPoint artesanal:**
  ```bash
  python generar_presentacion_artesanal.py
  ```
- **Sintetizar pistas de voz neuronal:**
  ```bash
  python sintetizar_voz.py
  ```

---

## 🎮 Controles de la Presentación Web
- `→` / `Re Pág` o botón **Siguiente**: Avanzar por las 15 paradas del tour.
- `←` / `Av Pág` o botón **Anterior**: Retroceder en el tour.
- **Detalle Teórico**: Abre el panel lateral con el marco analítico y recorte bibliográfico ampliable.
- `Home` o botón **Vista Panorámica**: Reajusta la cámara al mapa completo.
- **Rueda del Ratón / Arrastrar**: Zoom continuo y paneo libre sobre el lienzo.

---

## 🏛️ Créditos Académicos
* **Institución:** Universidad de Guanajuato (UGTO)
* **Programa:** Maestría en Ciencias Aplicadas
* **Materia:** Fundamentos de Ingeniería de Polímeros
* **Docente:** Dr. Julio César Armas Pérez
* **Alumno:** Miguel Alejandro Díaz Gaytán
