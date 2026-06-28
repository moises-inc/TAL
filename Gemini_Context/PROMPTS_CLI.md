# Prompts para Gemini CLI — Hito Brazo Robótico 3D

> Estos prompts están diseñados para ser copiados y ejecutados secuencialmente en Gemini CLI. Cada uno es autocontenido y describe exactamente los cambios que debe realizar.

---

## PROMPT 1: Correcciones al Informe LaTeX (`Informe_Hito.tex`)

```
Actúa como un experto en maquetación LaTeX académica y robótica. Trabaja sobre el archivo:
<WORKSPACE_ROOT>/Gemini/Informe_Hito.tex

REGLA ESTRICTA: No usar cálculo infinitesimal (límites, derivadas, integrales). Solo álgebra y trigonometría.

Necesito que hagas las siguientes correcciones y mejoras AL INFORME. Compila con pdflatex al terminar.

### A. CORRECCIONES CRÍTICAS

1. En la portada, cambiar "Universidad San Sebastián --- Concepción" por "Universidad San Sebastián --- Sede De la Patagonia".

2. INSERTAR CITAS DENTRO DEL TEXTO según APA 7. Las referencias ya existen al final, pero no están citadas en el cuerpo. Ejemplo:
   - En la introducción, cuando se habla de robótica industrial, citar a Craig (2005): "La cinemática directa... (Craig, 2005)."
   - Cuando se habla de resistencia de materiales, citar a Hibbeler (2016).
   - Agregar al menos 2 referencias más que puedan citarse:
     * Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). Robot Modeling and Control. John Wiley & Sons.
     * Beer, F. P., Johnston, E. R., DeWolf, J. T., & Mazurek, D. F. (2020). Mecánica de materiales (8a ed.). McGraw-Hill.
   - Colocar citas narrativas o entre paréntesis en al menos 5 puntos del informe donde se usen conceptos de otros autores.

3. Cambiar el formato de las referencias al final del documento: actualmente usan \begin{enumerate}. Deben usar el formato APA 7 con sangría francesa (\hangindent). Reemplazar la sección de referencias por entradas con \noindent y \hangindent=1.27cm.

### B. SECCIONES FALTANTES SEGÚN LA RÚBRICA

Revisa esta estructura obligatoria (extraída del informe de ejemplo de nivel alto):
- Introducción > Planteamiento y Contextualización ✅
- Introducción > Objetivos ✅
- Metodología > **Metodología de trabajo** ❌ FALTA — Describir el PROCESO seguido (no teoría): cómo eligieron el problema, cómo obtuvieron información, decisiones relevantes, cómo construyeron el modelo.
- Metodología > Variables y parámetros ✅
- Metodología > Supuestos ✅
- Metodología > Construcción del modelo ✅
- Metodología > **Interpretación del modelo** ❌ FALTA — Explicar qué significa el modelo en el contexto: qué representa cada variable, qué implica la forma trigonométrica, qué significa r, x, y, z en el mundo real.
- Resultados > Resultados del modelo ✅
- Resultados > **Validación del modelo** ⚠️ INCOMPLETA — Actualmente solo valida los componentes mecánicos. Debe validar el MODELO CINEMÁTICO con al menos 2 criterios:
  * Coherencia: verificar que con theta_1=0, theta_2=0, theta_3=0 el brazo está extendido horizontalmente (x=20, y=0, z=0).
  * Análisis dimensional: verificar que las unidades son coherentes (cm + cm = cm).
  * Razonabilidad: el alcance máximo R_max = L1+L2 = 20 cm es coherente con un brazo de laboratorio.
- Resultados > Prueba de robustez ⚠️ Necesita más casos (ver punto C)
- Resultados > Limitaciones ⚠️ Necesita ampliarse (ver punto D)
- **Conclusión** ⚠️ INCOMPLETA — Falta reflexión sobre trabajo en equipo.

### C. AGREGAR MÁS PROBLEMAS Y CASOS DE PRESIÓN

Actualmente solo se analiza el caso de estrés a 140 km/h. Necesito:

1. **Pregunta adicional 1: Alcance efectivo vs configuración angular**
   "¿Cuál es el alcance radial horizontal máximo del brazo cuando el hombro está elevado a 45°?"
   Resolver: r_max(45°) = L1*cos(45°) + L2*cos(45°+0°) = 10*cos(45°) + 10*cos(45°) = 10*(√2/2) + 10*(√2/2) = 10√2 ≈ 14.14 cm
   Interpretar: al elevar el hombro, el alcance horizontal se reduce de 20 cm a 14.14 cm, un 29.3% menos.

2. **Pregunta adicional 2: Configuración singular**
   "¿Qué sucede con el espacio de trabajo cuando el codo se pliega completamente (theta_3 = 180°)?"
   Resolver: r = L1*cos(theta_2) + L2*cos(theta_2 + 180°) = L1*cos(theta_2) - L2*cos(theta_2) = 0 (porque L1=L2).
   Interpretar: el brazo se pliega sobre sí mismo, el efector queda en el origen. Esta es una singularidad cinemática.

3. **Caso de presión adicional: 80 km/h**
   Calcular tau a 80 km/h (v = 22.22 m/s, omega = 111.11 rad/s):
   T_codo = (0.5*0.15 + 0.5*0.20) * 111.11^2 ≈ 2160.49 N
   tau = 2160.49 / 7.068e-6 ≈ 305.7 MPa → FALLA (aún supera 150 MPa)

4. **Caso de presión adicional: 40 km/h**
   v = 11.11 m/s, omega = 55.56 rad/s:
   T_codo = (0.075 + 0.1) * 55.56^2 ≈ 540.12 N
   tau = 540.12 / 7.068e-6 ≈ 76.4 MPa → RESISTE (FS = 1.96)

Incluir estos 4 nuevos análisis en la sección de Resultados.

### D. AMPLIAR LIMITACIONES
Agregar las siguientes limitaciones:
- No se considera el peso propio de los eslabones bajo gravedad (momento flector).
- No se considera la fatiga por ciclos repetidos de carga.
- El modelo asume masas puntuales, no distribuidas.
- Se desprecia la vibración mecánica y los modos de resonancia.
- Las articulaciones se modelan como ideales (sin holguras ni juego mecánico).

### E. ESTILO VISUAL — REDUCIR COLORES
Siguiendo el estilo formal del informe de álgebra (Solemne 2), hacer estos cambios:
- Eliminar los \definecolor de USSGold y RedWarning del preámbulo (conservar solo USSBlue como color de acento).
- Quitar el \rowcolor{LightGray} de la tabla WOI.
- Cambiar el encabezado derecho de \textcolor{USSGold}{...} a \textcolor{USSBlue}{...} o simplemente texto negro.
- Los títulos de sección pueden mantener color USSBlue, pero eliminar la titlerule dorada.
- Usar interlineado 1.5 (\usepackage{setspace} \setstretch{1.5}).

Compila con: pdflatex -interaction=nonstopmode Informe_Hito.tex (2 veces para resolver referencias cruzadas).
```

---

## PROMPT 2: Mejorar la Imagen 3D del Workspace (`generate_plots.py`)

```
Actúa como un experto en visualización científica con Python/Matplotlib. Trabaja sobre:
<WORKSPACE_ROOT>/Gemini/generate_plots.py

PROBLEMA ACTUAL: En la función generate_workspace_3d(), la perspectiva del brazo robot genera una vista en la que los eslabones se ven prácticamente como una línea vertical recta. El ángulo de cámara no permite distinguir bien las dos partes del brazo.

SOLUCIÓN REQUERIDA:

1. Cambiar los ángulos de configuración del brazo de ejemplo para que ambos eslabones sean claramente visibles en perspectiva:
   - Usar theta_1 = 30° (en vez de 45°)
   - Usar theta_2 = 25° (en vez de 30°) 
   - Usar theta_3 = 70° (en vez de 60°)
   Esto da una configuración más abierta donde ambos eslabones se distinguen.

2. Cambiar el ángulo de cámara para una mejor perspectiva:
   - ax.view_init(elev=25, azim=135) en vez de (elev=20, azim=45)
   Esto permite ver el brazo desde un ángulo donde la articulación del codo es visible.

3. Mejorar la visibilidad de la nube de puntos del workspace:
   - Usar alpha=0.03 y s=0.8 para los scatter points
   - Usar un color más suave como '#A0C4FF' en vez de 'lightgray'

4. Agregar una línea punteada desde el origen al efector final para mostrar la distancia directa r. El código es:
   ax.plot([x0, x2], [y0, y2], [z0, z2], color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Distancia r')

5. Agregar etiquetas en las articulaciones. El código es:
   ax.text(x0, y0, z0, '  Base', fontsize=8, color='black')
   ax.text(x1, y1, z1, '  Codo', fontsize=8, color='black')
   ax.text(x2, y2, z2, '  Efector', fontsize=8, color='limegreen')

6. Regenerar también el stress_analysis.png con los nuevos casos de presión:
   - Agregar puntos marcados para 40 km/h (76.4 MPa, verde), 80 km/h (305.7 MPa, naranja), 140 km/h (936.17 MPa, rojo oscuro) y 200 km/h (~1910 MPa, rojo brillante).
   - Agregar anotaciones para cada punto.

Después de editar, ejecuta: python3 generate_plots.py
```

---

## PROMPT 3: Correcciones a la Presentación Beamer (`Presentacion_Hito.tex`)

```
Actúa como un experto en maquetación Beamer/LaTeX. Trabaja sobre:
<WORKSPACE_ROOT>/Gemini/Presentacion_Hito.tex

PROBLEMAS IDENTIFICADOS:
1. En la diapositiva 5 ("Espacio de Trabajo Factible"), la imagen workspace_3d.png se sale por abajo de la presentación y el texto de los items se corta. El "Simetría radial completa" queda fuera de pantalla.
2. La tabla WOI en diapositiva 3 genera un Overfull vbox.

CORRECCIONES REQUERIDAS:

A. DIAPOSITIVA 5 — Imagen del Workspace
Reemplazar el frame "Espacio de Trabajo Factible (3D)" completo. El nuevo frame debe:
- Usar \begin{columns}[T] (alineación top)
- Columna izquierda de 0.55\textwidth con la imagen limitada a: width=\linewidth,height=0.65\textheight,keepaspectratio
- Columna derecha de 0.42\textwidth con \small y items condensados:
  * "Nube de puntos: posiciones alcanzables."
  * "Colores USS (Azul/Dorado)."
  * "Simetría radial (360 grados)."
  * "R_max = 20 cm."
- Usar \setlength\itemsep{0.3em} para reducir separación entre items

B. DIAPOSITIVA DEL GRÁFICO DE ESFUERZO
En la diapositiva "Perfil de Esfuerzo Cortante vs Velocidad":
- Agregar [T] al entorno columns
- Agregar height=0.65\textheight,keepaspectratio a la imagen stress_analysis.png para que no se desborde

C. AGREGAR DIAPOSITIVA DE NUEVOS CASOS
Agregar una diapositiva nueva DESPUÉS de "Análisis de Estrés: Validación de Componentes" y ANTES de "Perfil de Esfuerzo Cortante vs Velocidad". El frame debe titularse "Análisis de Robustez: Casos Adicionales" y contener:
- Una tabla centrada con columnas: Velocidad | tau (MPa) | Límite (MPa) | Resultado
- Filas:
  * 40 km/h  | 76.4   | 150 | RESISTE (en color GreenSafe)
  * 80 km/h  | 305.7  | 150 | FALLA (en color RedWarning)
  * 140 km/h | 936.2  | 150 | FALLA CRÍTICA (en color RedWarning)
  * 200 km/h | 1910   | 150 | DESTRUCCIÓN (en color RedWarning)
- Debajo de la tabla, dos items:
  * "Velocidad máxima segura: aprox 55 km/h (tau menor a 150 MPa)."
  * "Rediseño mínimo: pasador de 8 mm de diámetro."

D. CORRECCIÓN DE SEDE
En la portada, si aparece "Concepción", cambiar por "Sede De la Patagonia".

Compila con: pdflatex -interaction=nonstopmode Presentacion_Hito.tex (2 veces).
```

---

## PROMPT 4: Mejorar el Simulador 3D (`simulador_3d.py`)

```
Actúa como experto en interfaces gráficas con Matplotlib en Python. Trabaja sobre:
<WORKSPACE_ROOT>/Gemini/simulador_3d.py

PROBLEMA ACTUAL: El panel de texto informativo ("POSICIÓN EFECTOR") se sobrepone con el título del simulador "SIMULADOR INTERACTIVO 3D...". Además, la etiqueta de posición en 3D del efector "P(11.2, 0.0, 14.7)" queda encima de los elementos del workspace y la leyenda.

SOLUCIÓN REQUERIDA:

A. Mover el panel de información para que NO se superponga con el título
Cambiar la posición del info_text de (0.02, 0.98) a (0.02, 0.78). Esto lo baja lo suficiente para que no tape el título.

B. Reducir el contenido del panel informativo
Eliminar los ángulos del panel (ya se ven en los sliders) y dejar solo las coordenadas del efector. El texto debe ser:
   "EFECTOR FINAL (P):\n  X = {valor} cm\n  Y = {valor} cm\n  Z = {valor} cm"

C. Mover la leyenda para que no se superponga con el panel
Cambiar ax.legend de loc='upper right' a loc='lower right' y reducir fontsize a 8.

D. Ajustar la etiqueta del efector en 3D para que no quede sobrepuesta
Agregar un offset de +1.5 en cada coordenada cuando se posiciona la etiqueta del efector:
   effector_label.set_position_3d((xs[2]+1.5, ys[2]+1.5, zs[2]+1.5))

E. Aumentar el tamaño de la ventana
Cambiar fig = plt.figure(figsize=(11, 8.5), ...) a figsize=(13, 9.5) para dar más espacio.

F. Ajustar la posición del subplot para evitar superposiciones
Cambiar fig.subplots_adjust a: bottom=0.22, top=0.90, left=0.02, right=0.98

No ejecutes el simulador (necesita display gráfico), solo guarda los cambios.
```

---

## PROMPT 5: Sincronización Final con Obsidian

```
Después de haber completado todos los cambios anteriores, ejecuta los siguientes comandos para sincronizar los archivos actualizados con la bóveda de Obsidian:

cd "<WORKSPACE_ROOT>/Gemini"

# Regenerar gráficos
python3 generate_plots.py

# Compilar documentos (2 pasadas para resolver referencias cruzadas)
pdflatex -interaction=nonstopmode Informe_Hito.tex
pdflatex -interaction=nonstopmode Informe_Hito.tex
pdflatex -interaction=nonstopmode Presentacion_Hito.tex
pdflatex -interaction=nonstopmode Presentacion_Hito.tex

# Copiar a Obsidian
cp -f simulador_3d.py generate_plots.py Informe_Hito.tex Informe_Hito.pdf Presentacion_Hito.tex Presentacion_Hito.pdf SYSTEM_PROMPT_WEB.md SYSTEM_PROMPT.md logo_uss.png workspace_3d.png stress_analysis.png "<OBSIDIAN_VAULT>/Universidad/USS/Ramos actuales/Taller Aptitudes Lógicas y Matemáticas/Gemini/"
cp -f Informe_Hito.pdf Presentacion_Hito.pdf "<OBSIDIAN_VAULT>/Universidad/USS/Ramos actuales/Taller Aptitudes Lógicas y Matemáticas/Evaluaciones/Solemnes/Hito/"
```

---

## Checklist de Verificación Post-Ejecución

Después de ejecutar todos los prompts, verifica:

- [ ] La portada dice "Sede De la Patagonia" (no "Concepción")
- [ ] Hay al menos 5 citas APA dentro del cuerpo del informe
- [ ] Las referencias al final usan formato APA 7 con sangría francesa
- [ ] Existe la sección "Metodología de trabajo" 
- [ ] Existe la sección "Interpretación del modelo"
- [ ] La validación del modelo incluye: coherencia, unidades y razonabilidad del modelo cinemático
- [ ] Se incluyen 4 preguntas/casos adicionales (alcance a 45°, singularidad, 80 km/h, 40 km/h)
- [ ] La conclusión incluye reflexión sobre trabajo en equipo
- [ ] El workspace_3d.png muestra el brazo desde una perspectiva donde se ven los dos eslabones claramente
- [ ] La diapositiva 5 NO se desborda
- [ ] El stress_analysis.png muestra puntos para 40, 80, 140 y 200 km/h
- [ ] El simulador no tiene textos superpuestos
- [ ] El informe usa interlineado 1.5 y diseño más formal (sin colores excesivos)
- [ ] Los archivos están sincronizados en Obsidian
