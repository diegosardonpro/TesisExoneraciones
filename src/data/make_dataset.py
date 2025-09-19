# -*- coding: utf-8 -*-
"""
Script dedicado a leer los datos crudos, limpiarlos, procesarlos y guardar
una versión única y validada que servirá como fuente para todos los análisis.
"""

import pandas as pd
import os
import logging
import sys

def main():
    """
    Orquesta la creación del dataset procesado.
    """
    logging.info("Iniciando la creación del dataset procesado...")

    # --- PASO 1: Cargar datos crudos ---
    try:
        df = pd.read_csv('data/01_raw/mapbiomas_cobertura_1996_2023.csv')
        logging.info("Datos crudos cargados exitosamente.")
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo de datos crudos 'data/01_raw/mapbiomas_cobertura_1996_2023.csv'.")
        return

    # --- PASO 2: Procesamiento y limpieza ---
    logging.info("Procesando datos...")
    
    df = df.sort_values(by=['departamento', 'Periodo'])
    df['deforestacion_anual'] = df.groupby('departamento')['cobertura_boscosa'].diff() * -1
    
    df_processed = df[df['Periodo'] >= 1998].copy()
    logging.info("Filtro aplicado: El dataset ahora abarca desde 1998 hasta 2023.")

    # --- PASO 3: Guardar dataset procesado ---
    output_dir = 'data/02_processed'
    output_path = os.path.join(output_dir, 'deforestation_analysis_data.csv')

    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df_processed.to_csv(output_path, index=False)
        logging.info(f"Dataset procesado y guardado exitosamente en: {output_path}")
    except Exception as e:
        logging.error(f"Error al guardar el archivo procesado: {e}")

    logging.info("Creación del dataset completada.")

if __name__ == '__main__':
    main()
