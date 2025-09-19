# -*- coding: utf-8 -*-

import pandas as pd
import logging
import os
import sys

# Añadir el directorio raíz del proyecto al sys.path
# Esto asegura que podamos importar 'src' como un módulo.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import setup_run_environment

try:
    from tabulate import tabulate
except ImportError:
    logging.error("La librería 'tabulate' no está instalada. Por favor, instálala manualmente con 'pip install tabulate'.")
    sys.exit(1)

def main():
    """
    Script principal para generar la tabla de estadísticas descriptivas.
    """
    # --- PASO 0: Configurar entorno de ejecución ---
    run_dir = setup_run_environment('reports/tables')
    logging.info("Iniciando la generación de la tabla de estadísticas descriptivas con datos procesados...")

    # --- PASO 1: Cargar datos procesados ---
    try:
        df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
        logging.info("Datos procesados cargados exitosamente.")
    except FileNotFoundError:
        logging.error("No se encontró el archivo de datos procesados. Ejecuta primero 'src/data/make_dataset.py'.")
        return

    # --- PASO 2: Calcular estadísticas descriptivas ---
    logging.info("Calculando estadísticas descriptivas...")
    desc_stats = df.groupby('departamento')['deforestacion_anual'].describe()

    # --- PASO 3: Formatear y guardar la tabla (Estilo \"Investigación Anfibia\") ---
    logging.info("Formateando la tabla...")
    # Formatear los números a dos decimales para una mejor presentación
    for col in desc_stats.columns:
        desc_stats[col] = desc_stats[col].apply(lambda x: f"{x:,.2f}")

    # Renombrar columnas para mayor claridad y en español
    desc_stats = desc_stats.rename(columns={
        'count': 'Observaciones (N)',
        'mean': 'Media',
        'std': 'Desv. Estándar',
        'min': 'Mínimo',
        '25%': 'Percentil 25 (Q1)',
        '50%': 'Mediana (Q2)',
        '75%': 'Percentil 75 (Q3)',
        'max': 'Máximo'
    })

    # Convertir el DataFrame a una tabla formateada con un estilo limpio
    table = tabulate(desc_stats, headers='keys', tablefmt='simple', stralign="center", numalign="center")

    # Añadir título y notas al pie claras y concisas
    title = "Tabla 1: Estadísticas Descriptivas de la Deforestación Anual por Departamento (1998-2023)\n"
    separator = "=" * 120 + "\n"
    notes = (
        "Notas:\n"
        "1.  La deforestación anual se calcula como la diferencia interanual de la cobertura boscosa.\n"
        "2.  Las cifras están expresadas en miles de hectáreas.\n"
        "3.  El año 1997 fue excluido del análisis para eliminar un valor atípico inicial producto del cálculo.\n\n"
        "Fuente: Elaboración propia a partir de datos de MapBiomas Perú (Procesado - Colección 4.0).\n"
    )

    full_table = f"{title}{separator}{table}\n{separator}{notes}"


    # Guardar la tabla en un archivo de texto
    output_path = os.path.join(run_dir, 'descriptive_stats.txt')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_table)
        logging.info(f"Tabla de estadísticas descriptivas guardada en: {output_path}")
    except Exception as e:
        logging.error(f"Error al guardar la tabla: {e}")

    logging.info("Generación de tabla completada.")

if __name__ == '__main__':
    main()
