# -*- coding: utf-8 -*-
"""
Script refactorizado para ejecutar el análisis de impacto DiD utilizando
el módulo central de econometría y generando productos de "Investigación Anfibia".
"""

import os
import logging
import sys

# --- Configuración del Entorno ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Módulos del Proyecto ---
from src.utils import setup_run_environment
from src.core.econometrics import DiDAnalysis

def main():
    """
    Función principal para orquestar el análisis de Diferencias en Diferencias (DiD).
    Implementa el "Enfoque Anfibio" generando tanto un reporte técnico como visualizaciones.
    """
    # --- PASO 1: Configurar Entorno de Ejecución ---
    run_dir = setup_run_environment('reports/did_analysis')
    logging.info("Iniciando el análisis de Diferencias en Diferencias (DiD)...")

    # --- PASO 2: Inicializar el Análisis ---
    try:
        analyzer = DiDAnalysis(
            data_path='data/02_processed/deforestation_analysis_data.csv',
            treatment_unit='San Martin',
            treatment_year=2005
        )
        logging.info("Motor de análisis econométrico inicializado con éxito.")
    except FileNotFoundError:
        logging.error("No se encontró el dataset procesado. Abortando. Ejecuta 'python main.py data' primero.")
        return
    except Exception as e:
        logging.error(f"Error al inicializar el analizador: {e}")
        return

    # --- PASO 3: Ejecutar Modelos Econométricos ---
    logging.info("Ejecutando modelos DiD para corto y largo plazo...")
    did_short_term_results = analyzer.run_did_model(start_year=2005, end_year=2009)
    did_full_term_results = analyzer.run_did_model()

    # --- PASO 4: Generar Productos "Anfibios" ---

    # 4.1. Producto 1: Reporte Estadístico
    logging.info("Generando reporte estadístico técnico...")
    report_content = f"""
==============================================================================
    Resultados del Análisis de Diferencias en Diferencias (DiD)
==============================================================================

Análisis de Impacto de Corto Plazo (2005-2009)
----------------------------------------------
{did_short_term_results.summary()}

Interpretación:
El coeficiente 'did' representa el efecto causal estimado de la política.
- Efecto Estimado (Coef.): {did_short_term_results.params['did']:.4f} mil hectáreas.
- P-valor: {did_short_term_results.pvalues['did']:.4f}

Conclusión: El efecto {'es' if did_short_term_results.pvalues['did'] < 0.05 else 'no es'} estadísticamente significativo al 95% de confianza.

==============================================================================

Análisis de Impacto de Período Completo (1998-2023)
--------------------------------------------------
{did_full_term_results.summary()}

Interpretación:
- Efecto Estimado (Coef.): {did_full_term_results.params['did']:.4f} mil hectáreas.
- P-valor: {did_full_term_results.pvalues['did']:.4f}

Conclusión: El efecto {'es' if did_full_term_results.pvalues['did'] < 0.05 else 'no es'} estadísticamente significativo al 95% de confianza.
==============================================================================
"""
    report_path = os.path.join(run_dir, 'did_analysis_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    logging.info(f"Reporte técnico del análisis DiD guardado en: {report_path}")

    # 4.2. Producto 2: Visualizaciones de Impacto
    logging.info("Generando visualizaciones de impacto...")
    
    # Gráfico para el corto plazo
    plot_path_short = analyzer.plot_did_results(
        did_results=did_short_term_results,
        title='Impacto de Corto Plazo (2005-2009) en la Deforestación',
        run_dir=run_dir,
        filename='did_summary_short_term.png'
    )
    logging.info(f"Visualización de corto plazo guardada en: {plot_path_short}")

    # Gráfico para el período completo
    plot_path_full = analyzer.plot_did_results(
        did_results=did_full_term_results,
        title='Impacto de Período Completo (1998-2023) en la Deforestación',
        run_dir=run_dir,
        filename='did_summary_full_term.png'
    )
    logging.info(f"Visualización de período completo guardada en: {plot_path_full}")
    
    logging.info("Análisis de Diferencias en Diferencias completado exitosamente.")

if __name__ == '__main__':
    main()