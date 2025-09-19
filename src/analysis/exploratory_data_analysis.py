# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import logging
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment

def style_chart(ax, fig, title, subtitle, xlabel, source_note):
    """Aplica un estilo consistente y profesional a un gráfico."""
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
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])
    fig.text(0.05, 0.01, source_note, ha='left', fontsize=9, color='gray')

def main():
    """Genera los gráficos del Análisis Exploratorio de Datos (EDA)."""
    run_dir = setup_run_environment('reports/figures/eda')
    logging.info("Iniciando la generación de gráficos del EDA...")

    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
        logging.info("Datos procesados cargados para el EDA.")
    except FileNotFoundError:
        logging.error("No se encontró el archivo procesado. Ejecuta 'python main.py data' primero.")
        return

    departamentos = df['departamento'].unique()
    for dep in departamentos:
        fig, ax = plt.subplots(figsize=(12, 7))
        dep_data = df[df['departamento'] == dep]
        
        style_chart(ax, fig, 
                    title=f'Evolución de la Deforestación en {dep}',
                    subtitle=f'Período {dep_data["Periodo"].min()}-{dep_data["Periodo"].max()}',
                    xlabel='Año',
                    source_note='Fuente: Datos de MapBiomas Perú (Procesado). Elaboración propia.')
        
        ax.plot(dep_data['Periodo'], dep_data['deforestacion_anual'], marker='o', linestyle='-', color='#005f73')
        ax.axvline(x=2005, color='#E63946', linestyle=':', linewidth=2, label='Intervención Ley 2005')
        ax.legend(loc='upper left', frameon=False)

        output_path = os.path.join(run_dir, f'deforestacion_{dep.replace(" ", "_")}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

    logging.info("Gráficos individuales generados.")

    # Gráfico comparativo
    fig_comp, ax_comp = plt.subplots(figsize=(14, 8))
    style_chart(ax_comp, fig_comp, 
                title='Comparativo de Deforestación Anual por Departamento',
                subtitle=f'Período {df["Periodo"].min()}-{df["Periodo"].max()}',
                xlabel='Año',
                source_note='Fuente: Datos de MapBiomas Perú (Procesado). Elaboración propia.')

    colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(departamentos)))

    for i, dep in enumerate(departamentos):
        dep_data = df[df['departamento'] == dep]
        ax_comp.plot(dep_data['Periodo'], dep_data['deforestacion_anual'], marker='o', markersize=4, linestyle='-', label=dep, color=colors[i], alpha=0.8)

    ax_comp.axvline(x=2005, color='#E63946', linestyle=':', linewidth=2, label='Intervención Ley 2005')
    ax_comp.legend(loc='upper left', frameon=False, title='Departamentos')

    comp_path = os.path.join(run_dir, 'deforestacion_comparativo_total.png')
    plt.savefig(comp_path, dpi=300, bbox_inches='tight')
    plt.close(fig_comp)
    logging.info("Gráfico comparativo generado.")
    logging.info("Generación de gráficos del EDA completada.")

if __name__ == '__main__':
    main()