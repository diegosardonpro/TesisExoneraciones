# -*- coding: utf-8 -*-

import pandas as pd

try:
    from tabulate import tabulate
except ImportError:
    print("La librería 'tabulate' no está instalada. Se intentará instalar ahora.")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        from tabulate import tabulate
        print("'tabulate' se ha instalado correctamente.")
    except Exception as e:
        print(f"No se pudo instalar 'tabulate'. Por favor, instálala manualmente con 'pip install tabulate'. Error: {e}")
        exit()

# --- PASO 1: Cargar datos procesados ---
print("Iniciando la generación de la tabla de estadísticas descriptivas con datos procesados...")
try:
    df = pd.read_csv('data/02_processed/deforestation_analysis_data.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo de datos procesados. Ejecuta primero 'src/data/make_dataset.py'.")
    exit()

# --- PASO 2: Calcular estadísticas descriptivas ---
desc_stats = df.groupby('departamento')['deforestacion_anual'].describe()

# --- PASO 3: Formatear y guardar la tabla (Estilo "Investigación Anfibia") ---

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
separator = "=" * 80 + "\n"
notes = (
    "Notas:\n"
    "1.  La deforestación anual se calcula como la diferencia interanual de la cobertura boscosa.\n"
    "2.  Las cifras están expresadas en miles de hectáreas.\n"
    "3.  El año 1997 fue excluido del análisis para eliminar un valor atípico inicial producto del cálculo.\n\n"
    "Fuente: Elaboración propia a partir de datos de MapBiomas Perú (Procesado - Colección 4.0).\n"
)

full_table = f"{title}{separator}{table}\n{separator}{notes}"


# Guardar la tabla en un archivo de texto
output_path = 'reports/tables/descriptive_stats.txt'
try:
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_table)
    print(f"Tabla de estadísticas descriptivas (formato mejorado) guardada en: {output_path}")
except Exception as e:
    print(f"Error al guardar la tabla: {e}")
