# -*- coding: utf-8 -*-
"""
Script para realizar el análisis de Estudio de Eventos, que descompone
el efecto DiD a lo largo del tiempo, antes y después de la intervención.
"""

import os
import logging
import sys
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# --- Configuración del Entorno ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Módulos del Proyecto ---
from src.utils import setup_run_environment
from src.core.econometrics import DiDAnalysis
from src.core.visualization_utils import style_event_study_plot

def main():
    """
    Función principal para orquestar el análisis de Estudio de Eventos.
    """
    # --- PASO 1: Configurar Entorno de Ejecución ---
    run_dir = setup_run_environment('reports/event_study_analysis')
    logging.info("Iniciando el análisis de Estudio de Eventos...")

    # --- PASO 2: Cargar Datos a través del Analizador ---
    try:
        analyzer = DiDAnalysis(
            data_path='data/02_processed/deforestation_analysis_data.csv',
            treatment_unit='San Martin',
            treatment_year=2005
        )
        df = analyzer.df
        logging.info("Datos cargados y preparados a través del motor econométrico.")
    except FileNotFoundError:
        logging.error("No se encontró el dataset procesado. Abortando. Ejecuta 'python main.py data' primero.")
        return

    # --- PASO 3: Preparar Variables para el Estudio de Eventos ---
    logging.info("Creando variables relativas al tiempo para el modelo...")
    treatment_year = analyzer.treatment_year
    df['tiempo_relativo'] = df['Periodo'] - treatment_year

    # Crear dummies para cada período de tiempo relativo, y limpiar sus nombres.
    event_dummies = pd.get_dummies(df['tiempo_relativo'], prefix='evento', drop_first=False)
    clean_colnames = {col: col.replace('-', 'm') for col in event_dummies.columns}
    event_dummies = event_dummies.rename(columns=clean_colnames)
    df = pd.concat([df, event_dummies], axis=1)
    
    # Definir el año base para la regresión ('evento_m1' es el nuevo nombre para t-1)
    base_period_dummy = 'evento_m1'
    if base_period_dummy not in df.columns:
        logging.error(f"El período base '{base_period_dummy}' no se encuentra en los datos. No se puede continuar.")
        return
        
    # Crear los términos de interacción: tratado * dummy_de_evento
    interaction_terms = []
    for col in event_dummies.columns:
        if col != base_period_dummy: # Excluir el año base de los términos de interacción
            interaction_term = f"I({col} * tratado)"
            interaction_terms.append(interaction_term)

    # --- PASO 4: Construir y Ejecutar el Modelo de Regresión ---
    logging.info("Construyendo y ejecutando el modelo de Estudio de Eventos...")
    formula = f"""
        deforestacion_anual ~ tratado + C(Periodo) + {' + '.join(interaction_terms)}
    """
    
    model = smf.ols(formula, data=df).fit()
    
    # --- PASO 5: Extraer y Guardar Resultados (Método Robusto) ---
    logging.info("Extrayendo coeficientes y generando reporte técnico...")
    results_summary = model.summary()

    # Lógica de selección explícita para evitar errores de .filter()
    all_coef_names = model.params.index.tolist()
    interaction_names = [name for name in all_coef_names if name.startswith('I(evento_')]

    coefficients_table = model.params.loc[interaction_names].reset_index()
    coefficients_table.columns = ['Termino', 'Coeficiente']
    coefficients_table['Tiempo Relativo'] = coefficients_table['Termino'].str.extract(r'evento_m(-?\d+)')
    coefficients_table['Tiempo Relativo'] = pd.to_numeric(coefficients_table['Tiempo Relativo'])

    conf_int = model.conf_int().loc[interaction_names].reset_index()
    conf_int.columns = ['Termino', 'CI_lower', 'CI_upper']

    results_df = pd.merge(coefficients_table, conf_int, on='Termino')

    # Añadir el punto base (t-1) con coeficiente 0
    base_point = pd.DataFrame({
        'Termino': ['evento_m1'], 'Coeficiente': [0],
        'Tiempo Relativo': [-1], 'CI_lower': [0], 'CI_upper': [0]
    })
    results_df = pd.concat([results_df, base_point], ignore_index=True).sort_values('Tiempo Relativo').reset_index(drop=True)
    
    report_path = os.path.join(run_dir, 'event_study_coefficients.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Resultados del Estudio de Eventos\n")
        f.write("===================================\n\n")
        f.write("Coeficientes para los términos de interacción (Efecto por año):\n")
        f.write(results_df[['Tiempo Relativo', 'Coeficiente', 'CI_lower', 'CI_upper']].to_string(index=False))
        f.write("\n\n")
        f.write("Resumen Completo del Modelo de Regresión:\n")
        f.write(str(results_summary))
    logging.info(f"Reporte técnico guardado en: {report_path}")

    # 5.2. Visualización
    logging.info("Generando gráfico del Estudio de Eventos...")
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.errorbar(results_df['Tiempo Relativo'], results_df['Coeficiente'], 
                yerr=[results_df['Coeficiente'] - results_df['CI_lower'], results_df['CI_upper'] - results_df['Coeficiente']],
                fmt='o', color='#005f73', ecolor='#48cae4', elinewidth=1, capsize=5, markersize=8, label='Coeficiente Estimado (β)')

    style_event_study_plot(ax, fig,
        title="Estudio de Eventos: Efecto Dinámico de la Política Fiscal",
        subtitle="Evolución del impacto en la deforestación antes y después de la intervención de 2005 (Año 0)",
        source_note="Elaboración propia. Las barras de error representan el intervalo de confianza del 95%."
    )
    
    plot_path = os.path.join(run_dir, 'event_study_plot.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    logging.info(f"Gráfico del Estudio de Eventos guardado en: {plot_path}")
    
    logging.info("Análisis de Estudio de Eventos completado.")

if __name__ == '__main__':
    main()