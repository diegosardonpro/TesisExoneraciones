
import matplotlib.pyplot as plt

def style_chart(ax, fig, title, subtitle, xlabel, source_note):
    """
    Aplica un estilo consistente y profesional a un gráfico de Matplotlib.

    Args:
        ax (matplotlib.axes.Axes): El objeto de ejes del gráfico.
        fig (matplotlib.figure.Figure): El objeto de figura del gráfico.
        title (str): El título principal del gráfico.
        subtitle (str): El subtítulo o texto explicativo.
        xlabel (str): La etiqueta para el eje X.
        source_note (str): La nota de fuente al pie del gráfico.
    """
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
    ax.tick_params(axis='x', colors='gray')

    # --- Configuración del Eje Y ---
    ax.tick_params(axis='y', length=0) # Ocultar las marcas del eje Y

    # --- Añadir Nota de Fuente ---
    fig.text(0.05, 0.01, source_note, ha='left', fontsize=9, color='gray')

    # --- Ajuste del Layout ---
    fig.tight_layout(rect=[0, 0.05, 1, 0.9])

def add_value_labels(ax, bars, offset=0.5):
    """
    Añade etiquetas de valor a las barras de un gráfico horizontal.

    Args:
        ax (matplotlib.axes.Axes): El objeto de ejes del gráfico.
        bars (matplotlib.container.BarContainer): El contenedor de las barras.
        offset (float): El desplazamiento de la etiqueta desde el final de la barra.
    """
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + offset
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                va='center', ha='left', fontsize=10, color='#333333')
