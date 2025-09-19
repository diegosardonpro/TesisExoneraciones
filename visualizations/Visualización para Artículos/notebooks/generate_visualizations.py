
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Añadir la carpeta 'src' al path para poder importar las utilidades
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from plotting_utils import style_chart, add_value_labels

def create_concentration_chart(data_path, output_path):
    """Genera el gráfico de distribución de afiliados."""
    df = pd.read_csv(data_path)
    df = df.sort_values(by='% de Afiliados', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 10))

    # Colores: destacar Lima y Callao
    colors = ['#003366' if x >= 5.5 else '#6CA0DC' if x > 1.0 else '#D9E2EC' for x in df['% de Afiliados']]

    bars = ax.barh(df['Departamento'], df['% de Afiliados'], color=colors, height=0.7)

    style_chart(
        ax=ax, fig=fig,
        title='Distribución de Afiliados al SPP por Departamento',
        subtitle='El 58.3% de los afiliados se concentra en Lima y Callao, evidenciando un sistema centralista.',
        xlabel='Porcentaje del Total Nacional de Afiliados (%)',
        source_note='Fuente: Elaboración propia en base a datos de la SBS (Est. Dic 2023).'
    )
    
    ax.set_xticks(np.arange(0, 61, 10))
    add_value_labels(ax, bars, offset=0.5)

    plt.savefig(os.path.join(output_path, 'concentracion_afiliados.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Gráfico de concentración de afiliados guardado.")

def create_density_chart(data_path, output_path):
    """Genera el gráfico de densidad de cotización."""
    df = pd.read_csv(data_path)
    df = df.sort_values(by='Densidad Promedio', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 10))

    # Colores: gradiente para visualizar la brecha
    norm = plt.Normalize(df['Densidad Promedio'].min(), df['Densidad Promedio'].max())
    colors = plt.cm.coolwarm_r(norm(df['Densidad Promedio']))

    bars = ax.barh(df['Departamento'], df['Densidad Promedio'], color=colors, height=0.7)

    style_chart(
        ax=ax, fig=fig,
        title='Densidad de Cotización Promedio por Departamento',
        subtitle='La brecha entre la capital y las regiones rurales es abismal, haciendo inviable la jubilación para millones.',
        xlabel='Porcentaje de Tiempo Aportado (%)',
        source_note='Fuente: Elaboración propia en base a datos de la SBS (Est. Dic 2023).'
    )

    ax.set_xticks(np.arange(0, 71, 10))
    add_value_labels(ax, bars, offset=0.7)

    plt.savefig(os.path.join(output_path, 'densidad_cotizacion.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Gráfico de densidad de cotización guardado.")

def create_correlation_chart(data_path, output_path):
    """Genera un gráfico de dispersión mostrando la correlación entre informalidad y densidad de cotización."""
    df = pd.read_csv(data_path)

    fig, ax = plt.subplots(figsize=(14, 9))

    # Scatter plot
    scatter = ax.scatter(df['Informalidad'], df['Densidad'],
                         c=df['Densidad'],
                         cmap='coolwarm_r',
                         s=100,
                         alpha=0.8,
                         edgecolors='w',
                         linewidth=0.5)

    # Línea de Tendencia
    m, b = np.polyfit(df['Informalidad'], df['Densidad'], 1)
    ax.plot(df['Informalidad'], m*df['Informalidad'] + b, color='#333333', linestyle='--', linewidth=1.5, alpha=0.7, label='Línea de Tendencia')

    # Estilo y Formato
    ax.set_title('El Vínculo Innegable: Informalidad vs. Aportes a la Pensión', fontsize=20, fontweight='bold', pad=30)
    fig.suptitle('A medida que aumenta la informalidad laboral en un departamento, la capacidad de aportar a una AFP se desploma.', y=0.92, fontsize=14, fontstyle='italic', ha='center')

    ax.set_xlabel('Tasa de Informalidad Laboral (%)', fontsize=12, labelpad=15)
    ax.set_ylabel('Densidad de Cotización Promedio (%)', fontsize=12, labelpad=15)

    # Añadir etiquetas a puntos clave
    puntos_clave = ['Lima', 'Arequipa', 'Cajamarca', 'Huancavelica', 'Puno']
    for i, row in df.iterrows():
        if row['Departamento'] in puntos_clave:
            ax.text(row['Informalidad'] + 0.5, row['Densidad'], row['Departamento'],
                    fontsize=10, ha='left', va='center', fontweight='bold')

    ax.grid(True, color='#EEEEEE', linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.text(0.05, 0.01, 'Fuente: Elaboración propia en base a datos de la SBS e INEI (Est. Dic 2023).', ha='left', fontsize=9, color='gray')

    fig.tight_layout(rect=[0, 0.05, 1, 0.9])
    plt.savefig(os.path.join(output_path, 'correlacion_informalidad_densidad.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Gráfico de correlación entre informalidad y densidad guardado.")

def create_coverage_chart(data_path, output_path):
    """Genera el gráfico de tasa de cobertura previsional por departamento."""
    df = pd.read_csv(data_path)
    df['Tasa de Cobertura'] = 100 - df['Informalidad']
    df = df.sort_values(by='Tasa de Cobertura', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 10))

    # Colores: gradiente para visualizar la brecha
    norm = plt.Normalize(df['Tasa de Cobertura'].min(), df['Tasa de Cobertura'].max())
    colors = plt.cm.viridis(norm(df['Tasa de Cobertura']))

    bars = ax.barh(df['Departamento'], df['Tasa de Cobertura'], color=colors, height=0.7)

    style_chart(
        ax=ax, fig=fig,
        title='Tasa de Cobertura Previsional por Departamento',
        subtitle='Porcentaje de la fuerza laboral de cada departamento que está afiliada al SPP.',
        xlabel='Porcentaje de la PEA Departamental Afiliada (%)',
        source_note='Fuente: Elaboración propia en base a datos de INEI (ENAHO 2022).'
    )

    ax.set_xticks(np.arange(0, 51, 10))
    add_value_labels(ax, bars, offset=0.5)

    plt.savefig(os.path.join(output_path, 'cobertura_previsional_departamento.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Gráfico de cobertura previsional por departamento guardado.")

if __name__ == '__main__':
    # Definir rutas de entrada y salida
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    processed_data_path = os.path.join(base_path, 'data', 'processed')
    final_visualizations_path = os.path.join(base_path, 'visualizations', 'final')

    # Crear directorio de salida si no existe
    os.makedirs(final_visualizations_path, exist_ok=True)

    # Rutas a los archivos de datos
    concentration_data_file = os.path.join(processed_data_path, 'concentracion_afiliados.csv')
    density_data_file = os.path.join(processed_data_path, 'densidad_cotizacion.csv')
    correlation_data_file = os.path.join(processed_data_path, 'informalidad_vs_densidad.csv')

    # Generar y guardar los gráficos
    create_concentration_chart(concentration_data_file, final_visualizations_path)
    create_density_chart(density_data_file, final_visualizations_path)
    create_correlation_chart(correlation_data_file, final_visualizations_path)
    create_coverage_chart(correlation_data_file, final_visualizations_path) # Usa el mismo archivo de datos

    print(f"\nVisualizaciones generadas y guardadas en: {final_visualizations_path}")
