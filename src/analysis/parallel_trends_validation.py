# -*- coding: utf-8 -*-
"""
Script refactorizado para validar el supuesto de tendencias paralelas.
Admite un año de intervención dinámico para análisis de sensibilidad.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment

try:
    import statsmodels.formula.api as smf
except ImportError:
    logging.error("La librería 'statsmodels' no está instalada. Por favor, instálala manualmente con 'pip install statsmodels'.")
    sys.exit(1)

def main(year=2005):
    """Orquesta la validación de tendencias paralelas para un año de intervención dado."""
    # Directorio de salida dinámico para el análisis de sensibilidad
    output_dir = os.path.join('reports', 'pruebas_sensibilidad_año', str(year), 'validation')
    run_dir, _ = setup_run_environment(output_dir)
    
    logging.info(f"Iniciando la validación de tendencias paralelas para el año de intervención {year}...")

    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
    except FileNotFoundError:
        logging.error("Abortando. Ejecuta 'python main.py data' primero.")
        return

    df['tratado'] = (df['departamento'] == 'San Martin').astype(int)
    # Usar el año de intervención pasado como parámetro
    pre_intervention_df = df[df['Periodo'] < year].copy()

    if pre_intervention_df.empty:
        logging.warning(f"No hay datos pre-intervención para el año {year}. Saltando validación.")
        return

    logging.info("Generando gráfico de validación visual...")
    avg_trends = pre_intervention_df.groupby(['Periodo', 'tratado'])['deforestacion_anual'].mean().unstack()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle(f'Validación de Tendencias Paralelas (Intervención: {year})', fontsize=18, fontweight='bold')
    ax.set_title(f'Evolución de la Deforestación Promedio ({pre_intervention_df.Periodo.min()}-{pre_intervention_df.Periodo.max()})', fontsize=12, fontstyle='italic', pad=20)
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

    logging.info("Realizando prueba estadística...")
    pre_intervention_df['año_norm'] = pre_intervention_df['Periodo'] - pre_intervention_df['Periodo'].min()
    model = smf.ols('deforestacion_anual ~ tratado + año_norm + tratado:año_norm', data=pre_intervention_df).fit()
    
    report_table = f"""
==============================================================================
         Prueba Estadística de Tendencias Paralelas (Intervención: {year})
         Período de Prueba: {pre_intervention_df.Periodo.min()}-{pre_intervention_df.Periodo.max()}
==============================================================================
Variable Dependiente: deforestacion_anual

{model.summary()}
==============================================================================

Interpretación:
El supuesto de tendencias paralelas requiere que el coeficiente del término de
interacción ('tratado:año_norm') NO sea estadísticamente significativo.

- Coeficiente de Interacción: {model.params['tratado:año_norm']:.4f}
- P-valor de Interacción: {model.pvalues['tratado:año_norm']:.4f}

Un p-valor > 0.05 sugiere que no podemos rechazar la hipótesis nula de que las
tendencias son paralelas, lo cual valida nuestro supuesto para el análisis DiD.
==============================================================================
"""
    
    table_path = os.path.join(run_dir, 'parallel_trends_statistical_validation.txt')
    with open(table_path, 'w', encoding='utf-8') as f:
        f.write(report_table)
    logging.info(f"Resultados de la validación estadística guardados en: {table_path}")
    
    logging.info(f"Validación de tendencias paralelas para el año {year} completada.")

if __name__ == '__main__':
    # Permite la ejecución directa del script con un año por defecto
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2005)
    args = parser.parse_args()
    main(year=args.year)
