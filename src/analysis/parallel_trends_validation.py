# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os

try:
    import statsmodels.formula.api as smf
except ImportError:
    print("La librería 'statsmodels' no está instalada. Se intentará instalar ahora.")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "statsmodels"])
        import statsmodels.formula.api as smf
        print("'statsmodels' se ha instalado correctamente.")
    except Exception as e:
        print(f"No se pudo instalar 'statsmodels'. Por favor, instálala manualmente con 'pip install statsmodels'. Error: {e}")
        exit()

# --- PASO 1: Cargar datos procesados ---
print("Iniciando la validación de tendencias paralelas con datos procesados...")
try:
    df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo de datos procesados. Ejecuta primero 'src/data/make_dataset.py'.")
    exit()

# --- PASO 2: Preparar datos para la validación ---
# Definir grupo de tratamiento y control
df['tratado'] = (df['departamento'] == 'San Martin').astype(int)

# Filtrar por el período pre-intervención
pre_intervention_df = df[df['Periodo'] <= 2004].copy()

# --- PASO 3: Validación Visual ---
print("Generando gráfico de validación visual...")
avg_trends = pre_intervention_df.groupby(['Periodo', 'tratado'])['deforestacion_anual'].mean().unstack()

fig, ax = plt.subplots(figsize=(12, 8))

# Estilo del gráfico
fig.suptitle('Validación del Supuesto de Tendencias Paralelas', fontsize=18, fontweight='bold')
ax.set_title('Evolución de la Deforestación Promedio (1998-2004)', fontsize=12, fontstyle='italic', pad=20)
ax.set_xlabel('Año')
ax.set_ylabel('Deforestación Anual Promedio (miles de ha)')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Graficar tendencias
ax.plot(avg_trends.index, avg_trends[0], marker='o', linestyle='-', label='Grupo de Control (Promedio)')
ax.plot(avg_trends.index, avg_trends[1], marker='o', linestyle='-', label='Grupo de Tratamiento (San Martín)')

ax.legend(title='Grupos')
fig.tight_layout(rect=[0, 0.05, 1, 0.9])

# Guardar gráfico
output_dir = 'reports/validation'
plot_path = os.path.join(output_dir, 'parallel_trends_visual_validation.png')
plt.savefig(plot_path, dpi=300)
print(f"Gráfico de validación guardado en: {plot_path}")
plt.close(fig)


# --- PASO 4: Validación Estadística ---
print("Realizando prueba estadística de tendencias paralelas...")

# Crear una variable para la tendencia temporal
pre_intervention_df['año_norm'] = pre_intervention_df['Periodo'] - pre_intervention_df['Periodo'].min()

# Modelo de regresión con término de interacción
# La variable clave es la interacción: tratado:año_norm
model = smf.ols('deforestacion_anual ~ tratado + año_norm + tratado:año_norm', data=pre_intervention_df).fit()

# Extraer el resumen del modelo
results_summary = model.summary()

# Formatear la tabla de resultados para el reporte
p_value_interaction = model.pvalues['tratado:año_norm']
coef_interaction = model.params['tratado:año_norm']

report_table = f"""
==============================================================================
         Prueba Estadística de Tendencias Paralelas (1998-2004)
==============================================================================
Variable Dependiente: deforestacion_anual

{results_summary}
==============================================================================

Interpretación:
El supuesto de tendencias paralelas requiere que el coeficiente del término de
interacción ('tratado:año_norm') NO sea estadísticamente significativo.

- Coeficiente de Interacción: {coef_interaction:.4f}
- P-valor de Interacción: {p_value_interaction:.4f}

Un p-valor > 0.05 sugiere que no podemos rechazar la hipótesis de que las
tendencias son paralelas, lo cual validaría nuestro supuesto para el análisis DiD.
==============================================================================
"""

# Guardar resultados estadísticos
table_path = os.path.join(output_dir, 'parallel_trends_statistical_validation.txt')
with open(table_path, 'w', encoding='utf-8') as f:
    f.write(report_table)

print(f"Resultados de la validación estadística guardados en: {table_path}")
print("\nValidación de tendencias paralelas completada.")
