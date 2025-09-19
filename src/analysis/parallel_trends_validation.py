# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import sys

# Añadir el directorio raíz del proyecto al sys.path
# Esto asegura que podamos importar 'src' como un módulo.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment

try:
    import statsmodels.formula.api as smf
except ImportError:
    logging.error("La librería 'statsmodels' no está instalada. Por favor, instálala manualmente con 'pip install statsmodels'.")
    sys.exit(1)

def main():
    """
    Script principal para validar el supuesto de tendencias paralelas.
    """
    # --- PASO 0: Configurar entorno de ejecución ---
    run_dir = setup_run_environment('reports/validation')
    logging.info("Iniciando la validación de tendencias paralelas con datos procesados...")

    # --- PASO 1: Cargar datos procesados ---
    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
        logging.info("Datos procesados cargados exitosamente.")
    except FileNotFoundError:
        logging.error("No se encontró el archivo de datos procesados. Ejecuta primero 'src/data/make_dataset.py'.")
        return

    # --- PASO 2: Preparar datos para la validación ---
    logging.info("Preparando datos para la validación...")
    df['tratado'] = (df['departamento'] == 'San Martin').astype(int)
    pre_intervention_df = df[df['Periodo'] <= 2004].copy()

    # --- PASO 3: Validación Visual ---
    logging.info("Generando gráfico de validación visual...")
    avg_trends = pre_intervention_df.groupby(['Periodo', 'tratado'])['deforestacion_anual'].mean().unstack()
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('Validación del Supuesto de Tendencias Paralelas', fontsize=18, fontweight='bold')
    ax.set_title('Evolución de la Deforestación Promedio (1998-2004)', fontsize=12, fontstyle='italic', pad=20)
    ax.set_xlabel('Año')
    ax.set_ylabel('Deforestación Anual Promedio (miles de ha)')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.plot(avg_trends.index, avg_trends[0], marker='o', linestyle='-', label='Grupo de Control (Promedio)')
    ax.plot(avg_trends.index, avg_trends[1], marker='o', linestyle='-', label='Grupo de Tratamiento (San Martín)')
    ax.legend(title='Grupos')
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])
    
    plot_path = os.path.join(run_dir, 'parallel_trends_visual_validation.png')
    plt.savefig(plot_path, dpi=300)
    logging.info(f"Gráfico de validación guardado en: {plot_path}")
    plt.close(fig)

    # --- PASO 4: Validación Estadística ---
    logging.info("Realizando prueba estadística de tendencias paralelas...")
    pre_intervention_df['año_norm'] = pre_intervention_df['Periodo'] - pre_intervention_df['Periodo'].min()
    model = smf.ols('deforestacion_anual ~ tratado + año_norm + tratado:año_norm', data=pre_intervention_df).fit()
    results_summary = model.summary()
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
    
    table_path = os.path.join(run_dir, 'parallel_trends_statistical_validation.txt')
    with open(table_path, 'w', encoding='utf-8') as f:
        f.write(report_table)
    logging.info(f"Resultados de la validación estadística guardados en: {table_path}")
    
    logging.info("Validación de tendencias paralelas completada.")

if __name__ == '__main__':
    main()
