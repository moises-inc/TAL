import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.patches import Wedge, Circle

# Configuración visual profesional
plt.style.use('seaborn-v0_8-whitegrid')

# Parámetros del modelo (Los mismos de tu presentación)
L1 = 10
L2 = 10

# Inicializar figura y ajustar márgenes para hacer espacio a los controles
fig, ax = plt.subplots(figsize=(9, 8))
plt.subplots_adjust(bottom=0.25) 

# Dibujar área de alcance máximo físico (R=20)
area = Circle((0, 0), L1 + L2, color='lightgreen', alpha=0.15, label='Área Segura (Alcance Físico)')
ax.add_patch(area)

# Inicializar los elementos gráficos vacíos (se actualizarán dinámicamente)
line_brazo, = ax.plot([], [], 'ko-', linewidth=6, markersize=10, label='Eslabones')
punto_herramienta, = ax.plot([], [], 'ro', markersize=12, label='Herramienta')
cuñas = [] # Lista para almacenar y refrescar las áreas de los ángulos

def actualizar_grafico(val):
    """Función que recalcula la cinemática cada vez que mueves un slider."""
    # Obtener valores actuales de los sliders
    th1_deg = slider_th1.val
    th2_deg = slider_th2.val
    
    # Conversión a radianes para los cálculos trigonométricos
    th1 = np.radians(th1_deg)
    th2 = np.radians(th2_deg)
    
    # Deducción matemática de las coordenadas
    x1, y1 = L1 * np.cos(th1), L1 * np.sin(th1)
    x2, y2 = x1 + L2 * np.cos(th1 + th2), y1 + L2 * np.sin(th1 + th2)
    
    # Actualizar líneas del brazo
    line_brazo.set_data([0, x1, x2], [0, y1, y2])
    punto_herramienta.set_data([x2], [y2])
    
    # --- ACTUALIZACIÓN DE ÁREAS DE ÁNGULOS ---
    # Limpiar las cuñas anteriores del gráfico
    for c in cuñas:
        c.remove()
    cuñas.clear()
    
    # Crear nuevas áreas sombreadas
    # Theta 1: Desde 0° hasta th1_deg
    c1 = Wedge((0, 0), 3, min(0, th1_deg), max(0, th1_deg), color='blue', alpha=0.25)
    # Theta 2: Desde la línea del brazo 1 (th1_deg) hasta la posición final (th1_deg + th2_deg)
    c2 = Wedge((x1, y1), 3, min(th1_deg, th1_deg + th2_deg), max(th1_deg, th1_deg + th2_deg), color='red', alpha=0.25)
    
    ax.add_patch(c1)
    ax.add_patch(c2)
    cuñas.extend([c1, c2])
    
    # Actualizar el título dinámicamente usando raw f-strings
    ax.set_title(rf"Simulador Matemático en Tiempo Real | $\theta_1={th1_deg:.0f}^\circ$, $\theta_2={th2_deg:.0f}^\circ$" + "\n" + f"Coordenada Actual: ({x2:.1f}, {y2:.1f}) cm", fontsize=14)
    
    # Refrescar lienzo
    fig.canvas.draw_idle()

# Configurar límites y estética de los Ejes
ax.set_xlim(-22, 22)
ax.set_ylim(-22, 22)
ax.set_aspect('equal')
ax.axhline(0, color='black', linewidth=1, linestyle='--')
ax.axvline(0, color='black', linewidth=1, linestyle='--')
ax.set_xlabel("Eje X (cm)")
ax.set_ylabel("Eje Y (cm)")
ax.legend(loc='upper right')

# --- CREACIÓN DE LOS CONTROLES INTERACTIVOS (SLIDERS) ---
ax_th1 = plt.axes([0.15, 0.1, 0.65, 0.03])
ax_th2 = plt.axes([0.15, 0.05, 0.65, 0.03])

# Limitamos los sliders a los rangos de operación mecánicos
slider_th1 = Slider(ax_th1, r'$\theta_1$ (Base)', -180, 180, valinit=45, valstep=1, color='blue')
slider_th2 = Slider(ax_th2, r'$\theta_2$ (Codo)', -150, 150, valinit=-30, valstep=1, color='red')

# Conectar los sliders a la función de actualización
slider_th1.on_changed(actualizar_grafico)
slider_th2.on_changed(actualizar_grafico)

# Forzar el primer cálculo para que no inicie en blanco
actualizar_grafico(0)

print("Iniciando Simulador Interactivo...")
plt.show()