# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime

def setup_run_environment(base_path):
    """
    Crea un directorio de ejecución único con marca de tiempo y configura el logging.

    Args:
        base_path (str): La ruta base donde se creará el directorio de la ejecución (ej. 'reports/validation').

    Returns:
        str: La ruta al directorio de ejecución recién creado.
    """
    # Crear el directorio de ejecución con marca de tiempo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base_path, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    # Configurar el logging para guardar en un archivo dentro del nuevo directorio
    log_file = os.path.join(run_dir, 'run.log')
    
    # Remover manejadores de logging existentes para evitar duplicados
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler() # Para seguir viendo los logs en la consola
        ]
    )

    logging.info(f"Directorio de ejecución creado: {run_dir}")
    return run_dir
