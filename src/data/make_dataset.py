# -*- coding: utf-8 -*-

import pandas as pd
import os

print("Executing make_dataset.py...", flush=True)

# --- PASO 1: Cargar datos crudos ---
print("Iniciando la creación del dataset procesado...", flush=True)
try:
    df = pd.read_csv('data/01_raw/mapbiomas_cobertura_1996_2023.csv')
    print("Datos crudos cargados exitosamente.", flush=True)
except FileNotFoundError:
    print("Error: No se encontró el archivo de datos crudos. Asegúrate de que la ruta es correcta.", flush=True)
    exit()

# --- PASO 2: Procesamiento y limpieza ---
print("Procesando datos: calculando deforestación anual y eliminando outliers...", flush=True)
df = df.sort_values(by=['departamento', 'Periodo'])
df['deforestacion_anual'] = df.groupby('departamento')['cobertura_boscosa'].diff() * -1
df = df.dropna(subset=['deforestacion_anual'])
df = df[df['Periodo'] != 1997] # Excluir el outlier del año 1997
print("Procesamiento completado.", flush=True)

# --- PASO 3: Guardar dataset procesado ---
output_dir = 'data/02_processed'
output_path = os.path.join(output_dir, 'deforestation_analysis_data.csv')

# Asegurarse de que el directorio de salida exista
os.makedirs(output_dir, exist_ok=True)
print(f"Directorio de salida: {output_dir}", flush=True)

try:
    df.to_csv(output_path, index=False)
    print(f"Dataset procesado y guardado exitosamente en: {output_path}", flush=True)
except Exception as e:
    print(f"Error al guardar el archivo procesado: {e}", flush=True)

print("\nCreación del dataset completada.", flush=True)
