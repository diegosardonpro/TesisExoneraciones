# Guía de Inducción para Agentes de IA

## 1. Misión del Proyecto

El objetivo de esta investigación es medir el impacto causal de la reforma fiscal de 2005 en la deforestación del departamento de San Martín, Perú. Para ello, se utiliza un pipeline de análisis econométrico automatizado que compara la evolución de San Martín con un grupo de control de otros departamentos amazónicos.

## 2. Estado Actual del Proyecto

**COMPLETADO Y FUNCIONAL.**

El pipeline de análisis ha sido ejecutado en su totalidad. Todos los scripts son funcionales y los resultados finales han sido generados y versionados. El proyecto se encuentra en un estado estable y cerrado.

Los pasos implementados en el orquestador `main.py` son:
- `data`: Creación del dataset limpio y procesado.
- `eda`: Análisis Exploratorio de Datos.
- `parallel_trends`: Validación del supuesto de tendencias paralelas para el modelo DiD.
- `did`: Ejecución del análisis de Diferencias en Diferencias.
- `robustness`: Pruebas de robustez (placebo) sobre los resultados DiD.
- `event_study`: Análisis de Estudio de Eventos para visualizar la dinámica del impacto.
- `scm`: Análisis de Método de Control Sintético como validación final.

## 3. Filosofía y Arquitectura del Proyecto

- **Orquestador Central:** Toda la ejecución se centraliza en `main.py`. **Nunca ejecutes los scripts de análisis directamente.** Usa `python main.py <paso>`.
- **Enfoque Anfibio:** Cada análisis econométrico genera dos artefactos: un reporte técnico en texto (`.txt`) con los resultados estadísticos, y una o más visualizaciones de alta calidad (`.png`) que comunican los hallazgos de forma intuitiva.
- **Modularidad:** La lógica reutilizable está encapsulada en `src/core/` (econometría, visualización). Los scripts de análisis en `src/analysis/` orquestan la lógica para cada paso específico.
- **Versionamiento de Salidas:** Cada ejecución de un script crea una carpeta única con marca de tiempo en `reports/`, asegurando que ningún resultado se sobrescriba y manteniendo un historial completo.

## 4. Roadmap de Inducción (Tu Camino del Conocimiento)

Para entender este proyecto en profundidad y poder operar sobre él, debes leer los siguientes documentos en el orden estricto que se presenta. No intentes modificar código sin haber completado este roadmap.

**1. `README.md` (5 minutos):**
   - **Objetivo:** Entender el **qué** (propósito del proyecto) y el **cómo** a alto nivel (la estructura de carpetas y los comandos de ejecución de `main.py`).

**2. `diario_de_investigacion.md` (15 minutos):**
   - **Objetivo:** Entender la **historia y la narrativa** del proyecto. Este es el documento más importante para el contexto. Aprenderás sobre la hipótesis inicial, los descubrimientos contraintuitivos, las decisiones estratégicas (como el cambio de enfoque a un modelo de dos shocks) y la evolución de la arquitectura.

**3. `POSTMORTEM_SCM_DEBUG.md` (10 minutos):**
   - **Objetivo:** Aprender de la batalla técnica más dura del proyecto. **Este documento es de lectura obligatoria.** Detalla la compleja depuración del script de Control Sintético y contiene lecciones técnicas cruciales sobre incompatibilidades de API, estrategias de depuración por introspección (`dir()`) y la importancia de la preparación explícita de datos. Estudiar este documento te ahorrará horas de frustración.

## 5. Cómo Operar

- **Ejecución:** Utiliza siempre el orquestador: `python main.py <paso>`.
- **Modificaciones:** No modifiques el pipeline principal a menos que una nueva fase analítica sea aprobada. Si necesitas experimentar, hazlo en la carpeta `/notebooks`.
- **Nuevos Análisis:** Si implementas un nuevo paso, asegúrate de que siga la arquitectura existente: crea un nuevo script en `src/analysis/`, actualiza `main.py` para incluirlo y asegúrate de que genere resultados en una nueva subcarpeta dentro de `reports/`.
