from data_fetching import ieee
from data_cleaning import clean_data as cd
import os
import graficate.graficate as gr
import graficate.tree_graficate as gt


def main():

    #     print('init main')

    # Especifica la carpeta que contiene los archivos .bib
    #     carpeta_bib = 'assets/IEEE/'

    # # Obtener todos los archivos .bib de la carpeta
    #     archivos_bib = cd.obtener_archivos_bib(carpeta_bib)

    # # # Especificar la carpeta donde se guardará el archivo combinado
    #     carpeta_salida = 'assets/temps/'

    # # # Especificar el nombre del archivo de salida
    #     nombre_archivo_salida = 'IEEEFinal.bib'

    # # Crear la ruta completa para el archivo de salida
    #     ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)

    # # Combinar los archivos .bib y guardar en la ruta especificada
    #     cd.combinar_bibtex_sin_repetidos_por_titulo(
    #         archivos_bib, ruta_completa_salida)

    #     carpeta_bib = 'assets/sage/'

    #     nombre_archivo_salida = 'SAGEFinal.bib'

    #     ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)

    #     archivos_bib = cd.obtener_archivos_bib(carpeta_bib)

    #     cd.combinar_bibtex_sin_repetidos_por_titulo(
    #         archivos_bib, ruta_completa_salida)

    #     carpeta_bib = 'assets/sciense/'

    #     nombre_archivo_salida = 'ScienceFinal.bib'

    #     ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
    #     archivos_bib = cd.obtener_archivos_bib(carpeta_bib)

    #     cd.combinar_bibtex_sin_repetidos_por_titulo(
    #         archivos_bib, ruta_completa_salida)

    #     carpeta_bib = 'assets/scopus/'
    #     nombre_archivo_salida = 'ScopusFinal.bib'

    #     ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
    #     archivos_bib = cd.obtener_archivos_bib(carpeta_bib)

    #     cd.combinar_bibtex_sin_repetidos_por_titulo(
    #         archivos_bib, ruta_completa_salida)

    #     carpeta_bib = 'assets/temps/'
    #     carpeta_salida = 'assets/final/'
    #     nombre_archivo_salida = 'Final.bib'

    #     ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
    #     archivos_bib = cd.obtener_archivos_bib(carpeta_bib)
    #     cd.combinar_bibtex_sin_repetidos_por_titulo(
    #         archivos_bib, ruta_completa_salida)

    #     # Ruta del archivo .bib a procesar
    #     bibtex_file_path = 'assets/final/Final.bib'

    # # Leer el archivo .bib
    #     bib_database = cd.leer_bibtex_con_mmap_regex(bibtex_file_path)

    # # Convertir las entradas .bib a NormalData, eliminando campos vacíos
    #     normaldata_entries = cd.convertir_a_normaldata(bib_database)

    # # Especificar el archivo de salida donde se guardarán las entradas procesadas
    #     archivo_salida = 'assets/final/normalizate_data.bib'

    # # Escribir los datos filtrados en un nuevo archivo .bib
    #     cd.escribir_bibtex(archivo_salida, normaldata_entries)

    data = cd.leer_bibtex_con_mmap_regex('assets/final/Final.bib')
    # gr.graficvate_databases(data=data)
    # gr.graficate_year(data=data)
    # gr.graficate_entertype(data=data)
    # gr.graficate_journals(data=data)
    # gr.graficate_authors(data=data)
    # gr.stacked_bar_journal_entry_type_inverted(data=data)
    # gr.heatmap_journal_entry_type_wrapped(data=data)

    # gr.graficate_journal_year(data=data)
    # gr.graficate_type_database(data=data)
    # gr.graficate_words(data=data)
    # gr.generate_table_words(data=data)
    # gr.graficate_publisher(data=data)
    # gr.graficate_top_cited_articles(data=data)
    # gr.graficate_type_year(data=data)
    # gr.graficate_author_database(data=data)
    # gr.heatmap_author_journals(data=data)
    # gr.graficate_top_cited(data=data)
    # gt.build_graph(data)
    # gt.build_separate_trees(data)
    gr.authors_by_country(data=data)
    


if __name__ == '__main__':
    main()
