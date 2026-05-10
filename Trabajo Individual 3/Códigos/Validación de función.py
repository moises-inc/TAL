import matplotlib.pyplot as plt
import numpy as np

# --- 1. PARÁMETROS DEL MODELO ---
L1 = 10
L2 = 10

# Límites físicos de los servomotores (Rango de operación en grados)
# Esto simula las restricciones mecánicas reales del hardware.
LIMITE_THETA1 = (-180, 180)  # La base da una vuelta completa
LIMITE_THETA2 = (-150, 150)  # El codo no puede plegarse completamente sobre el brazo 1

def calcular_cinematica(theta1_deg, theta2_deg):
    """Calcula las coordenadas finales y valida los límites físicos."""
    
    # Validación de seguridad: Comprueba que los ángulos estén dentro del rango
    if not (LIMITE_THETA1[0] <= theta1_deg <= LIMITE_THETA1[1]):
        raise ValueError(f"CRÍTICO: Ángulo base theta1 ({theta1_deg}°) fuera del rango permitido {LIMITE_THETA1}.")
        
    if not (LIMITE_THETA2[0] <= theta2_deg <= LIMITE_THETA2[1]):
        raise ValueError(f"CRÍTICO: Ángulo codo theta2 ({theta2_deg}°) fuera del rango permitido {LIMITE_THETA2}.")

    # Conversión a radianes para las funciones trigonométricas de numpy
    theta1 = np.radians(theta1_deg)
    theta2 = np.radians(theta2_deg)

    # Deducción algebraica (Posición de la articulación del codo)
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    
    # Deducción algebraica (Posición de la herramienta)
    x_final = x1 + L2 * np.cos(theta1 + theta2)
    y_final = y1 + L2 * np.sin(theta1 + theta2)

    return (x1, y1), (x_final, y_final)

def ejecutar_movimiento(theta1_deg, theta2_deg):
    """Ejecuta el cálculo, imprime los datos y genera la gráfica del movimiento."""
    print("-" * 50)
    print(f"Iniciando secuencia de movimiento: θ1 = {theta1_deg}°, θ2 = {theta2_deg}°")
    
    try:
        # Llamamos a la función de cálculo. Si hay error, saltará al bloque 'except'
        (x1, y1), (x_final, y_final) = calcular_cinematica(theta1_deg, theta2_deg)
        
        print(f"✅ Movimiento exitoso.")
        print(f"   Posición del Codo: ({x1:.2f}, {y1:.2f}) cm")
        print(f"   Posición de la Herramienta: ({x_final:.2f}, {y_final:.2f}) cm")
        
        # --- GRAFICACIÓN ---
        fig, ax = plt.subplots(figsize=(7, 7))
        
        # Dibujar área de alcance máximo
        radio_max = L1 + L2
        area = plt.Circle((0, 0), radio_max, color='lightgreen', alpha=0.15, label='Área de Alcance Seguro')
        ax.add_patch(area)
        
        # Trazar el brazo
        ax.plot([0, x1, x_final], [0, y1, y_final], 'ko-', linewidth=6, markersize=10, label='Brazo Robótico')
        
        # Resaltar la herramienta final
        ax.plot(x_final, y_final, 'ro', markersize=12, label=f'Herramienta ({x_final:.1f}, {y_final:.1f})')
        
        # Configurar aspecto visual
        ax.set_xlim(-22, 22)
        ax.set_ylim(-22, 22)
        ax.set_aspect('equal')
        ax.axhline(0, color='black', linewidth=1, linestyle='--')
        ax.axvline(0, color='black', linewidth=1, linestyle='--')
        ax.set_title(rf"Validación de Posición | $\theta_1={theta1_deg}^\circ$, $\theta_2={theta2_deg}^\circ$", fontsize=14)
        ax.set_xlabel("Eje X (cm)")
        ax.set_ylabel("Eje Y (cm)")
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.legend(loc='upper right')
        
        # Mostrar gráfica
        plt.show()
        
    except ValueError as error:
        # Si la función calcular_cinematica lanza un ValueError, lo capturamos aquí
        print(f"❌ ERROR DEL SISTEMA: {error}")
        print("   -> Movimiento abortado por protocolo de seguridad.")


# ==========================================
#        ZONA DE EJECUCIÓN Y PRUEBAS
# ==========================================

# 1. Probamos el Punto A (Reposo)
ejecutar_movimiento(0, 0)

# 2. Probamos el Punto B (Acción)
ejecutar_movimiento(90, -90)

# 3. Probamos un punto arbitrario (Ejemplo: Brazo recogido hacia atrás)
ejecutar_movimiento(135, 45)

# 4. FORZAMOS UN ERROR MECÁNICO (Codo plegado en 160°, excede el límite de 150°)
ejecutar_movimiento(45, 160)