# Proyecto: Impacto de Exoneraciones Tributarias en San Martín

## 1. Objetivo de la Investigación
Este proyecto busca analizar el impacto del régimen fiscal especial aplicado en el departamento de San Martín (Perú) entre 2005 y 2025. La hipótesis central es que la modificación de los incentivos tributarios, en comparación con otros departamentos amazónicos, pudo haber generado condiciones que facilitaron la depreciación del Capital Natural (deforestación) y el crecimiento de economías ilícitas.

## 2. Flujo de Trabajo y Automatización
Este proyecto sigue un flujo de trabajo modular y automatizado para garantizar la máxima reproducibilidad y transparencia. Todas las operaciones se gestionan a través del script orquestador `main.py`.

### Cómo Ejecutar el Análisis
Abre una terminal en la raíz del proyecto y utiliza los siguientes comandos:

**Crear el Dataset Procesado:**
Limpia los datos crudos y genera la "fuente de la verdad" para todos los análisis.
```bash
python main.py data
```

**Generar Gráficos del EDA:**
Crea las visualizaciones exploratorias a partir de los datos procesados.
```bash
python main.py eda
```

**Validar Supuesto de Tendencias Paralelas:**
Ejecuta la validación visual y estadística indispensable para el modelo DiD.
```bash
python main.py parallel_trends
```

**Ejecutar el Análisis de Impacto DiD:**
Corre el modelo de Diferencias en Diferencias y genera el reporte de resultados.
```bash
python main.py did
```

## 3. Estructura del Directorio
- **/data**: Contiene todos los datos.
  - **/01_raw**: Datos originales, sin modificar.
  - **/02_processed**: Datos limpios generados por `main.py data`. Única fuente para análisis.
- **/reports**: Resultados generados, organizados en carpetas de ejecución versionadas.
  - **/figures**: Gráficos y visualizaciones.
  - **/tables**: Tablas de resultados.
  - **/validation**: Resultados de validación de supuestos.
  - **/did_analysis**: Reportes del análisis de impacto.
- **/src**: Código fuente.
  - **/core**: Módulos centrales y reutilizables.
  - **/data**: Scripts para el procesamiento de datos (ej. `make_dataset.py`).
  - **/analysis**: Scripts para cada fase del análisis.
- **main.py**: Orquestador principal del proyecto.
- **diario_de_investigacion.md**: Bitácora del proceso de investigación.
- **README.md**: Este archivo.
