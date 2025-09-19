# Proyecto: Impacto de Exoneraciones Tributarias en San Martín

## 1. Objetivo de la Investigación

Este proyecto busca analizar el impacto del régimen fiscal especial aplicado en el departamento de San Martín (Perú) entre 2005 y 2025. La hipótesis central es que la modificación de los incentivos tributarios, en comparación con otros departamentos amazónicos, pudo haber generado condiciones que facilitaron la depreciación del Capital Natural (deforestación) y el crecimiento de economías ilícitas, un fenómeno oculto por métricas tradicionales como el PBI.

La investigación se enmarca en los conceptos de la "Economía de la Biodiversidad" (Informe Dasgupta) y sigue un enfoque de "Investigación Anfibia" (Rodríguez Garavito), buscando generar conocimiento riguroso con potencial de incidencia en políticas públicas.

## 2. Estructura del Directorio

El proyecto está organizado de la siguiente manera para asegurar la reproducibilidad y claridad del análisis:

- **/data**: Contiene todos los datos del proyecto.
  - **/01_raw**: Datos originales, sin ninguna modificación. Aquí se encuentra `mapbiomas_cobertura_1996_2023.csv`.
  - **/02_processed**: Datos limpios, transformados y listos para el análisis.

- **/narratives**: Documentos fundacionales, marco teórico y análisis cualitativos que dan contexto a la investigación.

- **/notebooks**: Jupyter Notebooks utilizados para la exploración de datos y análisis preliminares.

- **/reports**: Contiene los resultados finales de la investigación.
  - **/figures**: Gráficos, mapas y otras visualizaciones generadas por los scripts de análisis.

- **/src**: Contiene todo el código fuente para el análisis.
  - **/analysis**: Scripts principales de análisis, como `smoke_test_analysis.py`.

- **README.md**: Este archivo, que documenta el proyecto.

## 3. Pasos del Análisis

1.  **Prueba de Humo (`smoke_test_analysis.py`):** Un primer análisis rápido para validar si existe una "señal" en los datos de deforestación que justifique un análisis más profundo.
2.  **Análisis Econométrico Principal:** (Por desarrollar) Un modelo de Diferencias en Diferencias o Control Sintético para estimar el impacto causal de la ley de 2005.
3.  **Análisis Cualitativo del Fideicomiso:** (Por desarrollar) Investigación sobre el uso de los fondos de compensación en San Martín.
