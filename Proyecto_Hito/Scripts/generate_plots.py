import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Configuración de colores institucionales USS
USS_BLUE = '#00205B'
USS_GOLD = '#D4AF37'

def generate_workspace_3d():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Parámetros
    L1 = 10.0
    L2 = 10.0
    
    # Generar nube de puntos para el workspace
    theta1 = np.linspace(-180, 180, 20)
    theta2 = np.linspace(-90, 90, 20)
    theta3 = np.linspace(-150, 150, 20)
    
    T1, T2, T3 = np.meshgrid(np.radians(theta1), np.radians(theta2), np.radians(theta3))
    
    R_proj = L1 * np.cos(T2) + L2 * np.cos(T2 + T3)
    X = R_proj * np.cos(T1)
    Y = R_proj * np.sin(T1)
    Z = L1 * np.sin(T2) + L2 * np.sin(T2 + T3)
    
    ax.scatter(X, Y, Z, color='#2F80ED', alpha=0.15, s=2.0, label='Espacio de Trabajo')
    
    # Dibujar robot en configuración de ejemplo: theta1=30, theta2=25, theta3=70
    t1, t2, t3 = np.radians([30, 25, 70])
    
    x0, y0, z0 = 0, 0, 0
    x1 = L1 * np.cos(t2) * np.cos(t1)
    y1 = L1 * np.cos(t2) * np.sin(t1)
    z1 = L1 * np.sin(t2)
    
    r_total = L1 * np.cos(t2) + L2 * np.cos(t2 + t3)
    x2 = r_total * np.cos(t1)
    y2 = r_total * np.sin(t1)
    z2 = L1 * np.sin(t2) + L2 * np.sin(t2 + t3)
    
    # Eslabón 1 (Azul USS)
    ax.plot([x0, x1], [y0, y1], [z0, z1], color=USS_BLUE, linewidth=5, label='Eslabón 1 (Brazo)')
    # Eslabón 2 (Dorado USS)
    ax.plot([x1, x2], [y1, y2], [z1, z2], color=USS_GOLD, linewidth=5, label='Eslabón 2 (Antebrazo)')
    
    # Línea de distancia r
    ax.plot([x0, x2], [y0, y2], [z0, z0], color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Proyección radial r')
    
    # Articulaciones
    ax.scatter([x0, x1], [y0, y1], [z0, z1], color='black', s=50, zorder=5)
    ax.scatter([x2], [y2], [z2], color='limegreen', s=100, label='Efector Final', zorder=5)
    
    # Etiquetas en articulaciones
    ax.text(x0, y0, z0, '  Base', fontsize=8, color='black')
    ax.text(x1, y1, z1, '  Codo', fontsize=8, color='black')
    ax.text(x2, y2, z2, '  Efector', fontsize=8, color='limegreen')
    
    # Configuración de ejes
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    ax.set_title('Espacio de Trabajo y Configuración del Brazo Robótico 3D', pad=20)
    
    # Limpiar fondo
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True, linestyle='--', alpha=0.3)
    
    ax.legend(loc='upper right', fontsize=8)
    ax.view_init(elev=25, azim=135)
    
    plt.savefig('workspace_3d.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("workspace_3d.png generado.")

def generate_stress_analysis():
    # Parámetros físicos
    R = 0.2  # m (20 cm)
    r2 = 0.15 # m
    r3 = 0.20 # m
    m2 = 0.5  # kg
    M_load = 0.5 # kg
    d_pin = 0.003 # m (3 mm)
    A_pin = np.pi/4 * d_pin**2
    
    v_kmh = np.linspace(0, 210, 300)
    v_ms = v_kmh / 3.6
    omega = v_ms / R
    
    # Tensión en el codo (centrífuga del eslabón 2 y la carga)
    T_codo = (m2 * r2 + M_load * r3) * omega**2
    
    # Esfuerzo cortante en MPa
    tau_mpa = (T_codo / A_pin) / 1e6
    
    plt.figure(figsize=(10, 6))
    plt.plot(v_kmh, tau_mpa, color=USS_BLUE, linewidth=2, label='Esfuerzo Cortante (Calculado)')
    
    # Línea de falla
    tau_limit = 150
    plt.axhline(y=tau_limit, color='red', linestyle='--', label='Límite de Cizalla Admisible (150 MPa)')
    
    # Casos de presión
    casos = [
        (40, 'green', 'Resiste', 76.4),
        (80, 'orange', 'Falla', 305.6),
        (140, 'darkred', 'Falla Crítica', 936.0),
        (200, 'red', 'Destrucción', 1910.3)
    ]
    
    for v, color, msg, expected_tau in casos:
        # Calcular tau real para el gráfico
        v_ms_c = v / 3.6
        omega_c = v_ms_c / R
        T_c = (m2 * r2 + M_load * r3) * omega_c**2
        tau_c = (T_c / A_pin) / 1e6
        
        plt.scatter([v], [tau_c], color=color, s=80, zorder=5)
        plt.annotate(f'{v} km/h\n({expected_tau:.1f} MPa)\n{msg}', 
                     xy=(v, tau_c), xytext=(v-15, tau_c+150),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=4),
                     fontsize=8, fontweight='bold', ha='center')
    
    plt.fill_between(v_kmh, tau_mpa, tau_limit, where=(tau_mpa > tau_limit), color='red', alpha=0.1, label='Zona de Falla')
    
    plt.xlabel('Velocidad Lineal del Efector (km/h)')
    plt.ylabel('Esfuerzo Cortante en Pasador $\\tau$ (MPa)')
    plt.title('Análisis de Estrés Físico: Esfuerzo en el Pasador del Codo vs. Velocidad')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.ylim(0, 2200)
    
    plt.savefig('stress_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("stress_analysis.png generado.")

if __name__ == "__main__":
    generate_workspace_3d()
    generate_stress_analysis()
