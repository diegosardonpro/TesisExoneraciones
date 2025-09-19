# Diario de Investigación: Tesis sobre Exoneraciones en San Martín

**Fecha de Inicio:** 18 de setiembre de 2025

## Entrada 1: Conceptualización y Validación del Proyecto

1.  **Hipótesis Inicial:** El proyecto comenzó con la sospecha de que las exoneraciones tributarias en San Martín eran un mecanismo para el lavado de activos, vinculado a la captura del Estado.
2.  **Análisis de Fuentes:** Se analizaron cuatro documentos clave que definieron el marco del proyecto.
3.  **Validación de Fase 1:** Se creó un `CHECKPOINT_FASE_1.md` para validar la coherencia y viabilidad de la hipótesis refinada.
4.  **Decisión Metodológica:** Se discutieron los métodos DiD y SCM. Se acordó un plan secuencial: usar DiD como análisis base y SCM como mejora.
5.  **Prueba de Humo:** Se realizó un análisis preliminar que arrojó un resultado contraintuitivo: la política parecía estar asociada a una *disminución* relativa de la deforestación en San Martín.

## Entrada 2: Formalización del Análisis Exploratorio de Datos (EDA)

1.  **Decisión:** Se formaliza el paso de Análisis Exploratorio de Datos (EDA) para asegurar la calidad y comprensión de los datos antes del modelado.
2.  **Reestructuración:** Se optimiza la estructura de directorios, creando `reports/tables` y `reports/figures/eda`.
3.  **Plan de Acción:** Se decide crear un script dedicado (`exploratory_data_analysis.py`) para generar todos los productos visuales del EDA.

## Entrada 3: Ejecución del EDA y Pausa Estratégica

1.  **Ejecución y Depuración:** El script `exploratory_data_analysis.py` se ejecutó. Se detectó y corrigió un error que causaba que el gráfico comparativo se generara en blanco. La versión final del script funciona correctamente.
2.  **Entregables Generados:**
    *   **Gráficos Individuales (5):** Creados en `reports/figures/eda/`.
    *   **Gráfico Comparativo (1):** Creados en `reports/figures/eda/`.
3.  **Tareas Pendientes:**
    *   La generación de la tabla de estadísticas en HTML no se pudo automatizar por una limitación técnica. Se entregó al usuario un script independiente (`generar_tabla_descriptiva.py`) para esta tarea.
4.  **Estado del Proyecto:** **Pausado.** El EDA está completo. El proyecto queda a la espera de una decisión estratégica del usuario sobre cuál de las hipótesis (Política Exitosa vs. Efecto Desplazamiento) se perseguirá en la fase de modelado de impacto).

## Entrada 4: Depuración de Datos y Refinamiento del EDA

1.  **Detección de Outlier:** Tras una revisión de los resultados del EDA, se identificó un valor atípico significativo en el primer año de datos de deforestación (1997), específicamente un valor negativo anómalo para el departamento de Madre de Dios. Este valor es un artefacto del método de cálculo (`.diff()`) y no representa una observación real del fenómeno.
2.  **Decisión de Tratamiento:** Para asegurar la robustez del análisis y evitar la distorsión de las métricas y visualizaciones, se ha tomado la decisión de excluir el año 1997 del conjunto de datos. El análisis se centrará, por tanto, en el período 1998-2023.
3.  **Acción Inmediata:** Se procederá a modificar los scripts `exploratory_data_analysis.py` y `descriptive_table.py` para implementar este filtro y se regenerarán todos los productos del EDA (gráficos y tabla de estadísticas).

## Entrada 5: Inicio de la Etapa 1 de Modelado - Validación de Supuestos DiD

1.  **Principio Rector:** Siguiendo el principio `[VALIDACIÓN]`, el primer paso de la Etapa 1 (Análisis DiD) es validar el supuesto fundamental del modelo.
2.  **Acción Inmediata:** Se procederá a realizar la prueba de **Tendencias Paralelas** para el período pre-intervención (1998-2004).
3.  **Metodología de Validación:**
    *   **Visual:** Se generará un gráfico comparando las tendencias de deforestación promedio entre el grupo de tratamiento (San Martín) and el de control.
    *   **Estadística:** Se ejecutará un modelo de regresión sobre los datos pre-intervención para probar si la diferencia en las pendientes de las tendencias es estadísticamente no significativa.
4.  **Entregable:** Se creará un nuevo script (`src/analysis/parallel_trends_validation.py`) que generará un gráfico y una tabla con los resultados de la validación, los cuales se guardarán en una nueva carpeta `reports/validation/`.

## Entrada 6: Reestructuración del Flujo de Datos para Robustez y Reproducibilidad

1.  **Diagnóstico:** Se identificó una falla crítica en el flujo de trabajo: la limpieza de datos se realizaba "en memoria" en cada script de análisis, en lugar de generar un dataset procesado y limpio. Esto va en contra de las mejores prácticas de reproducibilidad.
2.  **Nueva Metodología:** Se adopta un flujo de trabajo estandarizado:
    *   **`data/01_raw/`**: Contiene los datos originales, que no se modificarán.
    *   **`src/data/make_dataset.py`**: Se crea un nuevo script cuya única función es leer de `01_raw`, aplicar toda la limpieza (cálculo de `deforestacion_anual`, eliminación del outlier de 1997) y guardar el resultado.
    *   **`data/02_processed/`**: Contendrá el dataset limpio (`deforestation_analysis_data.csv`), que será la única fuente de datos para todos los análisis futuros.
3.  **Acción Inmediata:** Se procederá a crear `make_dataset.py`, ejecutarlo para generar los datos procesados, y luego refactorizar todos los scripts de análisis (`exploratory_data_analysis.py`, `descriptive_table.py`, `parallel_trends_validation.py`) para que lean directamente del nuevo archivo limpio.