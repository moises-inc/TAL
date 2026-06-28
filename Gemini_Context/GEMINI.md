# Proyecto: Cinemática Directa de Brazo Robótico Planar 2D a Antropomórfico 3D (3 GDL)
**Asignatura:** Taller Aptitudes Lógicas y Matemáticas (TALM) - Desafío Matemático 2026

## 1. Contexto y Transición al Modelo 3D
Para el Hito Académico (Desafío Matemático), se ha decidido elevar la complejidad del brazo de un movimiento puramente planar (2D) a uno **antropomórfico espacial (3D)**.
Esto simula los primeros 3 grados de libertad (articulaciones principales) de un robot industrial real (como un KUKA o ABB).

### Parámetros Físicos de Diseño
*   $L_1 = 10\text{ cm}$ (Eslabón del brazo/Shoulder to Elbow).
*   $L_2 = 10\text{ cm}$ (Eslabón del antebrazo/Elbow to Wrist).
*   *Nota:* Se puede asumir una altura de la base de soporte $d_1 = 0\text{ cm}$ o $10\text{ cm}$ según conveniencia. Para simplicidad matemática inicial, usaremos $d_1 = 0\text{ cm}$ (articulación del hombro en el origen $Z=0$).

### Variables Articulares (Rango de Movimiento)
1.  **$\theta_1$ (Rotación de la Base / Cintura):** Giro en torno al eje vertical $Z$ (Rango: $-180^\circ$ a $180^\circ$). Controla la orientación (guiñada/yaw) en el plano horizontal $XY$.
2.  **$\theta_2$ (Rotación del Hombro):** Elevación respecto al plano horizontal (Rango: $-90^\circ$ a $90^\circ$ o $-45^\circ$ a $135^\circ$).
3.  **$\theta_3$ (Rotación del Codo):** Ángulo relativo al primer eslabón $L_1$ (Rango: $-150^\circ$ a $150^\circ$).

---

## 2. Modelo Matemático en 3D (Trigonometría Pura)
La transición del plano 2D al espacio 3D se resuelve proyectando geométricamente el movimiento del brazo vertical sobre el plano horizontal mediante coordenadas esféricas-cilíndricas.

Sea $r$ la proyección en el plano horizontal $XY$ de la distancia total desde el origen al efector final:
$$r = L_1 \cdot \cos(\theta_2) + L_2 \cdot \cos(\theta_2 + \theta_3)$$

Las coordenadas espaciales cartesianas $(x, y, z)$ del efector final son:
$$x = r \cdot \cos(\theta_1) = \left( L_1 \cdot \cos(\theta_2) + L_2 \cdot \cos(\theta_2 + \theta_3) \right) \cos(\theta_1)$$
$$y = r \cdot \sin(\theta_1) = \left( L_1 \cdot \cos(\theta_2) + L_2 \cdot \cos(\theta_2 + \theta_3) \right) \sin(\theta_1)$$
$$z = L_1 \cdot \sin(\theta_2) + L_2 \cdot \sin(\theta_2 + \theta_3)$$

*Este modelo cumple estrictamente con el principio de utilizar solo trigonometría elemental (descomposición vectorial y sumas angulares), eliminando cualquier cálculo diferencial.*

---

## 3. Planificación del Proyecto (Carta Gantt)
Esta planificación abarca desde la constitución del equipo hasta el cierre del semestre.

| ID | Actividad / Tarea | Responsable(s) | Fecha Inicio | Fecha Fin | Entregable / Hito Relacionado | Estado |
|:---|:---|:---|:---|:---|:---|:---|
| **T1** | Definición del Equipo y Tema inicial | Grupo Completo | 27/05/2026 | 27/05/2026 | Constitución y Acta inicial | completado |
| **T2** | Elaboración de la Carta Gantt y Estructura | Grupo Completo | 28/05/2026 | 30/05/2026 | Planificación inicial del proyecto | completado |
| **T3** | Formulación Matemática del Modelo 3D y WOI | Grupo Completo | 29/05/2026 | 02/06/2026 | Definición de variables y ecuaciones | completado |
| **T4** | **Evaluación Grupal #2 (Hito)** | Grupo Completo | 03/06/2026 | 03/06/2026 | Entrega escrita de problema y modelo | completado |
| **T5** | Rediseño y Programación del Simulador 3D (Python) | Programadores | 04/06/2026 | 08/06/2026 | Código funcional del simulador en 3D | completado |
| **T6** | Estructuración del Borrador del Informe (LaTeX) | Editores LaTeX | 04/06/2026 | 09/06/2026 | PDF borrador basado en plantilla USS | completado |
| **T7** | **Presentación Voluntaria y Feedback** | Presentadores | 10/06/2026 | 10/06/2026 | Exposición para corrección de detalles | completado |
| **T8** | Pruebas de Presión, Robustez y Análisis Gráfico | Analistas | 11/06/2026 | 14/06/2026 | Gráficos integrados en el informe | Pendiente |
| **T9** | Revisión Final y Corrección de Estilo (Rúbrica) | Grupo Completo | 15/06/2026 | 16/06/2026 | Documento definitivo USS listo | Pendiente |
| **T10**| **Presentaciones Obligatorias y Entrega de Informe** | Grupo Completo | 17/06/2026 | 17/06/2026 | Nota de Presentación e Informe (100%) | Pendiente |
| **T11**| Preparación y Aplicación del Post-Test / Examen | Grupo Completo | 18/06/2026 | 24/06/2026 | Evaluación individual conceptual | Pendiente |
| **T12**| Revisión de Calificaciones y Cierre de Semestre | Grupo Completo | 25/06/2026 | 01/07/2026 | Acta de notas final | Pendiente |

---

## 4. Registro del WOI (Variables y Parámetros para Hito #2)

| Tipo de Variable | Símbolo | Significado Físico | Unidad (SI/Métrico) | Tipo de Dato |
|:---|:---:|:---|:---|:---|
| **Independiente (Entrada)** | $\theta_1$ | Ángulo azimutal de la base (Yaw) | Grados ($^\circ$) o Radianes ($\text{rad}$) | Real continuo |
| **Independiente (Entrada)** | $\theta_2$ | Ángulo de elevación del hombro (Pitch) | Grados ($^\circ$) o Radianes ($\text{rad}$) | Real continuo |
| **Independiente (Entrada)** | $\theta_3$ | Ángulo de flexión del codo (Pitch relativo) | Grados ($^\circ$) o Radianes ($\text{rad}$) | Real continuo |
| **Dependiente (Salida)** | $x$ | Posición cartesiana lateral en eje X | Centímetros ($\text{cm}$) | Real continuo |
| **Dependiente (Salida)** | $y$ | Posición cartesiana de profundidad en eje Y| Centímetros ($\text{cm}$) | Real continuo |
| **Dependiente (Salida)** | $z$ | Posición cartesiana de altura en eje Z | Centímetros ($\text{cm}$) | Real continuo |
| **Parámetro (Diseño)** | $L_1$ | Longitud del brazo (Hombro a Codo) | Centímetros ($\text{cm}$) | Constante ($10.0$) |
| **Parámetro (Diseño)** | $L_2$ | Longitud del antebrazo (Codo a Muñeca) | Centímetros ($\text{cm}$) | Constante ($10.0$) |

---

## 5. Preguntas Clave para el Docente (Sesión del Viernes/Feedback)
1.  *¿Es adecuado justificar la robustez del modelo 3D analizando la sensibilidad del radio horizontal $r$ ante cambios en $\theta_2$ y $\theta_3$, manteniendo $\theta_1$ fijo, para simplificar el análisis sin perder rigurosidad tridimensional?*
2.  *¿Para la sección de "Limitaciones", el hecho de omitir el volumen físico (grosor) de los eslabones es aceptable bajo el supuesto de "brazo lineal infinitamente delgado"?*
3.  *¿El formato de la Carta Gantt en el informe impreso final debe ser un gráfico visual de barras de tiempo o la tabla estructurada con dependencias de tareas es suficiente y preferible?*
