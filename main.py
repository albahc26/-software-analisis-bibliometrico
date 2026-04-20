# --- INSTALACIÓN DE LIBRERÍAS NECESARIAS ---
!pip install pandas openpyxl python-docx

import pandas as pd
import numpy as np
from docx import Document
import matplotlib.pyplot as plt
import networkx as nx


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

def ranking_revistas(df):
    # 'Source title' es el nombre común de la columna en Scopus
    ranking = df['Source title'].value_counts().reset_index()
    ranking.columns = ['Revista', 'Num_Articulos']
    print("\n📚 Top Revistas:")
    print(ranking.head(10))
    return ranking

# HU 21: Índice H Global del Dataset
def calcular_indice_h_global(df):
    # Se ordenan las citas de mayor a menor
    citas = sorted(df['Cited by'].dropna().tolist(), reverse=True)
    h_index = 0
    for i, c in enumerate(citas):
        if c >= i + 1:
            h_index = i + 1
        else:
            break
    print(f"\n📈 Índice H del Dataset: {h_index}")
    return h_index

# HU 22: Buscador interno
def buscar_en_procesados(df, termino):
    # Busca en Título, Autores o Keywords
    resultado = df[df['Title'].str.contains(termino, case=False) | 
                   df['Authors'].str.contains(termino, case=False)]
    return resultado[['Title', 'Authors', 'Year', 'Cited by']]

# HU 23: Enlaces DOI (Formato HTML para Colab)
def generar_links_doi(df):
    # Crea una columna con el link clickable
    def format_doi(doi):
        if pd.isna(doi): return "N/A"
        return f"https://doi.org/{doi}"
    
    df['Link_DOI'] = df['DOI'].apply(format_doi)
    return df[['Title', 'Link_DOI']].head()

# HU 24: Visualización Visual (Gráficos)
def generar_graficos(df):
    plt.figure(figsize=(12, 5))
    
    # Gráfico de Barras - Top 5 Países (Ejemplo)
    plt.subplot(1, 2, 1)
    df['Country'].value_counts().head(5).plot(kind='bar', color='skyblue')
    plt.title('Top 5 Países')
    
    # Gráfico de Pastel - Distribución de tipos de documento
    plt.subplot(1, 2, 2)
    df['Document Type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Tipos de Documento')
    
    plt.tight_layout()
    plt.show()

# HU 25: Red de Coautoría (Simplificada)
def visualizar_red_coautoria(df):
    G = nx.Graph()
    # Tomamos los primeros 20 artículos para no saturar el gráfico
    for lista_autores in df['Authors'].str.split(',').head(20):
        autores = [a.strip() for a in lista_autores]
        # Crear conexiones entre todos los autores del mismo artículo
        for i in range(len(autores)):
            for j in range(i + 1, len(autores)):
                G.add_edge(autores[i], autores[j])
    
    plt.figure(figsize=(10, 7))
    nx.draw(G, with_labels=True, node_size=50, font_size=8, edge_color='gray')
    plt.title("Red de Coautoría (Muestra)")
    plt.show()

    

# --- PRUEBA DEL SISTEMA ---
# 1. Instanciar
app = AnalisisBibliometrico()

# 2. Cargar (Asegúrate de subir un archivo llamado 'scopus.csv' a Colab)
# app.cargar_datos('scopus.csv') 

# 3. Analizar
# resultados = app.ejecutar_analisis()
