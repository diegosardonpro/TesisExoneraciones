# -*- coding: utf-8 -*-
"""
Módulo de econometría con la clase principal para análisis DiD.
"""
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np
from .visualization_utils import style_plot

class DiDAnalysis:
    """
    Clase para encapsular la lógica del análisis de Diferencias en Diferencias.
    """
    def __init__(self, data_path, treatment_unit, treatment_year):
        self.df = pd.read_csv(data_path)
        self.treatment_unit = treatment_unit
        self.treatment_year = treatment_year
        self._prepare_data()

    def _prepare_data(self):
        """Prepara el DataFrame para el análisis DiD."""
        self.df['tratado'] = (self.df['departamento'] == self.treatment_unit).astype(int)
        self.df['post_treatment'] = (self.df['Periodo'] >= self.treatment_year).astype(int)
        self.df['did'] = self.df['tratado'] * self.df['post_treatment']

    def run_did_model(self, start_year=None, end_year=None):
        """
        Ejecuta el modelo DiD clásico.
        Permite filtrar por un rango de años para análisis específicos.
        """
        if start_year and end_year:
            subset_df = self.df[(self.df['Periodo'] >= start_year) & (self.df['Periodo'] <= end_year)]
        else:
            subset_df = self.df
        
        model = smf.ols('deforestacion_anual ~ tratado + post_treatment + did', data=subset_df)
        results = model.fit()
        return results

    def plot_did_results(self, did_results, title, run_dir, filename="did_visual_summary.png"):
        """Genera un gráfico de barras para visualizar los resultados del DiD."""
        # Extraer datos para el gráfico
        pre_treatment_control = self.df[(self.df['tratado'] == 0) & (self.df['post_treatment'] == 0)]['deforestacion_anual'].mean()
        post_treatment_control = self.df[(self.df['tratado'] == 0) & (self.df['post_treatment'] == 1)]['deforestacion_anual'].mean()
        pre_treatment_treated = self.df[(self.df['tratado'] == 1) & (self.df['post_treatment'] == 0)]['deforestacion_anual'].mean()
        post_treatment_treated = self.df[(self.df['tratado'] == 1) & (self.df['post_treatment'] == 1)]['deforestacion_anual'].mean()

        labels = ['Grupo de Control', 'Grupo de Tratamiento (San Martín)']
        pre_means = [pre_treatment_control, pre_treatment_treated]
        post_means = [post_treatment_control, post_treatment_treated]
        
        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 7))
        rects1 = ax.bar(x - width/2, pre_means, width, label=f'Pre-{self.treatment_year}', color='#457B9D', alpha=0.7)
        rects2 = ax.bar(x + width/2, post_means, width, label=f'Post-{self.treatment_year}', color='#A8DADC')

        # Estilo
        ax.set_ylabel('Deforestación Anual Promedio (miles de ha)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(frameon=False, loc='upper left')

        style_plot(ax, fig, title, 
                   f"Efecto DiD estimado: {did_results.params['did']:.2f} (p-valor: {did_results.pvalues['did']:.3f})",
                   'Fuente: Elaboración propia con datos de MapBiomas Perú.')
        
        # Guardar la figura
        plot_path = f"{run_dir}/{filename}"
        fig.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return plot_path

    def run_parallel_trends_test(self):
        """Ejecuta la prueba de tendencias paralelas."""
        pre_intervention_df = self.df[self.df['Periodo'] < self.treatment_year].copy()
        pre_intervention_df['año_norm'] = pre_intervention_df['Periodo'] - pre_intervention_df['Periodo'].min()
        model = smf.ols('deforestacion_anual ~ tratado + año_norm + tratado:año_norm', data=pre_intervention_df)
        results = model.fit()
        return results

    def run_event_study_model(self):
        """Ejecuta un modelo de estudio de eventos."""
        df_event = self.df.copy()
        df_event['relative_year'] = df_event['Periodo'] - self.treatment_year
        
        # Omitir el año base (-1) para evitar multicolinealidad perfecta
        df_event = df_event[df_event['relative_year'] != -1]
        
        # Crear dummies para cada año relativo y tratarlas como categóricas
        formula = f'deforestacion_anual ~ tratado * C(relative_year, Treatment(reference=0)) + C(departamento) + C(Periodo)'
        
        model = smf.ols(formula, data=df_event)
        results = model.fit()
        return results

    def plot_event_study_results(self, event_study_results, run_dir):
        """Genera un gráfico para visualizar los resultados del estudio de eventos."""
        params = event_study_results.params.filter(like='tratado:C(relative_year').reset_index()
        conf_int = event_study_results.conf_int().filter(like='tratado:C(relative_year', axis=0)
        
        params.columns = ['term', 'coef']
        params['relative_year'] = params['term'].apply(lambda x: int(x.split('T.')[1][:-1]))
        
        conf_int.reset_index(inplace=True)
        conf_int.columns = ['term', 'conf_low', 'conf_high']
        
        plot_data = pd.merge(params, conf_int, on='term')
        
        # Añadir el punto base (año -1, efecto 0)
        base_year = pd.DataFrame({'relative_year': [-1], 'coef': [0], 'conf_low': [0], 'conf_high': [0]})
        plot_data = pd.concat([base_year, plot_data]).sort_values('relative_year')

        fig, ax = plt.subplots(figsize=(12, 8))
        
        yerr = [plot_data['coef'] - plot_data['conf_low'], plot_data['conf_high'] - plot_data['coef']]
        ax.errorbar(plot_data['relative_year'], plot_data['coef'], yerr=yerr,
                    fmt='-o', color='#005f73', capsize=5, label='Coeficiente de Impacto Anual')
        
        ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
        ax.axvline(x=-0.5, color='#E63946', linestyle=':', linewidth=2, label=f'Intervención ({self.treatment_year})')
        
        ax.set_xticks(plot_data['relative_year'])
        ax.legend(frameon=False, loc='lower left')
        
        ax.set_xlabel(f"Años relativos a la intervención (Año 0 = {self.treatment_year})")
        ax.set_ylabel("Coeficiente de Impacto (miles de ha)")

        style_plot(ax, fig, "Análisis de Estudio de Eventos",
                   "Evolución del Impacto de la Política Año a Año",
                   'Fuente: Elaboración propia con datos de MapBiomas Perú.')
        
        plot_path = f"{run_dir}/event_study_plot.png"
        fig.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return plot_path
