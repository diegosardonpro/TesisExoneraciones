# -*- coding: utf-8 -*-
"""
Script para realizar el análisis de Método de Control Sintético (SCM),
la validación econométrica final del impacto de la política fiscal.
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

# --- Módulos del Proyecto y Dependencias Externas ---
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
    # --- PASO 1: Configurar Entorno de Ejecución ---
    run_dir, logger = setup_run_environment('reports/scm_analysis')
    logger.info("Iniciando el análisis de Método de Control Sintético (SCM)...")

    # --- PASO 2: Cargar y Preparar Datos ---
    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
        logger.info("Datos procesados cargados.")
    except FileNotFoundError:
        logger.error("No se encontró el dataset procesado. Abortando. Ejecuta 'python main.py data' primero.")
        return

    # --- PASO 3: Preparar Datos para PySyncon ---
    logger.info("Preparando datos para el formato SCM...")
    
    # Renombramos las columnas para que coincidan con la terminología de PySyncon
    df_for_scm = df.rename(columns={
        'Periodo': 'time',
        'departamento': 'unit'
    })

    # --- PASO 4: Configurar y Ejecutar el Optimizador de Control Sintético ---
    logger.info("Configurando el Dataprep para el control sintético...")
    
    dataprep = Dataprep(
        foo=df_for_scm,
        predictors=['deforestacion_anual'], # CORREGIDO
        dependent='deforestacion_anual',   # CORREGIDO
        unit_variable='unit',
        time_variable='time',
        treatment_identifier='San Martin',
        controls_identifier=['Amazonas', 'Loreto', 'Ucayali', 'Madre de Dios'],
        time_predictors_prior=[1998, 2004],
        time_optimize_ssr=[1998, 2004],
        predictors_op="mean"
    )

    logger.info("Buscando los pesos óptimos para el control sintético...")
    synth = Synth()
    synth.fit(dataprep=dataprep)
    
    # --- PASO 5: Generar Productos "Anfibios" ---
    logger.info("Generando reporte y visualizaciones...")
    
    # 5.1. Reporte Técnico
    weights_table = synth.weights(round=4).to_string()
    summary_table = synth.summary(round=4).to_string()
    report_content = f"""Resultados del Análisis SCM...\n{weights_table}\n{summary_table}"""
    report_path = os.path.join(run_dir, 'scm_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    logger.info(f"Reporte técnico del SCM guardado en: {report_path}")

    # 5.2. Visualización de Impacto
    plt.figure(figsize=(14, 8))
    synth.path_plot()
    fig, ax = plt.gcf(), plt.gca()
    style_scm_plot(ax, fig,
        title="Validación con Control Sintético: Real vs. Contrafactual",
        subtitle="Comparación de la deforestación observada en San Martín con su 'gemelo' sintético",
        source_note="Elaboración propia."
    )
    plot_path = os.path.join(run_dir, 'scm_path_plot.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"Gráfico de trayectoria guardado en: {plot_path}")

    plt.figure(figsize=(14, 8))
    synth.gaps_plot()
    fig_gaps, ax_gaps = plt.gcf(), plt.gca()
    ax_gaps.set_ylabel('Diferencia en Deforestación (Real - Sintético)')
    style_scm_plot(ax_gaps, fig_gaps,
        title="Efecto Causal Estimado a lo Largo del Tiempo (SCM)",
        subtitle="Diferencia en la deforestación anual entre San Martín y su control sintético",
        source_note="Elaboración propia."
    )
    plot_path_gaps = os.path.join(run_dir, 'scm_gaps_plot.png')
    plt.savefig(plot_path_gaps, dpi=300, bbox_inches='tight')
    plt.close(fig_gaps)
    logger.info(f"Gráfico de diferencias (gaps) guardado en: {plot_path_gaps}")

    logging.info("Análisis de Control Sintético completado.")

if __name__ == '__main__':
    main()
