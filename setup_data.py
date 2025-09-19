import logging
import os
from src.core.data_manager import get_truth_data, save_processed_data

def setup_logging():
    """Configura un logging robusto a consola y archivo."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, 'data_setup.log')
    
    logger = logging.getLogger('DataSetup')
    logger.setLevel(logging.INFO)
    
    # Evitar duplicar handlers si se ejecuta varias veces
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formato del log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler para el archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para la consola
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger

def main():
    """Función principal para orquestar la configuración de datos."""
    logger = setup_logging()
    logger.info("--- Inicio del script de configuración de datos ---")
    
    output_path = "data/02_processed/deforestation_analysis_data.csv"
    
    logger.info("Paso 1: Obteniendo los datos desde la 'fuente de la verdad'.")
    truth_df = get_truth_data()
    
    logger.info(f"Paso 2: Intentando guardar los datos procesados en '{output_path}'.")
    save_processed_data(truth_df, output_path, logger)
    
    logger.info("--- Fin del script de configuración de datos ---")

if __name__ == "__main__":
    main()
