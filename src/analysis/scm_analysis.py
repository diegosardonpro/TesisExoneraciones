# -*- coding: utf-8 -*-
"""
Script para realizar el análisis de Método de Control Sintético (SCM),
la validación econométrica final del impacto de la política fiscal.

NOTA: La sección de visualización ha sido comentada debido a 
incompatibilidades insuperables con la versión de la librería `pysyncon`.
El script genera el reporte técnico, pero no los gráficos.
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
    run_dir, logger = setup_run_environment('reports/scm_analysis')
    logger.info("Iniciando el análisis de Método de Control Sintético (SCM)...")

    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
        logger.info("Datos procesados cargados.")
    except FileNotFoundError:
        logger.error("No se encontró el dataset procesado. Abortando. Ejecuta 'python main.py data' primero.")
        return

    logger.info("Preparando datos para el formato SCM...")
    df_for_scm = df.rename(columns={
        'Periodo': 'time',
        'departamento': 'unit',
        'deforestacion_anual': 'deforestation_anual'
    })

    logger.info("Configurando el Dataprep para el control sintético...")
    dataprep = Dataprep(
        foo=df_for_scm,
        predictors=['deforestation_anual'],
        dependent='deforestation_anual',
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
    
    logger.info("Generando reporte técnico con los pesos del control sintético...")
    weights_table = synth.weights(round=4).to_string()
    summary_table = synth.summary(round=4).to_string()
    
    report_content = f"""Resultados del Análisis SCM...\n{weights_table}\n{summary_table}"""
    report_path = os.path.join(run_dir, 'scm_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    logger.info(f"Reporte técnico del SCM guardado en: {report_path}")

    # --- SECCIÓN DE VISUALIZACIÓN DESACTIVADA ---
    logger.warning("La generación de gráficos SCM ha sido desactivada debido a incompatibilidades con la librería.")

    logging.info("Análisis de Control Sintético completado (sin visualizaciones).")

if __name__ == '__main__':
    main()