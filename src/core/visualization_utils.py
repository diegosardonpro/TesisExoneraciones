# -*- coding: utf-8 -*-
"""
Módulo centralizado para funciones de visualización.
Asegura un estilo consistente en todos los gráficos del proyecto.
"""
import matplotlib.pyplot as plt

def style_plot(fig, ax, title, subtitle, xlabel, ylabel, source_note):
    """
    Aplica un estilo consistente y profesional a un gráfico de Matplotlib.
    """
    fig.suptitle(title, fontsize=18, fontweight='bold', ha='center')
    if subtitle:
        ax.set_title(subtitle, fontsize=12, fontstyle='italic', pad=20, loc='center')
    
    # Ocultar bordes innecesarios
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_visible(False)

    # Configuración de ejes
    ax.set_xlabel(xlabel, fontsize=12, labelpad=15, color='gray')
    ax.set_ylabel(ylabel, fontsize=12, labelpad=15, color='gray')

    # Grid y ticks
    ax.grid(axis='y', color='#EEEEEE', linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', colors='gray', rotation=45)
    ax.tick_params(axis='y', length=0, colors='gray')

    # Nota de fuente
    fig.text(0.05, 0.01, source_note, ha='left', fontsize=9, color='gray')

    # Ajuste final
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])
