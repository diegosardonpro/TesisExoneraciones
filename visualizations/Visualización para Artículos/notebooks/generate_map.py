
import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import os

def create_choropleth_map(data_path, geojson_path, output_path):
    """Genera un mapa coroplético de la tasa de cobertura previsional en Perú."""
    
    # --- 1. Cargar y Preparar Datos ---
    try:
        gdf = geopandas.read_file(geojson_path)
        df = pd.read_csv(data_path)
        df['Tasa de Cobertura'] = 100 - df['Informalidad']
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return

    # --- 2. Estandarizar y Unir Datos ---
    df['DEPARTAMENTO_UPPER'] = df['Departamento'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    merged_gdf = gdf.merge(df, left_on='NOMBDEP', right_on='DEPARTAMENTO_UPPER', how="left")

    # --- 3. Crear la Visualización ---
    fig, ax = plt.subplots(1, 1, figsize=(10, 13)) # Altura reducida

    # Plotear el mapa
    merged_gdf.plot(column='Tasa de Cobertura', 
                    cmap='viridis', 
                    linewidth=0.8, 
                    ax=ax, 
                    edgecolor='0.8', 
                    legend=True,
                    legend_kwds={'label': "Tasa de Cobertura Previsional (%)",
                                 'orientation': "horizontal",
                                 'shrink': 0.7, # Leyenda más ancha
                                 'pad': 0.01}) # Espacio reducido

    # --- 4. Estilo y Formato ---
    ax.axis('off')
    ax.set_title('Cobertura del Sistema de Pensiones por Departamento', 
                 fontdict={'fontsize': '18', 'fontweight': 'bold'})
    
    # Anotaciones con mayor tamaño y reposicionadas
    ax.annotate('''La cobertura es un privilegio casi exclusivo de la costa y la capital,
mientras la sierra y selva permanecen desconectadas del sistema.''',
                xy=(0.1, .1), xycoords='figure fraction', # Posición Y ajustada
                horizontalalignment='left', verticalalignment='top', 
                fontsize=13, color='#555555') # Tamaño de fuente aumentado

    ax.annotate('Fuente: Elaboración propia con datos de INEI (ENAHO 2022) y juaneladio/peru-geojson.',
                xy=(0.1, .05), xycoords='figure fraction', # Posición Y ajustada
                horizontalalignment='left', verticalalignment='top', 
                fontsize=9, color='gray') # Tamaño de fuente aumentado

    # --- 5. Guardar el Gráfico ---
    try:
        plt.savefig(os.path.join(output_path, 'mapa_cobertura_peru.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("Gráfico de mapa coroplético guardado.")
    except Exception as e:
        print(f"Error al guardar el mapa: {e}")

if __name__ == '__main__':
    # Definir rutas
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_data_path = os.path.join(base_path, 'data', 'raw')
    processed_data_path = os.path.join(base_path, 'data', 'processed')
    final_visualizations_path = os.path.join(base_path, 'visualizations', 'final')
    
    # Ruta al archivo GeoJSON local
    geojson_file = os.path.join(raw_data_path, "peru_departamentos.geojson")
    
    # Archivo de datos del proyecto
    correlation_data_file = os.path.join(processed_data_path, 'informalidad_vs_densidad.csv')

    # Crear y guardar el mapa
    create_choropleth_map(correlation_data_file, geojson_file, final_visualizations_path)
