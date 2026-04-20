# --- INSTALACIÓN DE LIBRERÍAS NECESARIAS ---
!pip install pandas openpyxl python-docx

import pandas as pd
import numpy as np
from docx import Document

class AnalisisBibliometrico:
    def __init__(self):
        self.df = None

    # HU 1 & 13: Cargar y Limpiar Duplicados
    def cargar_datos(self, archivo_csv):
        self.df = pd.read_csv(archivo_csv)
        # Eliminar duplicados basados en Título para evitar sesgos
        self.df.drop_duplicates(subset=['Title'], keep='first', inplace=True)
        print(f"✅ Datos cargados. Total de registros únicos: {len(self.df)}")

    # HU 15: Corrección manual
    def corregir_campo(self, indice, columna, nuevo_valor):
        if self.df is not None:
            self.df.at[indice, columna] = nuevo_valor
            print(f"✅ Registro {indice} actualizado en columna '{columna}'.")

    # HU 14: Agrupar variantes de Universidades (Ejemplo simple de mapeo)
    def normalizar_universidades(self, mapeo):
        # mapeo es un diccionario: {"Univ de Sonora": "Universidad de Sonora"}
        self.df['Affiliations'] = self.df['Affiliations'].replace(mapeo)

    # CÁLCULOS DE MÉTRICAS (HU 2 - 11, 16)
    def ejecutar_analisis(self):
        # HU 2: Total Publicaciones
        total_pub = len(self.df)

        # HU 3 & 4: Autores
        # Asumiendo que Scopus separa autores por ';' o ','
        self.df['Autores_Lista'] = self.df['Authors'].str.split(';')
        self.df['Num_Autores'] = self.df['Autores_Lista'].str.len()
        
        autores_unicos = set([autor.strip() for lista in self.df['Autores_Lista'].dropna() for autor in lista])
        promedio_autores = self.df['Num_Autores'].mean()
        solo_un_autor = len(self.df[self.df['Num_Autores'] == 1])

        # HU 8: Promedio anual de citas
        año_actual = 2026 # Según contexto del sistema
        self.df['Citas_Anuales'] = self.df['Cited by'] / (año_actual - self.df['Year'] + 1)

        # MOSTRAR RESULTADOS
        print(f"--- MÉTRICAS GENERALES ---")
        print(f"Total Publicaciones: {total_pub}")
        print(f"Total Autores Únicos: {len(autores_unicos)}")
        print(f"Promedio Autores por Art: {promedio_autores:.2f}")
        print(f"Artículos con autoría individual: {solo_un_autor}")

        # HU 9, 10, 11: Top 10 (Ejemplo Top 10 Trabajos más citados)
        top_trabajos = self.df.sort_values(by='Cited by', ascending=False).head(10)
        
        return top_trabajos

    # HU 12: Exportar a Excel
    def exportar_excel(self, nombre_archivo="resultado_bibliometrico.xlsx"):
        self.df.to_excel(nombre_archivo, index=False)
        print(f"📂 Archivo Excel generado: {nombre_archivo}")

# --- PRUEBA DEL SISTEMA ---
# 1. Instanciar
app = AnalisisBibliometrico()

# 2. Cargar (Asegúrate de subir un archivo llamado 'scopus.csv' a Colab)
# app.cargar_datos('scopus.csv') 

# 3. Analizar
# resultados = app.ejecutar_analisis()
