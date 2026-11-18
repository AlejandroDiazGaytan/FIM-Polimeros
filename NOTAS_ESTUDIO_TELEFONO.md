# Guía de Bolsillo y Notas de Estudio: Polímeros Industriales
**Materia:** Fundamentos de Ingeniería de Materiales — Maestría en Ciencias Aplicadas (UGTO)  
**Alumno:** I.Q.S. Miguel Alejandro Díaz Gaytán  
**Docente:** Dr. Julio César Armas Pérez  

---

## 🛡️ Estrategia de Escape: ¿Qué responder si pregunta sobre "Termodinámica"?
> **Regla de oro:** No intentes memorizar ecuaciones diferenciales o derivar Gibbs ($\Delta G = \Delta H - T\Delta S$) si no la dominas en este momento. Lleva la respuesta al **terreno físico y estructural**:
>
> *"Profesor, más allá de la formulación termodinámica de fases, en ingeniería de transformación lo determinante es la **movilidad segmental de las cadenas**. Por debajo de $T_g$, los enlaces carbono-carbono están 'congelados' en una configuración rígida; al elevar la temperatura por encima de $T_g$, la agitación térmica desbloquea la rotación alrededor de los enlaces $\sigma$, permitiendo que el polímero transicione de estado vítreo a gomoso. En los **termoplásticos**, como las cadenas están unidas solo por fuerzas secundarias débiles de Van der Waals, esto permite el flujo viscoso y el moldeo repetible. En los **termofijos**, la presencia de una red covalente tridimensional infinita impide cualquier deslizamiento de cadenas, por lo que el material no funde y mantiene su rigidez hasta su descomposición térmica."*

---

## 🔬 1. Síntesis Química: Adición (Cadena) vs. Condensación (Pasos)

| Característica | Polimerización por Adición (*Chain-Growth*) | Polimerización por Condensación (*Step-Growth*) |
|---|---|---|
| **Tipo de Monómero** | Insaturados con dobles enlaces reactivos ($C=C$, alquenos vinílicos). | Monómeros bifuncionales o polifuncionales con grupos reactivos complementarios ($-COOH$, $-OH$, $-NH_2$). |
| **Mecanismo** | Requiere un iniciador que genera un centro activo (radical, anión, catión). El centro activo se transfiere sucesivamente a la unidad añadida. | Reacción orgánica clásica paso a paso entre grupos funcionales (esterificación, amidación). Cualquier dímero u oligómero puede reaccionar entre sí. |
| **Subproductos** | **Cero subproductos.** La masa del polímero es múltiplo entero exacto del monómero. | **Se libera invariablemente una molécula pequeña** ($H_2O$, $HCl$, metanol). |
| **Cinética y Crecimiento** | Las cadenas individuales crecen a tamaño completo ($>100,000\text{ g/mol}$) en milisegundos ($10^{-3}\text{ s}$). En el reactor solo conviven monómeros sin reaccionar y cadenas gigantes. | El peso molecular promedio crece muy lentamente a lo largo de horas. Monómero ➔ dímero ➔ trímero ➔ oligómero. |
| **Requisito de Conversión** | Alto peso molecular alcanzable a bajas conversiones globales de monómero. | **Ecuación de Carothers:** Para alcanzar longitudes útiles ($\overline{DP}_n \geq 100$), se requiere una conversión química $p \geq 0.99$ (99%), obligando a usar alto vacío para retirar el agua/subproducto y evitar la hidrólisis reversible. |
| **Ejemplos en los 10 Polímeros** | **Polietileno (HDPE y LDPE), Polipropileno (PP), Policloruro de Vinilo (PVC), Poliestireno (PS).** | **PET (poliéster), Nylon 6,6 (poliamida), Baquelita (fenol-formaldehído), Poliéster Insaturado (UPR).** *(Nota: Epoxis y Poliuretanos son poliadiciones sin subproducto pero crecen por pasos funcionales).* |

---

## 🎯 2. Pregunta de Oro: ¿Por qué hay polimerización radicalaria y no solo se unen 2 radicales?

> **La Pregunta del Profesor:**  
> *"¿Por qué ocurre la polimerización entre los monómeros después de que una especie radicalaria la inicia y no se unen 2 radicales simplemente?"*

### Tu Respuesta Maestra (Explicación Refinada):
*"Profesor, tu intuición inicial sobre **probabilidad y homogeneidad** es 100% correcta; el sustento cinético y mecanístico formal se resume en 3 pilares:*

1. **Ley de Acción de Masas y Razón Estadística ($[M] \gg [R^\bullet]$):**  
   En el medio de reacción existe una diferencia descomunal de concentraciones:  
   * Concentración de monómero neutro: $[M] \sim 1 - 10\text{ mol/L}$ (fase masiva concentrada).  
   * Concentración de radicales libres activos en estado estacionario: $[R^\bullet] \sim 10^{-7} - 10^{-9}\text{ mol/L}$ (ultradiluida).  
   * **¡Hay entre 10 y 100 millones de monómeros neutros por cada radical libre!** Físicamente, un radical libre en solución está rodeado en todo momento por un 'mar' de moléculas de monómero. La probabilidad matemática de que dos radicales libres choquen entre sí en ese mar es ínfima comparada con la colisión contra un monómero.

2. **La Naturaleza Regenerativa del Centro Activo (Propagación):**  
   Cuando el radical libre ataca el enlace $\pi$ de un monómero vinílico, rompe el doble enlace y forma un nuevo enlace covalente $\sigma$, pero **el electrón desapareado no se destruye ni se neutraliza**: se transfiere intacto al carbono terminal de la unidad que se acaba de pegar:
   $$R^\bullet + CH_2=CHX \longrightarrow R-CH_2-\dot{C}HX$$
   Ese nuevo extremo terminal sigue siendo un radical libre idéntico que repite el proceso miles de veces en una fracción de milisegundo ($10^{-3}\text{ s}$).

3. **¿Cuándo sí se unen dos radicales? ¡Esa es precisamente la TERMINACIÓN!:**  
   Sí ocurre la unión de dos radicales, pero ocurre únicamente como el **evento final que detiene el crecimiento de la cadena**:  
   * **Por Combinación o Acoplamiento:** Los extremos de dos cadenas en crecimiento colisionan de frente y sus electrones desapareados forman un enlace covalente simple ($M_n^\bullet + M_m^\bullet \longrightarrow M_{n+m}$).  
   * **Por Desproporción:** Un radical sustrae un átomo de hidrógeno del otro, produciendo una cadena saturada y otra con un doble enlace terminal.  
   Como la velocidad de terminación bimolecular depende del cuadrado de la concentración de radicales ($v_t = 2 k_t [R^\bullet]^2$), mientras que la propagación depende de la concentración masiva de monómero ($v_p = k_p [M][R^\bullet]$), la propagación domina absolutamente hasta que el monómero se agota."*

---

## 🧱 3. Las 4 Estructuras Macromoleculares (Analogías Directas)

| Estructura | Unión Intercadena | Comportamiento Mecánico y Térmico | Ejemplos Reales | Analogía Simple |
|---|---|---|---|---|
| **1. Lineal** | Fuerzas de Van der Waals débiles o puentes de H. | Cadenas rectas sin ramas. Fácil empaquetamiento, alta cristalinidad potencial, alta rigidez y límite elástico. Funden y fluyen con calor. | HDPE, PVC rígido, PET, Nylon 6,6. | **Espagueti cocido:** Las hebras pueden resbalar una sobre otra si se tira de ellas. |
| **2. Ramificado** | Fuerzas de Van der Waals débiles, pero con mayor separación. | Cadenas con ramas secundarias. Las ramas estorban el empaquetamiento (menor densidad, menor cristalinidad, menor $T_m$, pero mayor flexibilidad y elongación). | LDPE (PEBD), LLDPE. | **Ramas de zarza o pino:** No se pueden apretar en un paquete compacto; dejan mucho espacio vacío. |
| **3. Entrecruzado (*Crosslinked*)** | Enlaces covalentes transversales periódicos. | Cadenas lineales unidas en puntos específicos por enlaces químicos (ej. puentes de azufre). Impiden el flujo pero permiten estiramiento masivo reversible (>200%). | Caucho vulcanizado de llantas, elastómeros. | **Escalera de cuerda o resortes:** Se estira mucho y regresa a su forma original por memoria elástica. |
| **4. De Red Tridimensional (*Network*)** | Toda la pieza es una sola molécula covalente gigante. | Monómeros trifuncionales o polifuncionales. No funden (infusibles), no se disuelven (insolubles), máxima rigidez y dureza, pero fractura frágil sin fluencia. | Resinas Epoxi, Baquelita, Poliuretano rígido, Poliéster Insaturado. | **Jaula o malla metálica soldada:** No se puede doblar sin fracturarla ni desarmar con calor. |

---

## 📦 4. Los 10 Polímeros Más Utilizados (Quién es quién)

### Termoplásticos (Commodities)
1. **PET (Tereftalato de polietileno - SPI #1):** Lineal por condensación. Transparente, rígido, barrera impermeable a gases ($CO_2$).  
   *Usos:* Botellas de refrescos y agua, fibras textiles (poliéster).
2. **HDPE (Polietileno de Alta Densidad - SPI #2):** Lineal por adición. Cadena compacta, denso, alta resistencia química y rigidez.  
   *Usos:* Galones de leche, tuberías de agua potable y drenaje, bidones químicos.
3. **PVC (Policloruro de vinilo - SPI #3):** Lineal con átomos de cloro ($\sim 57\%$ en peso). Autoextinguible, duradero a la intemperie.  
   *Usos:* Tuberías sanitarias e hidráulicas, marcos de ventanas, aislamientos de cables.
4. **LDPE (Polietileno de Baja Densidad - SPI #4):** Ramificado por alta presión. Cadenas con ramas cortas y largas; baja densidad, flexible y dúctil.  
   *Usos:* Bolsas de plástico, películas para emplayar (*stretch film*), juguetes flexibles.
5. **PP (Polipropileno - SPI #5):** Lineal con grupos metilo. Es el plástico más liviano ($\sim 0.90\text{ g/cm}^3$), excelente resistencia a fatiga por flexión.  
   *Usos:* Bisagras vivas integradas, parachoques automotrices, envases para microondas.
6. **PS (Poliestireno - SPI #6):** Lineal con anillos de benceno voluminosos. Rígido, vidrioso y frágil a temperatura ambiente ($T_g \approx 100^\circ\text{C}$).  
   *Usos:* Vasos desechables, cajas transparentes de CD, aislamiento térmico espumado (unicel / EPS).

### Termofijos (Polímeros de Red)
7. **Resinas Epóxicas (Epoxi):** Anillos oxirano curados con poliaminas. Cero contracción al fraguar, adherencia y resistencia mecánica estructural máxima.  
   *Usos:* Pegamentos aeroespaciales, palas de aerogeneradores eólicos (con fibra de carbono), encapsulado de microchips.
8. **Fenol-Formaldehído (Baquelita):** Red fenólica densa. Gran dureza superficial, excelente aislamiento térmico y eléctrico.  
   *Usos:* Mangos de sartenes y planchas, disyuntores eléctricos, discos de corte abrasivo.
9. **Poliuretano Reticulado (PU):** Reacción de diisocianatos con polioles. Espumas microcelulares rígidas con la menor conductividad térmica del mercado.  
   *Usos:* Aislamiento térmico de refrigeradores, espumas de asientos, suelas de botas de seguridad.
10. **Resinas de Poliéster Insaturado (UPR):** Poliéster lineal mezclado con monómero de estireno que cura a temperatura ambiente.  
    *Usos:* Plástico reforzado con fibra de vidrio (PRFV) para lanchas, tinacos y láminas para techos.

---

## ⚙️ 5. Procesos de Conformado Industrial (Resumen en 30 segundos)

* **Extrusión (Continuo):** Tornillo sinfín compacta, funde y empuja el plástico a través de una boquilla abierta con forma fija; al salir, se enfría en una tina de agua.  
  *Productos:* Tuberías de HDPE/PVC, perfiles de ventana, cables forrados, láminas.
* **Moldeo por Inyección (Cíclico de alta precisión):** El husillo actúa como pistón e inyecta plástico fundido a alta presión ($>1000\text{ bar}$) dentro de un molde metálico frío. Se abre y expulsa la pieza en segundos.  
  *Productos:* Tapas roscadas, carcasas de electrodomésticos, piezas automotrices, jeringas.
* **Moldeo por Soplado (*Blow Molding*):** Se extruye o inyecta un tubo hueco caliente (parisón) y se le inyecta aire comprimido como un globo para inflarlo contra las paredes del molde.  
  *Productos:* Botellas de refresco (PET), galones de detergente (HDPE).
* **Termoformado:** Se calienta una lámina de plástico previamente extruida por encima de $T_g$ y se succiona con vacío o prensa neumática sobre un molde.  
  *Productos:* Vasos desechables, charolas de comida rápida, empaques tipo blister.
* **Rotomoldeo (Moldeo Rotacional):** Se introduce plástico en polvo en un molde que gira biaxialmente dentro de un horno; el polímero recubre homogéneamente las paredes por gravedad.  
  *Productos:* Tinacos gigantes de agua (Rotoplas), kayaks, contenedores sin costuras ni esfuerzos residuales.
* **Moldeo por Compresión y Transferencia (Termofijos):** Se coloca polvo o preforma en un molde caliente; bajo presión hidráulica el material llena la cavidad y reacciona químicamente (cura).  
  *Dato clave:* **¡La pieza se desmolda caliente!** Ya no funde porque la red covalente se formó de manera permanente.

---

## ♻️ 6. Los 7 Métodos de Reciclaje (Normas ISO 15270 y ASTM D5033)

1. **Reciclaje Primario (*Closed-loop* / Re-extrusión en planta):** Molienda y reincorporación inmediata de recortes limpios y rebabas dentro de la misma fábrica sin pérdida de calidad.
2. **Reciclaje Secundario (Mecánico Post-Consumo):** Plásticos urbanos/comerciales clasificados, lavados, triturados en hojuelas (*flakes*), extruidos y convertidos en nuevos pellets. Sufre ligera degradación térmica (*downcycling*).
3. **Reciclaje Terciario Químico (Solvólisis / Despolimerización):** Reacciones de glicólisis, hidrólisis o metanólisis que rompen los enlaces químicos para volver a los monómeros originales con calidad de resina virgen (*food-grade*, muy común en PET).
4. **Reciclaje Terciario Térmico (Pirólisis y Gasificación):** Descomposición a $>450^\circ\text{C}$ sin oxígeno para transformar mezclas complejas de poliolefinas en combustible líquido (aceite de pirólisis) o gas de síntesis.
5. **Reciclaje Terciario por Disolución Física (*Solvent-based*):** Proceso físico (ej. CreaSolv) donde un solvente selectivo disuelve un polímero específico de un empaque multicapa y lo precipita puro sin romper enlaces moleculares.
6. **Reciclaje Cuaternario (Valorización Energética / *Waste-to-Energy*):** Incineración controlada con recuperación de calor para generar vapor o electricidad. Aprovecha el alto poder calorífico de los plásticos ($\sim 40\text{ MJ/kg}$, similar al diésel).
7. **Reciclaje Orgánico / Biológico (Compostaje):** Biodegradación controlada por microorganismos para biopolímeros certificados (PLA, almidón) convirtiéndose en agua, $CO_2$ y abono orgánico.

### ❓ ¿Y qué pasa con los Termofijos?
Los termoestables **no se pueden reciclar mecánicamente por fusión**. Sus opciones de fin de ciclo son:
1. **Molienda mecánica:** Triturados en polvo ultrafino para usarse como carga inerte (*filler*) en asfalto, concreto o nuevas resinas.
2. **Quimiólisis selectiva:** Despolimerización química de resinas epoxi para recuperar fibras de carbono vírgenes de alto valor.
3. **Valorización energética:** Incineración controlada para recuperar energía térmica.
