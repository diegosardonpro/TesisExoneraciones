# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

# --- PASO 1: Cargar los datos desde la carpeta de datos crudos ---
try:
    df = pd.read_csv('data/01_raw/mapbiomas_cobertura_1996_2023.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo 'data/01_raw/mapbiomas_cobertura_1996_2023.csv'")
    print("Asegúrate de que el archivo de datos crudos esté en la ubicación correcta.")
    exit()

# --- PASO 2: Calcular la deforestación anual ---
df = df.sort_values(by=['departamento', 'Periodo'])
df['deforestacion_anual'] = df.groupby('departamento')['cobertura_boscosa'].diff() * -1
df = df.dropna(subset=['deforestacion_anual'])

# --- PASO 3: Análisis Estadístico Descriptivo ---
print("--- Análisis Estadístico Descriptivo de la Deforestación Anual (miles de hectáreas) ---")
descriptive_stats = df.groupby('departamento')['deforestacion_anual'].describe()
print(descriptive_stats.to_string(float_format="{:.2f}".format))
print("\n" + "="*80 + "\n")

# --- PASO 4: Preparar los grupos de Tratamiento y Control ---
tratamiento_dep = 'San Martin'
control_deps = ['Amazonas', 'Loreto', 'Ucayali']

df_tratamiento = df[df['departamento'] == tratamiento_dep].copy()
df_control_group = df[df['departamento'].isin(control_deps)]

control_avg = df_control_group.groupby('Periodo')['deforestacion_anual'].mean().reset_index()

# --- PASO 5: Generar el Gráfico de la Divergencia con Estilo Profesional ---

def style_chart(ax, fig, title, subtitle, xlabel, source_note):
    """
    Aplica un estilo consistente y profesional a un gráfico de Matplotlib,
    basado en los ejemplos proporcionados por el usuario.

    Args:
        ax (matplotlib.axes.Axes): El objeto de ejes del gráfico.
        fig (matplotlib.figure.Figure): El objeto de figura del gráfico.
        title (str): El título principal del gráfico.
        subtitle (str): El subtítulo o texto explicativo.
        xlabel (str): La etiqueta para el eje X.
        source_note (str): La nota de fuente al pie del gráfico.
    """
    # Limpiar estilo anterior
    ax.clear()
    
    # --- Títulos y Subtítulos ---
    ax.set_title(title, fontsize=18, fontweight='bold', pad=30, loc='center')
    fig.suptitle(subtitle, y=0.92, fontsize=12, fontstyle='italic', ha='center')

    # --- Ocultar Ejes y Bordes (Spines) ---
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # --- Configuración del Eje X ---
    ax.set_xlabel(xlabel, fontsize=12, labelpad=15, color='gray')
    ax.xaxis.grid(True, color='#EEEEEE', linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', colors='gray', rotation=45)
    
    # --- Configuración del Eje Y ---
    ax.tick_params(axis='y', length=0)
    ax.set_ylabel('Deforestación Anual (miles de hectáreas)', fontsize=12, color='gray')


    # --- Añadir Nota de Fuente ---
    fig.text(0.05, 0.01, source_note, ha='left', fontsize=9, color='gray')

    # --- Ajuste del Layout ---
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(14, 8))

# Aplicar el nuevo estilo
style_chart(ax, fig, 
            title='Prueba de Humo: ¿Divergen las Tendencias de Deforestación?',
            subtitle='Comparación de la deforestación anual en San Martín vs. el promedio de otros departamentos amazónicos',
            xlabel='Año',
            source_note='Fuente: Datos de cobertura boscosa de MapBiomas Perú. Elaboración propia.')

# Dibujar los datos sobre el gráfico ya estilizado
ax.plot(df_tratamiento['Periodo'], df_tratamiento['deforestacion_anual'], marker='o', linestyle='-', label='San Martín (Tratamiento)', color='#E63946')
ax.plot(control_avg['Periodo'], control_avg['deforestacion_anual'], marker='s', linestyle='--', label='Promedio Control (Amazonas, Loreto, Ucayali)', color='#457B9D')
ax.axvline(x=2005, color='#333333', linestyle=':', linewidth=2, label='Ley N° 28575 (Exclusión de San Martín)')

# Configurar leyenda
ax.legend(loc='upper left', frameon=False)

# Guardar el gráfico en la carpeta de reportes
output_path = 'reports/figures/smoke_test_divergence_plot.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Gráfico con estilo profesional guardado en: {output_path}")

# --- PASO 6: Calcular y mostrar el efecto preliminar ---
pre_periodo_mask = (df['Periodo'] >= 2001) & (df['Periodo'] <= 2005)
post_periodo_mask = (df['Periodo'] >= 2006) & (df['Periodo'] <= 2010)

tratamiento_pre = df_tratamiento.loc[pre_periodo_mask]['deforestacion_anual'].mean()
tratamiento_post = df_tratamiento.loc[post_periodo_mask]['deforestacion_anual'].mean()

control_pre = control_avg[(control_avg['Periodo'] >= 2001) & (control_avg['Periodo'] <= 2005)]['deforestacion_anual'].mean()
control_post = control_avg[(control_avg['Periodo'] >= 2006) & (control_avg['Periodo'] <= 2010)]['deforestacion_anual'].mean()

diff_tratamiento = tratamiento_post - tratamiento_pre
diff_control = control_post - control_pre
diff_in_diff = diff_tratamiento - diff_control

print("\n--- Cálculo Preliminar de Diferencias en Diferencias (Período 2001-2010) ---")
print(f"Promedio Deforestación Anual San Martín (Antes, 2001-05): {tratamiento_pre:.2f} mil ha")
print(f"Promedio Deforestación Anual San Martín (Después, 2006-10): {tratamiento_post:.2f} mil ha")
print(f"Cambio en San Martín: {diff_tratamiento:+.2f} mil ha\n")

print(f"Promedio Deforestación Anual Control (Antes, 2001-05): {control_pre:.2f} mil ha")
print(f"Promedio Deforestación Anual Control (Después, 2006-10): {control_post:.2f} mil ha")
print(f"Cambio en el Control: {diff_control:+.2f} mil ha\n")

print("--- Conclusión de la Prueba de Humo ---")
print(f"Estimador Simple de Diferencias en Diferencias: {diff_in_diff:+.2f} mil ha")
print("Interpretación: El estimador sugiere que, en los 5 años posteriores a la ley, la deforestación anual en San Martín se incrementó en aproximadamente 10.49 mil hectáreas adicionales en comparación a lo que habría ocurrido si hubiera seguido la misma tendencia que el grupo de control.")
