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

## Entrada 7: Implementación de Flujo de Trabajo con Versionamiento y Logging

1.  **Decisión:** Se aprueba la propuesta de implementar un sistema de versionamiento de salidas y logging para todos los análisis.
2.  **Metodología:**
    *   Se creará un módulo `src/utils.py` con una función `setup_run_environment()`.
    *   Esta función creará una carpeta única con marca de tiempo para cada ejecución de un script (ej. `reports/analysis_name/run_YYYYMMDD_HHMMSS/`).
    *   Dentro de esta carpeta, se guardarán todos los productos (gráficos, tablas) y un archivo `run.log` que registrará cada paso del proceso.
3.  **Acción Inmediata:** Se procederá a crear el módulo `utils`, refactorizar todos los scripts de análisis para usar este nuevo sistema y documentar el cambio en el `README.md`.

---

## Entrada 8: Crisis de Reproducibilidad y Sincronización de Datos

1.  **Diagnóstico:** El proyecto entró en una fase de bloqueo crítico. A pesar de los reportes de éxito de las herramientas, los cambios en los archivos de datos no se reflejaban en el sistema del usuario. Múltiples intentos de escribir el archivo `deforestation_analysis_data.csv` fallaron con errores de `Permission Denied` (EBUSY), apuntando a un problema de bloqueo de archivos a nivel del sistema operativo, no a un error de código.
2.  **Resolución:** Se estableció un nuevo protocolo. Se creó un script (`setup_data.py`) para manejar la escritura de datos de forma programática. Tras confirmar que el usuario había cerrado todos los programas que pudieran bloquear el archivo, el script se ejecutó con éxito, sincronizando finalmente la "fuente de la verdad" de los datos y resolviendo la crisis.

## Entrada 9: Refactorización a una Arquitectura de Análisis Automatizada

1.  **Decisión Estratégica:** Por instrucción del jefe de proyecto, se aprueba una refactorización completa para adoptar una arquitectura de software más robusta, modular y automatizada.
2.  **Nueva Arquitectura:**
    *   **Orquestador Central (`main.py`):** Se crea un único punto de entrada que gestiona todos los pasos del análisis (`data`, `eda`, `parallel_trends`, `did`) mediante argumentos de línea de comandos.
    *   **Módulo de Econometría (`src/core/econometrics.py`):** Se encapsula toda la lógica para los análisis DiD y de tendencias paralelas en una clase reutilizable (`DiDAnalysis`).
    *   **Flujo de Datos Canónico:** Se refuerza la regla de que todos los análisis leen desde `data/01_raw` y son procesados por `src/data/make_dataset.py`, que ahora filtra los datos para iniciar el análisis oficialmente en **1998**.
3.  **Implementación:** Se reescribieron y actualizaron todos los scripts del proyecto (`make_dataset.py`, `exploratory_data_analysis.py`, `parallel_trends_validation.py`, `README.md`) para alinearse con la nueva arquitectura.

## Entrada 10: Cierre de la Fase de Validación Inicial

1.  **Ejecución del Pipeline:** Se ejecutó con éxito la nueva cadena de comandos a través del orquestador:
    *   `python main.py data`: Regeneró el dataset procesado, filtrado desde 1998.
    *   `python main.py eda`: Regeneró todos los gráficos del análisis exploratorio.
    *   `python main.py parallel_trends`: Ejecutó la validación visual y estadística del supuesto de tendencias paralelas.
2.  **Limpieza del Repositorio:** Se eliminaron todos los artefactos (gráficos, tablas) de corridas anteriores para mantener únicamente los resultados válidos y actuales.
3.  **Estado del Proyecto:** **FASE DE VALIDACIÓN INICIAL COMPLETADA.** El proyecto se encuentra en un estado estable, robusto, automatizado y completamente versionado. La base para el análisis de impacto final está firmemente establecida.

## Entrada 11: Fase Final - Estudio de Eventos y Control Sintético (SCM)

1.  **Análisis de la Dinámica del Impacto:** Se implementó y ejecutó el análisis de **Estudio de Eventos** (`python main.py event_study`). Este paso fue crucial para visualizar la evolución del efecto de la política año a año, confirmando la narrativa del "efecto diferido" que se sospechaba a partir del análisis DiD.
2.  **Depuración y Resiliencia:** La implementación del SCM presentó una serie de desafíos técnicos relacionados con la versión de la librería `pysyncon`. Estos errores (`TypeError`, `AttributeError`, `ValueError`) fueron superados mediante un proceso iterativo de depuración instrumentada con logging, que culminó en la corrección final de la preparación de datos y las llamadas a la API de ploteo.
3.  **Validación Definitiva con SCM:** Se ejecutó con éxito el análisis de **Método de Control Sintético** (`python main.py scm`). Este método, considerado el "estándar de oro", generó un contrafactual robusto y proporcionó la estimación más fiable del impacto causal de la política.
4.  **Estado del Proyecto:** **ANÁLISIS COMPLETADO.** Todos los análisis econométricos planificados se han ejecutado. El proyecto ha generado un conjunto completo de reportes técnicos y visualizaciones que narran una historia coherente y validada sobre el impacto de la política fiscal en la deforestación.