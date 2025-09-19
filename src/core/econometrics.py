# -*- coding: utf-8 -*-
"""
Módulo central para el análisis econométrico.

Contiene la clase DiDAnalysis que encapsula la lógica para el análisis
de Diferencias en Diferencias, asegurando modularidad y reutilizabilidad.
"""
import pandas as pd
import statsmodels.formula.api as smf
import logging

class DiDAnalysis:
    """
    Una clase para gestionar y ejecutar un análisis de Diferencias en Diferencias.
    """
    def __init__(self, data_path, treatment_group, control_group, treatment_year):
        """
        Inicializa el análisis DiD.

        Args:
            data_path (str): Ruta al archivo de datos procesados.
            treatment_group (str): Nombre del departamento de tratamiento.
            control_group (list): Lista de nombres de departamentos de control.
            treatment_year (int): Año en que comienza la intervención.
        """
        self.data_path = data_path
        self.treatment_group = treatment_group
        self.control_group = control_group
        self.treatment_year = treatment_year
        self.df = None
        self.results = {}
        self._load_and_prepare_data()

    def _load_and_prepare_data(self):
        """Carga y prepara el DataFrame para el análisis."""
        try:
            # Cargar solo los datos de los grupos de tratamiento y control
            full_df = pd.read_csv(self.data_path)
            self.df = full_df[full_df['departamento'].isin([self.treatment_group] + self.control_group)].copy()
            
            # Crear las variables necesarias para el modelo DiD
            self.df['tratado'] = (self.df['departamento'] == self.treatment_group).astype(int)
            self.df['post_treatment'] = (self.df['Periodo'] >= self.treatment_year).astype(int)
            self.df['did'] = self.df['post_treatment'] * self.df['tratado']
            logging.info("Datos cargados y preparados para el análisis.")
        except FileNotFoundError:
            logging.error(f"No se encontró el archivo de datos en {self.data_path}.")
            raise

    def run_parallel_trends_test(self):
        """Ejecuta la prueba estadística de tendencias paralelas."""
        logging.info("Ejecutando la prueba estadística de tendencias paralelas...")
        pre_intervention_df = self.df[self.df['Periodo'] < self.treatment_year].copy()
        pre_intervention_df['año_norm'] = pre_intervention_df['Periodo'] - pre_intervention_df['Periodo'].min()
        
        model = smf.ols('deforestacion_anual ~ tratado + año_norm + tratado:año_norm', data=pre_intervention_df).fit()
        self.results['parallel_trends'] = {
            'summary': model.summary(),
            'p_value_interaction': model.pvalues['tratado:año_norm'],
            'coef_interaction': model.params['tratado:año_norm']
        }
        logging.info("Prueba de tendencias paralelas completada.")
        return self.results['parallel_trends']

    def run_did_model(self, start_year=None, end_year=None):
        """
        Ejecuta el modelo DiD principal.

        Args:
            start_year (int, optional): Año de inicio para el análisis post-tratamiento. Defaults to treatment_year.
            end_year (int, optional): Año de fin para el análisis post-tratamiento. Defaults to last year in data.

        Returns:
            dict: Un diccionario con el resumen y los parámetros del modelo.
        """
        start_year = start_year or self.treatment_year
        end_year = end_year or self.df['Periodo'].max()
        period_key = f"did_{start_year}_{end_year}"
        logging.info(f"Ejecutando modelo DiD para el período {start_year}-{end_year}...")
        
        analysis_df = self.df[
            (self.df['Periodo'] < self.treatment_year) | 
            ((self.df['Periodo'] >= start_year) & (self.df['Periodo'] <= end_year))
        ].copy()

        model = smf.ols('deforestacion_anual ~ tratado + post_treatment + did', data=analysis_df).fit()
        
        self.results[period_key] = {
            'summary': model.summary(),
            'coef_did': model.params['did'],
            'p_value_did': model.pvalues['did']
        }
        logging.info(f"Modelo DiD para {period_key} completado.")
        return self.results[period_key]
