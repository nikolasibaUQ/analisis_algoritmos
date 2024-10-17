import os
import bibtexparser

from normal_data import NormalData

# # Función para leer un archivo .bib
# def leer_bibtex(filepath):
#     with open(filepath, 'r', encoding='utf-8') as bibtex_file:
#         return bibtexparser.load(bibtex_file)

# # Función para combinar múltiples archivos .bib en uno solo
# def combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, output_filepath):
#     entradas_unicas = {}

#     for archivo in archivos_bib:
#         print(f"Leyendo el archivo: {archivo}")
#         # Leer cada archivo .bib y obtener sus entradas
#         bib_database = leer_bibtex(archivo)
#         for entry in bib_database.entries:
#             title = entry.get('title', '').strip().lower()  # Normalizamos el título para evitar errores de capitalización
#             if title and title not in entradas_unicas:
#                 entradas_unicas[title] = entry  # Guardar la entrada si el título es único

#     # Crear un nuevo objeto de base de datos con todas las entradas únicas
#     bib_database_combinado = bibtexparser.bibdatabase.BibDatabase()
#     bib_database_combinado.entries = list(entradas_unicas.values())

#     # Guardar el archivo combinado
#     with open(output_filepath, 'w', encoding='utf-8') as bibtex_file:
#         bibtexparser.dump(bib_database_combinado, bibtex_file)

#     print(f"Archivo combinado sin repetidos guardado en: {output_filepath}")


# # Función para obtener todos los archivos .bib de una carpeta
# def obtener_archivos_bib(carpeta):
#     archivos_bib = []
#     for archivo in os.listdir(carpeta):
#         if archivo.endswith(".bib"):  # Verificar que sea un archivo .bib
#             archivos_bib.append(os.path.join(carpeta, archivo))
#     return archivos_bib

# # Especifica la carpeta que contiene los archivos .bib
# carpeta_bib = 'assets/IEEE/'

# # Obtener todos los archivos .bib de la carpeta
# archivos_bib = obtener_archivos_bib(carpeta_bib)

# # Especificar la carpeta donde se guardará el archivo combinado
# carpeta_salida = 'assets/temps/'

# # Especificar el nombre del archivo de salida
# nombre_archivo_salida = 'IEEEFinal.bib'

# # Crear la ruta completa para el archivo de salida
# ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)

# # Combinar los archivos .bib y guardar en la ruta especificada
# combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, ruta_completa_salida)

# carpeta_bib = 'assets/sage/'

# nombre_archivo_salida = 'SAGEFinal.bib'

# ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
# archivos_bib = obtener_archivos_bib(carpeta_bib)

# combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, ruta_completa_salida)




# carpeta_bib = 'assets/sciense/'

# nombre_archivo_salida = 'ScienceFinal.bib'

# ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
# archivos_bib = obtener_archivos_bib(carpeta_bib)

# combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, ruta_completa_salida)

# carpeta_bib = 'assets/scopus/'
# nombre_archivo_salida = 'ScopusFinal.bib'

# ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
# archivos_bib = obtener_archivos_bib(carpeta_bib)

# combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, ruta_completa_salida)



# carpeta_bib = 'assets/temps/'
# carpeta_salida = 'assets/final/'
# nombre_archivo_salida = 'Final.bib'

# ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
# archivos_bib = obtener_archivos_bib(carpeta_bib)
# combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, ruta_completa_salida)



# Función para leer un archivo .bib
def leer_bibtex(filepath):
    with open(filepath, 'r', encoding='utf-8') as bibtex_file:
        return bibtexparser.load(bibtex_file)

# Función para convertir las entradas .bib a NormalData y filtrar los campos nulos
def convertir_a_normaldata(entries):
    normaldata_entries = []

    for entry in entries:
        author = entry.get('author', None)
        title = entry.get('title', None)
        abstract = entry.get('abstract', None)
        year = entry.get('year', None)
        volume = entry.get('volume', None)

        # Crear instancia de NormalData solo con los campos que existan
        normaldata = NormalData(author=author, title=title, abstract=abstract, year=year, volume=volume)

        # Añadir solo si tiene datos válidos
        if normaldata.get_data():
            normaldata_entries.append(normaldata)
    
    return normaldata_entries

# Función para escribir los datos filtrados en un nuevo archivo .bib
def escribir_bibtex(output_filepath, normaldata_entries):
    with open(output_filepath, 'w', encoding='utf-8') as bibtex_file:
        for entry in normaldata_entries:
            data = entry.get_data()

            # Escribir la entrada en formato .bib
            bibtex_file.write("@article{\n")
            for key, value in data.items():
                bibtex_file.write(f"  {key} = {{{value}}},\n")
            bibtex_file.write("}\n\n")

# Ruta del archivo .bib a procesar
bibtex_file_path = 'assets/final/Final.bib'

# Leer el archivo .bib
bib_database = leer_bibtex(bibtex_file_path)

# Convertir las entradas .bib a NormalData, eliminando campos vacíos
normaldata_entries = convertir_a_normaldata(bib_database.entries)

# Especificar el archivo de salida donde se guardarán las entradas procesadas
archivo_salida = 'assets/final/normalizate_data.bib'

# Escribir los datos filtrados en un nuevo archivo .bib
escribir_bibtex(archivo_salida, normaldata_entries)
