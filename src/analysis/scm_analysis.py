# -*- coding: utf-8 -*-
"""
Script final para el análisis de Método de Control Sintético (SCM).
Esta versión sintetiza todas las correcciones y depuraciones realizadas.
"""
import os
import logging
import sys
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuración del Entorno ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment
from src.core.visualization_utils import style_scm_plot

try:
    from pysyncon import Dataprep, Synth
except ImportError:
    logging.error("La librería 'pysyncon' no está instalada. Por favor, instálala con 'pip install pysyncon'.")
    sys.exit(1)

def main():
    """
    Función principal para orquestar el análisis de Control Sintético.
    """
    run_dir, logger = setup_run_environment('reports/scm_analysis')
    logger.info("Iniciando el análisis de Método de Control Sintético (SCM)...")

    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
        logger.info("Datos procesados cargados.")
    except FileNotFoundError:
        logger.error("No se encontró el dataset procesado. Abortando. Ejecuta 'python main.py data' primero.")
        return

    # --- Lógica de Preparación de Datos Definitiva ---
    logger.info("Preparando datos para el formato SCM con predictores explícitos...")
    df_wide = df.pivot_table(index='departamento', columns='Periodo', values='deforestacion_anual')
    predictors_years = [2002, 2003, 2004]
    for year in predictors_years:
        df[f"defo_{year}"] = df['departamento'].map(df_wide[year])
    df_for_scm = df.rename(columns={'Periodo': 'time', 'departamento': 'unit'})
    
    # --- Llamada a Dataprep Definitiva (con todas las correcciones) ---
    logger.info("Configurando el Dataprep para el control sintético...")
    predictor_names = [f"defo_{year}" for year in predictors_years]
    dataprep = Dataprep(
        foo=df_for_scm,
        predictors=predictor_names,
        dependent='deforestacion_anual', # CORREGIDO
        unit_variable='unit',
        time_variable='time',
        treatment_identifier='San Martin',
        controls_identifier=['Amazonas', 'Loreto', 'Ucayali', 'Madre de Dios'],
        time_predictors_prior=predictors_years,
        time_optimize_ssr=[1998, 2004],
        predictors_op="mean"
    )

    logger.info("Buscando los pesos óptimos para el control sintético...")
    synth = Synth()
    synth.fit(dataprep=dataprep)
    
    # --- Generación de Reporte y Visualización Definitiva ---
    logger.info("Generando reporte y visualizaciones finales...")
    
    # Reporte Técnico
    weights_table = synth.weights(round=4).to_string()
    summary_table = synth.summary(round=4).to_string()
    report_content = f"""Resultados del Análisis SCM...\n{weights_table}\n{summary_table}"""
    report_path = os.path.join(run_dir, 'scm_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    logger.info(f"Reporte técnico del SCM guardado en: {report_path}")

    # Visualización Manual Robusta
    real_path = synth.dataprep.foo[synth.dataprep.foo['unit'] == synth.dataprep.treatment_identifier].set_index('time')['deforestacion_anual'] # CORREGIDO
    synth_path = synth._synthetic()
    gaps = synth._gaps()

    # Gráfico de Trayectorias
    fig_path, ax_path = plt.subplots(figsize=(14, 8))
    ax_path.plot(real_path.index, real_path, label="San Martín (Real)", color='#E63946', linewidth=2)
    ax_path.plot(synth_path.index, synth_path, label="San Martín (Sintético)", color='#457B9D', linestyle='--', linewidth=2)
    min_val, max_val = min(real_path.min(), synth_path.min()), max(real_path.max(), synth_path.max())
    margin = (max_val - min_val) * 0.1
    ax_path.set_ylim(min_val - margin, max_val + margin)
    style_scm_plot(ax_path, fig_path, title="Validación con Control Sintético", subtitle="Comparación de deforestación observada vs. contrafactual sintético", source_note="Elaboración propia.")
    output_path_path = os.path.join(run_dir, 'scm_path_plot.png')
    plt.savefig(output_path_path, dpi=300, bbox_inches='tight')
    plt.close(fig_path)
    logger.info(f"Gráfico de trayectoria guardado en: {output_path_path}")

    # Gráfico de Diferencias (Gaps)
    fig_gaps, ax_gaps = plt.subplots(figsize=(14, 8))
    ax_gaps.plot(gaps.index, gaps, label="Diferencia (Real - Sintético)", color='#1D3557')
    ax_gaps.axhline(0, color='black', linestyle='--', linewidth=1.0, alpha=0.8)
    ax_gaps.fill_between(gaps.index, gaps, 0, where=gaps > 0, facecolor='#A8DADC', interpolate=True, alpha=0.5)
    ax_gaps.fill_between(gaps.index, gaps, 0, where=gaps <= 0, facecolor='#F1FAEE', interpolate=True, alpha=0.5)
    ax_gaps.set_ylabel('Diferencia en Deforestación (Real - Sintético)')
    style_scm_plot(ax_gaps, fig_gaps, title="Efecto Causal Estimado a lo Largo del Tiempo (SCM)", subtitle="Diferencia en la deforestación anual entre San Martín y su control sintético", source_note="Elaboración propia.")
    output_path_gaps = os.path.join(run_dir, 'scm_gaps_plot.png')
    plt.savefig(output_path_gaps, dpi=300, bbox_inches='tight')
    plt.close(fig_gaps)
    logger.info(f"Gráfico de diferencias (gaps) guardado en: {output_path_gaps}")

    logging.info("Análisis de Control Sintético completado.")

if __name__ == '__main__':
    main()
