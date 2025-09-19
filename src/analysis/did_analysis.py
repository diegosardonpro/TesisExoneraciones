# -*- coding: utf-8 -*-
"""
Script refactorizado para ejecutar el análisis de impacto DiD utilizando
el módulo central de econometría.
"""

import os
import logging
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment
from src.core.econometrics import DiDAnalysis

def main():
    """Función principal para orquestar el análisis DiD."""
    run_dir = setup_run_environment('reports/did_analysis')
    logging.info("Iniciando el análisis de Diferencias en Diferencias (DiD)...")

    try:
        analyzer = DiDAnalysis(
            data_path='data/02_processed/deforestation_analysis_data.csv',
            treatment_group='San Martin',
            control_group=['Amazonas', 'Loreto', 'Ucayali'],
            treatment_year=2005
        )
    except FileNotFoundError:
        logging.error("Abortando. Ejecuta 'python main.py data' primero.")
        return

    # --- PASO 2: Ejecutar modelos para diferentes períodos ---
    did_short_term = analyzer.run_did_model(start_year=2005, end_year=2009)
    did_full_term = analyzer.run_did_model() 

    # --- PASO 3: Generar y guardar reporte ---
    report_content = f"""
==============================================================================
    Resultados del Análisis de Diferencias en Diferencias (DiD)
==============================================================================

Análisis de Impacto de Corto Plazo (2005-2009)
----------------------------------------------
{did_short_term['summary']}

Interpretación:
El coeficiente 'did' representa el efecto causal estimado de la política.
- Efecto Estimado (Coef.): {did_short_term['coef_did']:.4f} mil hectáreas.
- P-valor: {did_short_term['p_value_did']:.4f}

Conclusión: El efecto {'es' if did_short_term['p_value_did'] < 0.05 else 'no es'} estadísticamente significativo al 95% de confianza.

==============================================================================

Análisis de Impacto de Período Completo (1998-2023)
--------------------------------------------------
{did_full_term['summary']}

Interpretación:
- Efecto Estimado (Coef.): {did_full_term['coef_did']:.4f} mil hectáreas.
- P-valor: {did_full_term['p_value_did']:.4f}

Conclusión: El efecto {'es' if did_full_term['p_value_did'] < 0.05 else 'no es'} estadísticamente significativo al 95% de confianza.
==============================================================================
"""
    output_path = os.path.join(run_dir, 'did_analysis_report.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    logging.info(f"Reporte del análisis DiD guardado en: {output_path}")

if __name__ == '__main__':
    main()
