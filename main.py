# -*- coding: utf-8 -*-
"""
Script principal para orquestar todas las fases del análisis econométrico.

Uso desde la terminal:
- Para ejecutar el pre-procesamiento de datos:
  python main.py data

- Para ejecutar el Análisis Exploratorio de Datos (EDA):
  python main.py eda

- Para validar tendencias paralelas para un año específico (ej. 2006):
  python main.py parallel_trends --year 2006

- Para ejecutar el análisis DiD para un año específico (ej. 2006):
  python main.py did --year 2006

... y así para los demás pasos.
"""
import argparse
import logging
import sys
import os
from datetime import datetime

def setup_logging():
    """Configura un sistema de logging robusto con salida a archivo y consola."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        '%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        os.path.join(log_dir, f"analysis_{datetime.now().strftime('%Y%m%d')}.log"),
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('pandas').setLevel(logging.WARNING)

def main():
    """Punto de entrada principal del programa."""
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Orquestador del proyecto de análisis de deforestación.")
    parser.add_argument(
        "step",
        choices=["data", "eda", "parallel_trends", "did", "robustness", "event_study", "scm"],
        help="El paso del análisis a ejecutar."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2005,
        help="Año de intervención para el análisis. Default: 2005."
    )
    args = parser.parse_args()

    logging.info(f"--- Iniciando ejecución del paso: '{args.step}' para el año de intervención '{args.year}' ---")
    
    try:
        if args.step == "data":
            from src.data import make_dataset
            make_dataset.main()
        elif args.step == "eda":
            from src.analysis import exploratory_data_analysis
            exploratory_data_analysis.main()
        elif args.step == "parallel_trends":
            from src.analysis import parallel_trends_validation
            parallel_trends_validation.main(year=args.year)
        elif args.step == "did":
            from src.analysis import did_analysis
            did_analysis.main(year=args.year)
        elif args.step == "robustness":
            from src.analysis import robustness_checks
            robustness_checks.main()
        elif args.step == "event_study":
            from src.analysis import event_study_analysis
            event_study_analysis.main(year=args.year)
        elif args.step == "scm":
            from src.analysis import scm_analysis
            scm_analysis.main(year=args.year)
            
        logging.info(f"--- Paso '{args.step}' para el año '{args.year}' completado exitosamente. ---")

    except Exception as e:
        logging.critical(f"--- Ocurrió un error fatal durante el paso '{args.step}' (año {args.year}) ---", exc_info=True)
        logging.critical(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()