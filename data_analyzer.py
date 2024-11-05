import pandas as pd
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self, normaldata_entries):
        # Convertir instancias de NormalData a un DataFrame
        entries = [nd.get_data() for nd in normaldata_entries]
        self.df = pd.DataFrame(entries)

        # Asegurar que 'year' y 'citations' sean numéricos
        self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')
        self.df['citations'] = pd.to_numeric(self.df['citations'], errors='coerce')

        # Eliminar filas con valores nulos en campos críticos
        self.df.dropna(subset=['author', 'title', 'year'], inplace=True)

    def generar_estadisticas(self):
        # Estadísticas descriptivas por año de publicación
        stats_por_año = self.df.groupby('year').size()

        # Crear el gráfico de barras
        plt.figure(figsize=(10, 6))
        stats_por_año.plot(kind='bar')
        plt.title("Número de Publicaciones por Año")
        plt.xlabel("Año")
        plt.ylabel("Cantidad de Publicaciones")
        plt.xticks(rotation=45)
        plt.show()

        # Los 15 autores más citados
        top_autores = self.df.groupby('author')['citations'].sum().nlargest(15)

        top_autores = self.df.groupby('author')['citations'].sum().nlargest(15)
        plt.figure(figsize=(10, 6))
        top_autores.plot(kind='bar')
        plt.title("Top 15 Autores Más Citados")
        plt.xlabel("Autor")
        plt.ylabel("Cantidad de Citaciones")
        plt.xticks(rotation=45)
        plt.show()


        # Cantidad de productos por tipo y año
        productos_por_tipo_año = self.df.groupby(['product_type', 'year']).size()

        productos_por_tipo_año.plot(kind='bar', stacked=True, figsize=(12, 7))
        plt.title("Cantidad de Productos por Tipo y Año")
        plt.xlabel("Año")
        plt.ylabel("Cantidad de Productos")
        plt.xticks(rotation=45)
        plt.legend(title="Tipo de Producto")
        plt.show()

        # Almacenar resultados en un diccionario para consulta
        self.stats = {
            'stats_por_año': stats_por_año,
            'top_autores': top_autores,
            'productos_por_tipo_año': productos_por_tipo_año,
        }

    def mostrar_resultados(self):
        # Imprimir o retornar los resultados de los análisis
        print("Estadísticas por año:\n", self.stats['stats_por_año'])
        print("\nTop 15 autores más citados:\n", self.stats['top_autores'])
        print("\nCantidad de productos por tipo y año:\n", self.stats['productos_por_tipo_año'])
