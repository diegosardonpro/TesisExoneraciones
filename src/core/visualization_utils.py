# -*- coding: utf-8 -*-
"""
Módulo centralizado para la creación y estilización de visualizaciones
bajo la filosofía de "Investigación Anfibia".
"""
import matplotlib.pyplot as plt
import pandas as pd

def style_plot(ax, fig, title, subtitle, source_note):
    """
    Aplica un estilo base y profesional a un gráfico de Matplotlib.
    Función genérica para gráficos exploratorios y descriptivos.
    """
    fig.suptitle(title, fontsize=18, fontweight='bold', ha='center')
    ax.set_title(subtitle, fontsize=12, fontstyle='italic', pad=20, loc='center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_visible(False)
    ax.yaxis.grid(True, color='#EEEEEE', linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', colors='gray', rotation=45)
    ax.tick_params(axis='y', length=0, colors='gray')
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])
    fig.text(0.05, 0.01, source_note, ha='left', fontsize=9, color='gray')

def plot_did_results(results_data, title, subtitle, output_path):
    """
    Crea y guarda un gráfico de barras estilizado para los resultados del DiD.
    """
    for period, data in results_data.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        
        coef = data['coef_did']
        p_value = data['p_value_did']
        conf_int = data['summary'].tables[1].data[-1][5:7]
        ci_lower, ci_upper = map(float, conf_int)
        error = coef - ci_lower

        significant = p_value < 0.05
        color = '#E63946' if significant else 'grey'
        
        ax.barh(['Efecto Estimado (DiD)'], [coef], xerr=error, color=color, alpha=0.8, capsize=5)
        
        style_plot(ax, fig,
            title=f"Resultado del Análisis DiD: {period}",
            subtitle=subtitle,
            source_note="Elaboración propia. La barra de error representa el intervalo de confianza del 95%."
        )
        ax.set_xlabel("Impacto en la Deforestación Anual (miles de hectáreas)")
        
        # Añadir texto con el valor del coeficiente y p-valor
        conclusion = f"Coeficiente: {coef:.2f}\nP-valor: {p_value:.3f}\n{'Estadísticamente Significativo' if significant else 'No Significativo'}"
        ax.text(0.95, 0.95, conclusion, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5))

        # Guardar la figura
        period_filename = period.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')
        period_output_path = output_path.replace('.png', f'_{period_filename}.png')
        plt.savefig(period_output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

def style_event_study_plot(ax, fig, title, subtitle, source_note):
    """
    Aplica un estilo específico para gráficos de Estudio de Eventos.
    """
    # Títulos y subtítulos
    fig.suptitle(title, fontsize=18, fontweight='bold', ha='center')
    ax.set_title(subtitle, fontsize=12, fontstyle='italic', pad=20, loc='center')

    # Líneas de referencia clave
    ax.axhline(0, color='black', linestyle='--', linewidth=1.0, alpha=0.8)
    ax.axvline(-0.5, color='#E63946', linestyle=':', linewidth=2, label='Intervención (Año 2005)')

    # Estilo de ejes y rejilla
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, color='#EEEEEE', linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel('Años Relativos a la Intervención', fontsize=12, labelpad=15, color='gray')
    ax.set_ylabel('Coeficiente Estimado del Impacto (β)', fontsize=12, labelpad=15, color='gray')
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')

    # Leyenda y notas
    ax.legend(loc='upper left', frameon=False)
    fig.text(0.05, 0.01, source_note, ha='left', fontsize=9, color='gray')
    
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])