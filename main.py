import bibtexparser
from normal_data import NormalData
from data_analyzer import DataAnalyzer

# Función para leer un archivo .bib
def leer_bibtex(C:/Users/kimbe/OneDrive/Documentos/analisis_algoritmos/assets/final/Final.bib):
    with open(filepath, 'r', encoding='utf-8') as bibtex_file:
        return bibtexparser.load(bibtex_file).entries

# Paso 1: Leer el archivo Final.bib
bib_entries = leer_bibtex('assets/final/Final.bib')

# Paso 2: Convertir las entradas a NormalData
normaldata_entries = [] 
for entry in bib_entries:
    normaldata = NormalData(
        author=entry.get('author'),
        title=entry.get('title'),
        abstract=entry.get('abstract'),
        year=int(entry.get('year', 0)),
        product_type=entry.get('type'),
        affiliation=entry.get('affiliation'),
        journal=entry.get('journal'),
        publisher=entry.get('publisher'),
        database=entry.get('database'),
        citations=int(entry.get('citations', 0))
    )
    normaldata_entries.append(normaldata)

# Paso 3: Análisis con DataAnalyzer
analyzer = DataAnalyzer(normaldata_entries)
analyzer.generar_estadisticas()
analyzer.mostrar_resultados()
