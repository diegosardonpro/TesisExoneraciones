# -*- coding: utf-8 -*-
"""
Script principal para orquestar todas las fases del análisis econométrico.

Uso desde la terminal:
- Para ejecutar el pre-procesamiento de datos:
  python main.py data

- Para ejecutar el Análisis Exploratorio de Datos (EDA):
  python main.py eda

- Para validar el supuesto de tendencias paralelas:
  python main.py parallel_trends

- Para ejecutar el análisis de impacto DiD:
  python main.py did
"""
import argparse
import logging
import sys

# Configuración del logging para que los mensajes se muestren en la consola
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    stream=sys.stdout
)

def main():
    """Punto de entrada principal del programa."""
    parser = argparse.ArgumentParser(description="Orquestador del proyecto de análisis de deforestación.")
    parser.add_argument(
        "step", 
        choices=["data", "eda", "parallel_trends", "did"], 
        help="El paso del análisis a ejecutar."
    )
    args = parser.parse_args()

    logging.info(f"--- Ejecutando el paso: '{args.step}' ---")

    if args.step == "data":
        from src.data import make_dataset
        make_dataset.main()
    elif args.step == "eda":
        from src.analysis import exploratory_data_analysis
        exploratory_data_analysis.main()
    elif args.step == "parallel_trends":
        from src.analysis import parallel_trends_validation
        parallel_trends_validation.main()
    elif args.step == "did":
        # Se necesita crear el script did_analysis.py
        # from src.analysis import did_analysis
        # did_analysis.main()
        logging.warning("El paso 'did' aún no está implementado.")
    
    logging.info(f"--- Paso '{args.step}' completado exitosamente. ---")

if __name__ == "__main__":
    main()
