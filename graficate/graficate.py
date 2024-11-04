import textwrap
import re
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import data_models.data_lists as dl


# this funtion will take a bibtex file and generate a graph whit  databases
def graficvate_databases(data):
    databases = []
    count_dbs = []

    for entry in data:
        # existe la clave database en la entrada
        if 'database' in entry:
            if entry['database'] not in databases:
                databases.append(entry['database'])
                count_dbs.append(1)
            else:
                index = databases.index(entry['database'])
                count_dbs[index] += 1
        # Acceder al título mediante la clave 'title'

    colors = [plt.cm.tab10(i / len(databases)) for i in range(len(databases))]
    plt.figure(figsize=(10, 5))

    plt.title('Databases')
    plt.xlabel('Databases')
    plt.ylabel('Count')

    # Agrega cada base de datos con su color y etiqueta individualmente
    for i, database in enumerate(databases):
        plt.bar(database, count_dbs[i], color=colors[i], label=database)

    # Muestra la leyenda con todas las bases de datos
    plt.legend(title="Databases")
    plt.savefig('assets/graficas/databases.png')


def graficate_year(data, interval=5):
    years_count = {}

    for entry in data:
        if 'year' in entry:
            # Extraer solo los caracteres numéricos del año
            year = re.sub(r'\D', '', entry['year'])
            if year:  # Verifica que no esté vacío después de eliminar letras
                year = int(year)
                # Agrupar el año en intervalos
                interval_start = (year // interval) * \
                    interval  # Agrupa en el intervalo
                years_count[interval_start] = years_count.get(
                    interval_start, 0) + 1

    # Ordenar los intervalos de años y sus conteos
    years, count_years = zip(*sorted(years_count.items()))

    plt.figure(figsize=(15, 5))
    plt.title('Years (Grouped by Intervals)')
    plt.xlabel('Year Intervals')
    plt.ylabel('Count')

    # Crear el gráfico de barras
    plt.bar(years, count_years, width=interval *
            0.8, color='blue', align='center')

    # Ajuste del eje x para mostrar cada intervalo
    plt.xticks(years)  # Muestra solo los intervalos calculados en el eje x

    # Guardar la figura
    plt.savefig('assets/graficas/years.png')

# Llamar a la función con los datos
# graficate_year(data)  # Asegúrate de tener los datos cargados en 'data'


def graficate_entetrype(data):
    enter_types = {}
    for entry in data:
        if 'type' in entry:
            enter_types[entry['type']] = enter_types.get(entry['type'], 0) + 1

    # Crear una lista con los tipos de entradas y sus conteos
    enter_types, count_enter_types = zip(*enter_types.items())

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title('Entry Types')
    plt.xlabel('Entry Types')
    plt.ylabel('Count')

    # Crear el gráfico de barras horizontal
    ax.barh(enter_types, count_enter_types, color='green')

    # Guardar la figura
    plt.savefig('assets/graficas/entry_types.png')


def graficate_journals(data):
    journals = {}

    # Contar la cantidad de veces que aparece cada journal
    for entry in data:
        if 'journal' in entry:
            journals[entry['journal']] = journals.get(entry['journal'], 0) + 1

    # Ordenar los journals por el número de apariciones en orden descendente y tomar los 15 primeros
    top_journals = sorted(
        journals.items(), key=lambda x: x[1], reverse=True)[:25]

    # Verificar que top_journals no esté vacío
    if not top_journals:
        print("No hay journals con suficientes datos para graficar.")
        return

    # Desempaquetar los datos de los 15 journals más citados
    journals, count_journals = zip(*top_journals)

    # Ajustar los nombres de los journals largos con saltos de línea
    journals_wrapped = [textwrap.fill(journal, width=30)
                        for journal in journals]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(24, 20))
    plt.title('Top 25 Journals by Citations')
    plt.xlabel('Count')
    plt.ylabel('Journals')

    # Crear el gráfico de barras horizontal
    ax.barh(journals_wrapped, count_journals, color='purple')

    # Invertir el eje y para que el journal con más citaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de las etiquetas para que no se superpongan
    plt.tight_layout()

    # Guardar la figura
    plt.savefig('assets/graficas/journals.png')


def graficate_authors(data):
    authors = {}

    for entry in data:
        if 'author' in entry and entry['author'].strip():
            # Obtener solo el primer autor y formatear
            # Tomar el primer autor de la lista
            first_author = entry['author'].split(' and ')[0].strip()
            # Formatear a 'inicial del nombre. apellido'
            parts = first_author.split()
            # Verifica que parts no esté vacío y que parts[0] tenga contenido
            if parts and parts[0]:
                formatted_author = f"{parts[0][0].lower()}. {' '.join(
                    parts[1:])}".lower() if len(parts) > 1 else parts[0].lower()
            else:
                formatted_author = "unknown"  # Valor predeterminado si no hay autor válido

            # Contar las citaciones del primer autor
            authors[formatted_author] = authors.get(formatted_author, 0) + 1

    # Ordenar los autores por el número de citaciones en orden descendente y tomar los 15 primeros
    top_authors = sorted(
        authors.items(), key=lambda x: x[1], reverse=True)[:15]

    # Verificar que top_authors no esté vacío
    if not top_authors:
        print("No hay autores con suficientes datos para graficar.")
        return

    # Desempaquetar los datos de los 15 autores más citados
    authors, count_authors = zip(*top_authors)

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 7))

    plt.title('Top 15 Authors by Citations')
    plt.xlabel('Count')
    plt.ylabel('Authors')

    # Crear el gráfico de barras horizontal
    ax.barh(authors, count_authors, color='red')

    # Invertir el eje y para que el autor con más citaciones esté arriba
    ax.invert_yaxis()

    # Guardar la figura
    plt.savefig('assets/graficas/authors.png')


def graficate_journal_year(data):
    # Contador para las combinaciones de journal y year
    journal_year_count = {}

    for entry in data:
        if 'journal' in entry and 'year' in entry:
            journal = entry['journal'].strip()
            # Extraer solo los números del año (ignorar letras)
            year = re.sub(r'\D', '', entry['year'])

            if journal and year:
                year = int(year)  # Convertir el año a entero
                # Usar un set para garantizar que cada año se cuente solo una vez por journal
                journal_year_count[(journal, year)] = journal_year_count.get(
                    (journal, year), 0) + 1

    # Filtrar solo los últimos 20 años
    current_year = max(year for _, year in journal_year_count.keys())
    cutoff_year = current_year - 19  # Limitar a los últimos 20 años
    journal_year_count = {
        k: v for k, v in journal_year_count.items() if k[1] >= cutoff_year}

    # Organizar los datos en un formato adecuado para graficar
    journal_years = list(journal_year_count.keys())
    journals = list(set([j[0] for j in journal_years]))
    years = sorted(list(set([j[1] for j in journal_years])))

    # Crear una matriz de datos para contar las publicaciones
    count_matrix = np.zeros((len(journals), len(years)))

    # Rellenar la matriz con los conteos
    for (journal, year), count in journal_year_count.items():
        journal_idx = journals.index(journal)
        year_idx = years.index(year)
        count_matrix[journal_idx, year_idx] = count

    # Filtrar los top 20 journals con más publicaciones
    top_journals_indices = np.argsort(np.sum(count_matrix, axis=1))[-20:]

    journals = [journals[i] for i in top_journals_indices]
    count_matrix = count_matrix[top_journals_indices, :]

    # Precalcular las posiciones de "left" para las barras apiladas
    left_positions = np.cumsum(count_matrix, axis=1) - count_matrix

    # Ajustar los nombres de los journals largos con saltos de línea
    journals_wrapped = [textwrap.fill(journal, width=30)
                        for journal in journals]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(24, 20))  # Aumentar el tamaño de la figura

    # Obtener una paleta de colores distinta para cada año
    # 'tab20' tiene 20 colores únicos; se ajusta a la cantidad de años
    cmap = cm.get_cmap('tab20', len(years))
    colors = [cmap(i) for i in range(len(years))]

    # Graficar cada año como una barra apilada en cada journal
    width = 0.4  # Ancho de las barras (más delgado para más espacio)
    for i, year in enumerate(years):
        ax.barh(journals_wrapped, count_matrix[:, i], left=left_positions[:, i], label=str(
            year), height=width, color=colors[i])

    plt.title('Publications by Journal and Year (Last 20 Years)', fontsize=18)
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Journals', fontsize=14)
    # Ajustar el tamaño de la fuente de las etiquetas de los journals
    ax.tick_params(axis='y', labelsize=12)

    # Mostrar la leyenda en la parte superior del gráfico dividida en columnas
    ax.legend(title='Year', bbox_to_anchor=(1.05, 1),
              loc='upper left', fontsize=10, ncol=2)

    # Invertir el eje y para que el journal con más publicaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que todo se vea bien
    plt.subplots_adjust(left=0.25, right=0.85, top=0.9, bottom=0.1)

    # Guardar la figura
    plt.savefig('assets/graficas/journals_years.png')
    plt.show()


def graficate_journal_year(data):
    # Contador para las combinaciones de journal y year
    journal_year_count = {}

    for entry in data:
        if 'journal' in entry and 'year' in entry:
            journal = entry['journal'].strip()
            # Extraer solo los números del año (ignorar letras)
            year = re.sub(r'\D', '', entry['year'])

            if journal and year:
                year = int(year)  # Convertir el año a entero
                # Usar un set para garantizar que cada año se cuente solo una vez por journal
                journal_year_count[(journal, year)] = journal_year_count.get(
                    (journal, year), 0) + 1

    # Filtrar solo los últimos 20 años
    current_year = max(year for _, year in journal_year_count.keys())
    cutoff_year = current_year - 19  # Limitar a los últimos 20 años
    journal_year_count = {
        k: v for k, v in journal_year_count.items() if k[1] >= cutoff_year}

    # Organizar los datos en un formato adecuado para graficar
    journal_years = list(journal_year_count.keys())
    journals = list(set([j[0] for j in journal_years]))
    years = sorted(list(set([j[1] for j in journal_years])))

    # Crear una matriz de datos para contar las publicaciones
    count_matrix = np.zeros((len(journals), len(years)))

    # Rellenar la matriz con los conteos
    for (journal, year), count in journal_year_count.items():
        journal_idx = journals.index(journal)
        year_idx = years.index(year)
        count_matrix[journal_idx, year_idx] = count

    # Filtrar los top 20 journals con más publicaciones
    top_journals_indices = np.argsort(np.sum(count_matrix, axis=1))[-20:]

    journals = [journals[i] for i in top_journals_indices]
    count_matrix = count_matrix[top_journals_indices, :]

    # Precalcular las posiciones de "left" para las barras apiladas
    left_positions = np.cumsum(count_matrix, axis=1) - count_matrix

    # Ajustar los nombres de los journals largos con saltos de línea
    journals_wrapped = [textwrap.fill(journal, width=30)
                        for journal in journals]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(24, 20))  # Aumentar el tamaño de la figura

    # Obtener una paleta de colores distinta para cada año
    # 'tab20' tiene 20 colores únicos; se ajusta a la cantidad de años
    cmap = cm.get_cmap('tab20', len(years))
    colors = [cmap(i) for i in range(len(years))]

    # Graficar cada año como una barra apilada en cada journal
    width = 0.4  # Ancho de las barras (más delgado para más espacio)
    for i, year in enumerate(years):
        ax.barh(journals_wrapped, count_matrix[:, i], left=left_positions[:, i], label=str(
            year), height=width, color=colors[i])

    plt.title('Publications by Journal and Year (Last 20 Years)', fontsize=18)
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Journals', fontsize=14)
    # Ajustar el tamaño de la fuente de las etiquetas de los journals
    ax.tick_params(axis='y', labelsize=12)

    # Mostrar la leyenda en la parte superior del gráfico dividida en columnas
    ax.legend(title='Year', bbox_to_anchor=(1.05, 1),
              loc='upper left', fontsize=10, ncol=2)

    # Invertir el eje y para que el journal con más publicaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que todo se vea bien
    plt.subplots_adjust(left=0.25, right=0.85, top=0.9, bottom=0.1)

    # Guardar la figura
    plt.savefig('assets/graficas/journals_years.png')
    plt.show()


def graficate_type_database(data):
    # Contador para las combinaciones de tipo y base de datos
    type_database_count = {}

    # Crear sets para las bases de datos y tipos únicos
    bases_datos = set()
    tipos = set()

    for entry in data:
        if 'type' in entry and 'database' in entry:
            tipo = entry['type'].strip()
            database = entry['database'].strip()

            # Añadir a los sets
            bases_datos.add(database)
            tipos.add(tipo)

            # Contar la cantidad de publicaciones por tipo y base de datos
            type_database_count[(tipo, database)] = type_database_count.get(
                (tipo, database), 0) + 1

    # Convertir los sets a listas ordenadas para un orden consistente
    bases_datos = sorted(list(bases_datos))
    tipos = sorted(list(tipos))[:16]  # Limitar a los 16 tipos únicos

    # Crear una matriz de datos para contar las publicaciones
    count_matrix = np.zeros((len(tipos), len(bases_datos)))

    # Rellenar la matriz con los conteos
    for (tipo, database), count in type_database_count.items():
        if tipo in tipos and database in bases_datos:
            type_idx = tipos.index(tipo)
            database_idx = bases_datos.index(database)
            count_matrix[type_idx, database_idx] = count

    # Precalcular las posiciones de "left" para las barras apiladas
    left_positions = np.cumsum(count_matrix, axis=1) - count_matrix

    # Ajustar los nombres de los tipos largos con saltos de línea
    tipos_wrapped = [textwrap.fill(tipo, width=30) for tipo in tipos]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(20, 12))  # Aumentar el tamaño de la figura

    # Obtener una paleta de colores distinta para cada base de datos
    # 'tab20' tiene 20 colores únicos; se ajusta a la cantidad de bases de datos
    cmap = cm.get_cmap('tab20', len(bases_datos))
    colors = [cmap(i) for i in range(len(bases_datos))]

    # Graficar cada base de datos como una barra apilada en cada tipo
    width = 0.6  # Ancho de las barras
    for i, database in enumerate(bases_datos):
        ax.barh(tipos_wrapped, count_matrix[:, i], left=left_positions[:,
                i], label=database, height=width, color=colors[i])

    plt.title('Publications by Type and Database', fontsize=18)
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Types', fontsize=14)
    # Ajustar el tamaño de la fuente de las etiquetas de los tipos
    ax.tick_params(axis='y', labelsize=12)

    # Mostrar la leyenda en la parte superior del gráfico dividida en columnas si es necesario
    ax.legend(title='Database', bbox_to_anchor=(1.05, 1),
              loc='upper left', fontsize=10, ncol=2)

    # Invertir el eje y para que el tipo con más publicaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que todo se vea bien
    plt.subplots_adjust(left=0.25, right=0.85, top=0.9, bottom=0.1)

    # Guardar la figura
    plt.savefig('assets/graficas/types_databases.png')
    plt.show()


def graficate_words(data):
    # Obtener todos los abstracts
    abstracts = [entry['abstract'] for entry in data if 'abstract' in entry]

    # Definir las categorías y sus listas de palabras
    categories = {
        'Habilities': dl.DataLists.habilities,
        'Computational Concepts': dl.DataLists.computal_concepts,
        'Attitudes': dl.DataLists.actitudes,
        'Psychometric Properties': dl.DataLists.psychometric_properties,
        'Evaluation Tools': dl.DataLists.evaluation_tools,
        'Investigation Design': dl.DataLists.investigation_design,
        'Schooling Level': dl.DataLists.schooling_level,
        'Medium': dl.DataLists.medio,
        'Strategy': dl.DataLists.strategy,
        'Tools': dl.DataLists.tools
    }

    # Contador de frecuencia por categoría
    category_freq = {}

    for category, words in categories.items():
        words = [word.lower() for word in words]  # Convertir todas las palabras a minúsculas
        # Contar la frecuencia total de las palabras de la categoría en todos los abstracts
        total_count = sum(
            sum(abstract.lower().count(word) for abstract in abstracts)
            for word in words
        )
        category_freq[category] = total_count

    # Ordenar las categorías por frecuencia en orden descendente
    sorted_categories = sorted(category_freq.items(), key=lambda x: x[1], reverse=True)

    # Desempaquetar los datos
    categories, count_categories = zip(*sorted_categories)

    # Envolver los nombres de las categorías largas
    categories_wrapped = [textwrap.fill(category, width=20) for category in categories]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(20, 20))
    plt.title('Frecuencia de palabras por categoría en los abstracts')
    plt.xlabel('Count')
    plt.ylabel('Categories')

    # Obtener una paleta de colores distinta para cada barra
    cmap = cm.get_cmap('tab20', len(categories))
    colors = [cmap(i) for i in range(len(categories))]

    # Crear el gráfico de barras horizontal
    bars = ax.barh(categories_wrapped, count_categories, color=colors)

    # Añadir la leyenda con los colores respectivos
    ax.legend(bars, categories, title='Categories', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, ncol=1)

    # Invertir el eje y para que la categoría con más frecuencia esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que la leyenda no se corte
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Ajustar la posición del gráfico para dejar espacio a la leyenda

    # Guardar la figura
    plt.savefig('assets/graficas/words_by_category.png', bbox_inches='tight')

    plt.show()
