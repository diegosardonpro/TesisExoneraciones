import os
import logging
import sys
from datetime import datetime

def setup_run_environment(base_dir):
    """
    Crea un directorio único para una corrida de análisis con marca de tiempo
    y configura un logger para registrar en un archivo dentro de ese directorio.

    Args:
        base_dir (str): El directorio base donde se creará la carpeta de la corrida.

    Returns:
        tuple: Una tupla conteniendo la ruta al directorio de la corrida y el logger configurado.
    """
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base_dir, f"run_{run_timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    # Configuración del logger
    logger = logging.getLogger(f"run_{run_timestamp}")
    logger.setLevel(logging.INFO)
    
    # Evitar añadir handlers duplicados si la función se llama varias veces
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formato del log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler para escribir a un archivo de log en el directorio de la corrida
    log_path = os.path.join(run_dir, 'run.log')
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para mostrar en consola
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    logger.info(f"Directorio de ejecución creado: {run_dir}")
    return run_dir, logger
