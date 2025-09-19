# -*- coding: utf-8 -*-
"""
Script para realizar un análisis rápido de "prueba de humo" para validar si 
existe una "señal" en los datos que justifique un análisis más profundo.
Este script ahora lee desde los datos procesados para mantener la consistencia.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import sys

# Añadir el directorio raíz del proyecto al sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment

def style_chart(ax, fig, title, subtitle, xlabel, source_note):
    """Aplica un estilo consistente y profesional a un gráfico de Matplotlib."""
    fig.suptitle(title, fontsize=18, fontweight='bold', ha='center')
    ax.set_title(subtitle, fontsize=12, fontstyle='italic', pad=20, loc='center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_visible(False)
    ax.set_xlabel(xlabel, fontsize=12, labelpad=15, color='gray')
    ax.yaxis.grid(True, color='#EEEEEE', linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', colors='gray', rotation=45)
    ax.tick_params(axis='y', length=0, colors='gray')
    ax.set_ylabel('Deforestación Anual (miles de hectáreas)', fontsize=12, color='gray')
    fig.text(0.05, 0.01, source_note, ha='left', fontsize=9, color='gray')
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])

def main():
    """Función principal para orquestar la prueba de humo."""
    run_dir = setup_run_environment('reports/figures/smoke_test')
    logging.info("Iniciando la prueba de humo con datos procesados...")

    # --- PASO 1: Cargar los datos desde la carpeta de datos PROCESADOS ---
    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
        logging.info("Datos procesados cargados para la prueba de humo.")
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo de datos procesados. Ejecuta 'src/data/make_dataset.py' primero.")
        return

    # --- PASO 2: Preparar los grupos de Tratamiento y Control ---
    logging.info("Preparando grupos de tratamiento y control...")
    tratamiento_dep = 'San Martin'
    control_deps = ['Amazonas', 'Loreto', 'Ucayali']

    df_tratamiento = df[df['departamento'] == tratamiento_dep].copy()
    df_control_group = df[df['departamento'].isin(control_deps)]

    control_avg = df_control_group.groupby('Periodo')['deforestacion_anual'].mean().reset_index()

    # --- PASO 3: Generar el Gráfico de Divergencia ---
    logging.info("Generando gráfico de divergencia...")
    fig, ax = plt.subplots(figsize=(14, 8))

    style_chart(ax, fig, 
                title='Prueba de Humo: ¿Divergen las Tendencias de Deforestación?',
                subtitle='Comparación de la deforestación anual en San Martín vs. el promedio de otros departamentos amazónicos (1998-2023)',
                xlabel='Año',
                source_note='Fuente: Datos de MapBiomas Perú (Procesado). Elaboración propia.')

    ax.plot(df_tratamiento['Periodo'], df_tratamiento['deforestacion_anual'], marker='o', linestyle='-', label='San Martín (Tratamiento)', color='#E63946', zorder=10)
    ax.plot(control_avg['Periodo'], control_avg['deforestacion_anual'], marker='s', linestyle='--', label='Promedio Control (Amazonas, Loreto, Ucayali)', color='#457B9D')
    ax.axvline(x=2005, color='#333333', linestyle=':', linewidth=2, label='Ley N° 28575 (Exclusión de San Martín)')

    ax.legend(loc='upper left', frameon=False)

    output_path = os.path.join(run_dir, 'smoke_test_divergence_plot.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logging.info(f"Gráfico de la prueba de humo guardado en: {output_path}")
    plt.close(fig)

    logging.info("Prueba de humo completada.")

if __name__ == '__main__':
    main()