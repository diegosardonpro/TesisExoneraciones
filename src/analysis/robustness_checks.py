# -*- coding: utf-8 -*-
"""
Script para realizar pruebas de robustez, incluyendo pruebas de placebo,
para validar la solidez de los resultados del análisis DiD.
"""
import os
import logging
import sys
import pandas as pd
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment
from src.core.econometrics import DiDAnalysis

def run_placebo_test(analyzer, placebo_year, run_dir):
    """
    Ejecuta una prueba de placebo para un año específico.

    Args:
        analyzer (DiDAnalysis): Una instancia de la clase de análisis.
        placebo_year (int): El año falso para simular la intervención.
        run_dir (str): El directorio para guardar los resultados.
    """
    logging.info(f"--- Ejecutando Prueba de Placebo para el año {placebo_year} ---")
    
    # Modificar temporalmente el año de tratamiento en una copia del dataframe
    placebo_df = analyzer.df.copy()
    placebo_df['post_treatment'] = (placebo_df['Periodo'] >= placebo_year).astype(int)
    placebo_df['did'] = placebo_df['post_treatment'] * placebo_df['tratado']

    try:
        import statsmodels.formula.api as smf
        model = smf.ols('deforestacion_anual ~ tratado + post_treatment + did', data=placebo_df).fit()
        
        coef_did = model.params['did']
        p_value_did = model.pvalues['did']
        
        logging.info(f"Placebo {placebo_year}: Coeficiente DiD = {coef_did:.4f}, P-valor = {p_value_did:.4f}")
        return {'year': placebo_year, 'coef': coef_did, 'p_value': p_value_did}

    except Exception as e:
        logging.error(f"Fallo la prueba de placebo para el año {placebo_year}: {e}")
        return None

def main():
    """Función principal para orquestar las pruebas de robustez."""
    run_dir, _ = setup_run_environment('reports/robustness_checks')
    logging.info("Iniciando pruebas de robustez...")

    try:
        analyzer = DiDAnalysis(
            data_path='data/02_processed/deforestation_analysis_data.csv',
            treatment_unit='San Martin',
            treatment_year=2005 # El año real de la intervención
        )
    except FileNotFoundError:
        logging.error("Abortando. Ejecuta 'python main.py data' primero.")
        return

    # Años pre-intervención para las pruebas de placebo
    placebo_years = [year for year in range(1999, 2005)]
    placebo_results = []

    for year in placebo_years:
        result = run_placebo_test(analyzer, year, run_dir)
        if result:
            placebo_results.append(result)

    # --- Generar reporte y gráfico de las pruebas de placebo ---
    if placebo_results:
        df_placebo = pd.DataFrame(placebo_results)
        
        # Guardar resultados en un archivo de texto
        report_path = os.path.join(run_dir, 'placebo_tests_summary.txt')
        with open(report_path, 'w') as f:
            f.write("Resultados de las Pruebas de Placebo\n")
            f.write("=======================================\n")
            f.write("Un modelo robusto no debería mostrar efectos significativos en años placebo.\n\n")
            f.write(df_placebo.to_string(index=False))
        logging.info(f"Reporte de placebo guardado en {report_path}")

        # Generar gráfico
        fig, ax = plt.subplots(figsize=(12, 7))
        fig.suptitle('Resultados de las Pruebas de Placebo', fontsize=16, fontweight='bold')
        ax.set_title('Coeficientes DiD para Años de Intervención Falsos', fontsize=12, fontstyle='italic')
        ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
        
        # Colorear por significancia
        colors = ['red' if p < 0.05 else 'gray' for p in df_placebo['p_value']]
        
        ax.bar(df_placebo['year'], df_placebo['coef'], color=colors, alpha=0.7)
        ax.set_xlabel('Año de Placebo')
        ax.set_ylabel('Coeficiente DiD Estimado')
        ax.grid(axis='y', linestyle=':', alpha=0.5)

        plot_path = os.path.join(run_dir, 'placebo_coefficients_plot.png')
        plt.savefig(plot_path, dpi=300)
        plt.close(fig)
        logging.info(f"Gráfico de placebo guardado en {plot_path}")

    logging.info("Pruebas de robustez completadas.")

if __name__ == '__main__':
    main()