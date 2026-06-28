#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador 3D Interactivo de Brazo Antropomórfico (3 GDL) - Versión Sede De la Patagonia
Optimizaciones de visualización y análisis de expansión térmica.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D

# --- Parámetros Físicos y de Diseño ---
L1_nominal = 10.0  # cm
L2_nominal = 10.0  # cm
ALPHA_AL = 23e-6   # Coeficiente expansión Aluminio (1/°C)
TEMP_DELTA = 0.0 # °C (Caso B: Expansión Térmica)

L1 = L1_nominal * (1 + ALPHA_AL * TEMP_DELTA)
L2 = L2_nominal * (1 + ALPHA_AL * TEMP_DELTA)

# Generar nube de puntos para el workspace
num_samples = 15
t1_range = np.linspace(-np.pi, np.pi, num_samples)
t2_range = np.linspace(-np.pi/2, np.pi/2, num_samples)
t3_range = np.linspace(-150 * np.pi / 180, 150 * np.pi / 180, num_samples)

T1, T2, T3 = np.meshgrid(t1_range, t2_range, t3_range)
X_w = (L1 * np.cos(T2) + L2 * np.cos(T2 + T3)) * np.cos(T1)
Y_w = (L1 * np.cos(T2) + L2 * np.cos(T2 + T3)) * np.sin(T1)
Z_w = L1 * np.sin(T2) + L2 * np.sin(T2 + T3)

x_w, y_w, z_w = X_w.flatten(), Y_w.flatten(), Z_w.flatten()

# --- Configuración Estética ---
USS_BLUE = '#00205B'
USS_GOLD = '#D4AF37'

plt.rcParams['text.color'] = 'black'
fig = plt.figure(figsize=(13, 9.5), facecolor='#ffffff')
fig.subplots_adjust(bottom=0.22, top=0.90, left=0.02, right=0.98)

ax = fig.add_subplot(111, projection='3d', facecolor='#ffffff')
ax.set_title("BRAZO ROBÓTICO 3D - USS SEDE DE LA PATAGONIA", 
             color=USS_BLUE, fontsize=14, fontweight='bold', pad=20)

# Perspectiva solicitada
ax.view_init(elev=30, azim=-60)

# Ocultar paneles y configurar cuadrícula
ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False
ax.grid(True, color='#e5e7eb', linestyle='--', alpha=0.6)

limit = 22
ax.set_xlim([-limit, limit]); ax.set_ylim([-limit, limit]); ax.set_zlim([-limit, limit])
ax.set_box_aspect([1, 1, 1])
ax.set_xlabel("X (cm)"); ax.set_ylabel("Y (cm)"); ax.set_zlabel("Z (cm)")

# Workspace con baja opacidad
ax.scatter(x_w, y_w, z_w, s=2.5, color=USS_BLUE, alpha=0.12)

# Eslabones y Articulaciones
line_l1, = ax.plot([], [], [], color=USS_BLUE, linewidth=6, label='Eslabón 1', zorder=5)
line_l2, = ax.plot([], [], [], color=USS_GOLD, linewidth=6, label='Eslabón 2', zorder=5)
joints, = ax.plot([], [], [], color='black', marker='o', markersize=7, linestyle='', zorder=6)
effector, = ax.plot([], [], [], color='#FFD700', marker='o', markersize=10, 
                    markeredgecolor=USS_BLUE, linestyle='', label='Efector Final', zorder=7)

# Cuadro de información (Movido a posición inferior para evitar solapamiento)
info_text = ax.text2D(0.02, 0.78, "", transform=ax.transAxes, verticalalignment='top', fontsize=10, 
                     fontname='monospace', fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8fafc', alpha=0.85, edgecolor=USS_BLUE, linewidth=1.5))

# Etiqueta dinámica con offset
effector_label = ax.text(0, 0, 0, "", color=USS_BLUE, fontsize=9, fontweight='bold', zorder=8)

def forward_kinematics(t1, t2, t3):
    t1, t2, t3 = np.radians([t1, t2, t3])
    x1 = L1 * np.cos(t2) * np.cos(t1)
    y1 = L1 * np.cos(t2) * np.sin(t1)
    z1 = L1 * np.sin(t2)
    x2 = (L1 * np.cos(t2) + L2 * np.cos(t2 + t3)) * np.cos(t1)
    y2 = (L1 * np.cos(t2) + L2 * np.cos(t2 + t3)) * np.sin(t1)
    z2 = L1 * np.sin(t2) + L2 * np.sin(t2 + t3)
    return (0.0, x1, x2), (0.0, y1, y2), (0.0, z1, z2)

def update(val):
    global L1, L2
    temp_delta = slider_temp.val
    L1 = L1_nominal * (1 + ALPHA_AL * temp_delta)
    L2 = L2_nominal * (1 + ALPHA_AL * temp_delta)
    
    t1, t2, t3 = slider_t1.val, slider_t2.val, slider_t3.val
    xs, ys, zs = forward_kinematics(t1, t2, t3)
    
    line_l1.set_data_3d(xs[:2], ys[:2], zs[:2])
    line_l2.set_data_3d(xs[1:], ys[1:], zs[1:])
    joints.set_data_3d(xs[:2], ys[:2], zs[:2])
    effector.set_data_3d([xs[2]], [ys[2]], [zs[2]])
    
    info_text.set_text(
        f"EFECTOR FINAL (P):\n"
        f"  X = {xs[2]:6.2f} cm\n"
        f"  Y = {ys[2]:6.2f} cm\n"
        f"  Z = {zs[2]:6.2f} cm"
    )
    
    effector_label.set_position_3d((xs[2]+1.5, ys[2]+1.5, zs[2]+1.5))
    effector_label.set_text(f"P({xs[2]:.1f}, {ys[2]:.1f}, {zs[2]:.1f})")
    fig.canvas.draw_idle()

# Controles
ax_t1 = fig.add_axes([0.15, 0.12, 0.3, 0.022]); slider_t1 = Slider(ax_t1, 'θ₁ Base', -180, 180, valinit=0, valfmt='%1.1f°', color=USS_BLUE)
ax_t2 = fig.add_axes([0.15, 0.08, 0.3, 0.022]); slider_t2 = Slider(ax_t2, 'θ₂ Hombro', -90, 90, valinit=30, valfmt='%1.1f°', color=USS_BLUE)
ax_t3 = fig.add_axes([0.15, 0.04, 0.3, 0.022]); slider_t3 = Slider(ax_t3, 'θ₃ Codo', -150, 150, valinit=45, valfmt='%1.1f°', color=USS_GOLD)

slider_t1.on_changed(update); slider_t2.on_changed(update); slider_t3.on_changed(update)

ax_temp = fig.add_axes([0.6, 0.08, 0.25, 0.022])
slider_temp = Slider(ax_temp, 'ΔT Temp (°C)', 0.0, 150.0, valinit=0.0, valfmt='%1.0f °C', color='#e74c3c')
slider_temp.on_changed(update)

ax_reset = fig.add_axes([0.8, 0.04, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Reset', color='#f1f5f9', hovercolor='#e2e8f0')
btn_reset.on_clicked(lambda e: [slider_t1.reset(), slider_t2.reset(), slider_t3.reset(), slider_temp.reset()])

# Añadir leyenda de elementos
ax.legend(loc='lower right', facecolor='#ffffff', edgecolor='#d1d5db', labelcolor='black', fontsize=8)

update(None)
plt.show()
