# Post-Mortem Técnico: Depuración del Script de Control Sintético (SCM)

## 1. Propósito

Este documento detalla el proceso de depuración del script `src/analysis/scm_analysis.py`. El objetivo es registrar las causas raíz de los errores encontrados y las soluciones implementadas, para que sirva como base de conocimiento técnico y evite la repetición de estos problemas en el futuro.

La depuración del SCM fue un proceso complejo debido a una serie de incompatibilidades entre el código base y la versión de la librería `pysyncon` instalada en el entorno de ejecución.

## 2. Comparativa: Código Problemático vs. Código Funcional

A continuación se desglosan las tres áreas clave que fueron corregidas.

### 2.1. Preparación de Datos: El Origen del Error

La causa principal de los errores `TypeError` y `ZeroDivisionError` residía en cómo se preparaban los datos antes de pasarlos a `pysyncon`.

**Versión Problemática:**

El código intentaba que la librería infiriera los predictores a partir de la trayectoria de la variable dependiente, pasando una lista vacía o el nombre de la propia variable a `predictors`.

```python
# CÓDIGO PROBLEMÁTICO
dataprep = Dataprep(
    foo=df_for_scm,
    predictors=[], # O predictors=['deforestacion_anual']
    # ...
)
```

**Diagnóstico:** La API de `pysyncon` requiere que los predictores (las variables que se usan para el "matching" en el período pre-intervención) sean **columnas explícitas y separadas** en el DataFrame de entrada. La librería no infiere los predictores automáticamente de la variable dependiente en este modo.

**Versión Funcional:**

La solución fue reestructurar los datos para crear estas columnas de predictores de forma explícita antes de llamar a `Dataprep`.

```python
# CÓDIGO FUNCIONAL
# Pivoteamos para acceder a los valores de años específicos
df_wide = df.pivot_table(index='departamento', columns='Periodo', values='deforestacion_anual')

# Creamos columnas explícitas para los predictores
predictors_years = [2002, 2003, 2004]
for year in predictors_years:
    df[f"defo_{year}"] = df['departamento'].map(df_wide[year])

# ...
predictor_names = [f"defo_{year}" for year in predictors_years]
dataprep = Dataprep(
    foo=df_for_scm,
    predictors=predictor_names,
    # ...
)
```

**Lección:** La preparación de datos para `pysyncon` debe ser explícita. Las variables para el matching pre-intervención deben existir como columnas independientes.

### 2.2. Configuración de `Dataprep`: Incompatibilidades de API

Incluso con los datos bien preparados, la llamada a `Dataprep` fallaba por desajustes con la versión de la librería.

**Versión Problemática:**

El código incluía parámetros obsoletos (`time_plot`) y omitía otros que ahora son requeridos (`predictors_op`).

```python
# CÓDIGO PROBLEMÁTICO
dataprep = Dataprep(
    # ...
    time_plot=[1998, 2023], # Argumento inválido
    # Omitía 'predictors_op'
)
```

**Versión Funcional:**

La llamada final y correcta refleja la API actual:

```python
# CÓDIGO FUNCIONAL
dataprep = Dataprep(
    # ...
    time_optimize_ssr=[1998, 2004],
    predictors_op="mean"  # Argumento REQUERIDO que faltaba
    # El argumento 'time_plot' fue ELIMINADO
)
```

**Lección:** Ante un `TypeError` en la inicialización de una clase de una librería externa, se debe verificar la firma de la función en la versión instalada. Los argumentos pueden cambiar, volverse obligatorios u obsoletos.

### 2.3. Lógica de Visualización: Depuración por Introspección

El último obstáculo fue la generación de los gráficos, que producía un `AttributeError`.

**Versión Problemática:**

Se intentó usar métodos de ploteo (`synth.plot`, `synth.plot_path`) que no existían o tenían una firma diferente en la versión instalada.

```python
# CÓDIGO PROBLEMÁTICO
# Esta llamada fallaba porque el método no existía o no aceptaba el argumento 'ax'
synth.plot(plot_type="path", ax=ax)
```

**Versión Funcional (Estrategia de Depuración):**

La solución no fue adivinar el nombre correcto, sino forzar al objeto a revelar sus métodos. Se utilizó una **estrategia de depuración por introspección**:

1.  Se añadió `logger.debug(dir(synth))` al script para imprimir todos los atributos y métodos disponibles del objeto `synth` después de ser creado.
2.  El log reveló que los métodos correctos eran `path_plot()` y `gaps_plot()`.
3.  Un error posterior (`TypeError: got an unexpected keyword argument 'ax'`) nos enseñó que estos métodos no aceptaban un objeto `ax`.

La solución final fue refactorizar la visualización para **tomar control total del proceso**:

```python
# CÓDIGO FUNCIONAL
# 1. Extraer los datos crudos del objeto 'synth'
real_path = synth.dataprep.foo[...].set_index('time')['deforestacion_anual']
synth_path = synth._synthetic() # Usando el método "privado" revelado por dir()

# 2. Construir el gráfico desde cero con Matplotlib
fig, ax = plt.subplots(...)
ax.plot(real_path.index, real_path, ...)
ax.plot(synth_path.index, synth_path, ...)

# 3. Aplicar nuestro estilo estandarizado
style_scm_plot(ax, fig, ...)
```

**Lección:** Ante una API externa opaca o con un comportamiento inesperado, la introspección en tiempo de ejecución (`dir()`) es una herramienta de depuración más poderosa que la adivinanza o la documentación externa. Si la API de visualización es problemática, es más robusto extraer los datos y construir los gráficos manualmente.
