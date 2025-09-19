# Proyecto: Impacto de Exoneraciones Tributarias en San Martín

## 1. Objetivo de la Investigación

Este proyecto busca analizar el impacto del régimen fiscal especial aplicado en el departamento de San Martín (Perú) entre 2005 y 2025. La hipótesis central es que la modificación de los incentivos tributarios, en comparación con otros departamentos amazónicos, pudo haber generado condiciones que facilitaron la depreciación del Capital Natural (deforestación) y el crecimiento de economías ilícitas, un fenómeno oculto por métricas tradicionales como el PBI.

La investigación se enmarca en los conceptos de la "Economía de la Biodiversidad" (Informe Dasgupta) y sigue un enfoque de "Investigación Anfibia" (Rodríguez Garavito), buscando generar conocimiento riguroso con potencial de incidencia en políticas públicas.

## 2. Flujo de Trabajo y Reproducibilidad

Este proyecto sigue un flujo de trabajo robusto para garantizar la máxima reproducibilidad y transparencia.

1.  **Datos Crudos (`/data/01_raw`):** Los datos originales no se modifican nunca.
2.  **Procesamiento de Datos (`/src/data/make_dataset.py`):** Un script dedicado lee los datos crudos, los limpia, procesa y guarda una versión lista para el análisis.
3.  **Datos Procesados (`/data/02_processed`):** Contiene los datasets limpios. Esta es la única fuente de datos para todo el análisis.
4.  **Análisis y Validación (`/src/analysis`):** Los scripts de análisis leen exclusivamente de `/data/02_processed`.
5.  **Resultados Versionados (`/reports`):** Cada ejecución de un script de análisis crea una carpeta única con marca de tiempo (ej. `run_YYYYMMDD_HHMMSS`) dentro de la carpeta de reportes correspondiente (`figures`, `tables`, `validation`). Esto evita la sobrescritura y crea un historial completo de cada experimento. Cada carpeta de ejecución contiene los artefactos generados (gráficos, tablas) y un archivo `run.log` con el registro detallado de la ejecución.

## 3. Estructura del Directorio

-   **/data**: Contiene todos los datos del proyecto.
    -   **/01_raw**: Datos originales, sin ninguna modificación.
    -   **/02_processed**: Datos limpios, transformados y listos para el análisis.
-   **/narratives**: Documentos fundacionales y marco teórico.
-   **/reports**: Resultados generados por los análisis, organizados en carpetas de ejecución versionadas.
    -   **/figures**: Gráficos y visualizaciones.
    -   **/tables**: Tablas de resultados.
    -   **/validation**: Resultados de las pruebas de validación de los modelos.
-   **/src**: Código fuente.
    -   **/data**: Scripts para el procesamiento de datos.
    -   **/analysis**: Scripts para el análisis y modelado.
    -   **/utils.py**: Funciones de utilidad compartidas (ej. logging, gestión de carpetas).
-   **diario_de_investigacion.md**: Bitácora que documenta el proceso de investigación, decisiones y hallazgos.
-   **README.md**: Este archivo.

## 4. Pasos del Análisis

1.  **Prueba de Humo (`smoke_test_analysis.py`):** Un primer análisis rápido para validar si existe una "señal" en los datos.
2.  **Análisis Econométrico Principal:** (En desarrollo) Un modelo de Diferencias en Diferencias (DiD) y/o Control Sintético (SCM) para estimar el impacto causal de la ley de 2005.

**VALIDATION_TEST_LINE_ABCDE**