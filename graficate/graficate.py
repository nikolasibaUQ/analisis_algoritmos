import textwrap
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import data_models.data_lists as dl
import pandas as pd
import seaborn as sns


# this funtion will take a bibtex file and generate a graph whit  databases
def graficate_databases(data):
    databases = []
    count_dbs = []

    for entry in data:
        if 'database' in entry:
            if entry['database'] not in databases:
                databases.append(entry['database'])
                count_dbs.append(1)
            else:
                index = databases.index(entry['database'])
                count_dbs[index] += 1

    colors = [plt.cm.tab10(i / len(databases)) for i in range(len(databases))]
    plt.figure(figsize=(10, 5))

    plt.title('Databases')
    plt.xlabel('Databases')
    plt.ylabel('Count')

    # Agrega cada base de datos con su color y etiqueta individualmente
    for i, database in enumerate(databases):
        plt.bar(database, count_dbs[i], color=colors[i], label=database)
        # Agregar el valor encima de cada barra
        plt.text(database, count_dbs[i], str(count_dbs[i]), ha='center', va='bottom', fontsize=10)

    # Muestra la leyenda con todas las bases de datos
    plt.legend(title="Databases")
    plt.tight_layout()  # Ajustar el layout para evitar recortes
    plt.savefig('assets/graficas/databases.png')
    plt.show()

def graficate_year(data):
    years_count = {}

    for entry in data:
        if 'year' in entry:
            # Extraer solo los caracteres numéricos del año
            year = re.sub(r'\D', '', entry['year'])
            if year:  # Verifica que no esté vacío después de eliminar letras
                year = int(year)
                # Contar cada año de forma individual sin agrupación
                years_count[year] = years_count.get(year, 0) + 1

    # Ordenar los años y sus conteos
    years, count_years = zip(*sorted(years_count.items()))

    plt.figure(figsize=(18, 6))
    plt.plot(years, count_years, marker='o', linestyle='-', color='blue')
    # Sombrear el área debajo de la línea
    plt.fill_between(years, count_years, color='lightblue', alpha=0.5)
    plt.title('Publications Over Time')
    plt.xlabel('Years')
    plt.ylabel('Number of Publications')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Ajuste del eje x para mostrar cada año
    plt.xticks(years, rotation=45)

    # Guardar la figura
    plt.tight_layout()
    plt.savefig('assets/graficas/years_timeline.png')

    plt.show()


def graficate_entertype(data):
    enter_types = {}
    for entry in data:
        if 'type' in entry:
            # Convertir a minúsculas para unificar duplicados como "article" y "Article"
            entry_type = entry['type'].strip().lower()
            enter_types[entry_type] = enter_types.get(entry_type, 0) + 1

    # Ordenar los tipos de entrada por conteo en orden descendente
    sorted_enter_types = sorted(enter_types.items(), key=lambda x: x[1], reverse=True)

    # Desempaquetar los datos
    enter_types, count_enter_types = zip(*sorted_enter_types)

    # Envolver los textos largos con textwrap
    enter_types_wrapped = [textwrap.fill(etype, width=20) for etype in enter_types]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.title('Entry Types')
    plt.xlabel('Count')
    plt.ylabel('Entry Types')

    # Obtener una paleta de colores distinta para cada barra
    cmap = cm.get_cmap('tab20', len(enter_types))
    colors = [cmap(i) for i in range(len(enter_types))]

    # Crear el gráfico de barras horizontal con colores diferentes
    bars = ax.barh(enter_types_wrapped, count_enter_types, color=colors)

    # Añadir el valor al final de cada barra
    for bar, count in zip(bars, count_enter_types):
        ax.text(
            bar.get_width() + 0.1,  # Posición en el eje x
            bar.get_y() + bar.get_height() / 2,  # Posición en el eje y
            str(count),
            va='center',
            ha='left',
            fontsize=10
        )

    # Añadir la leyenda con los colores respectivos
    ax.legend(bars, enter_types, title='Entry Types', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, ncol=1)

    # Invertir el eje y para que el tipo con más publicaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que la leyenda no se corte
    
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Ajuste inicial
    plt.subplots_adjust(left=0.2, right=0.85, top=0.9, bottom=0.1)  # Ajuste adicional


    # Guardar la figura
    plt.savefig('assets/graficas/entry_types.png', bbox_inches='tight')

    # Mostrar la figura
    plt.show()


def graficate_journals(data):
    journals = {}

    # Contar la cantidad de veces que aparece cada journal
    for entry in data:
        if 'journal' in entry:
            journals[entry['journal']] = journals.get(entry['journal'], 0) + 1

    # Ordenar los journals por el número de apariciones en orden descendente y tomar los 25 primeros
    top_journals = sorted(journals.items(), key=lambda x: x[1], reverse=True)[:25]

    # Verificar que top_journals no esté vacío
    if not top_journals:
        print("No hay journals con suficientes datos para graficar.")
        return

    # Desempaquetar los datos de los 25 journals más citados
    journals, count_journals = zip(*top_journals)

    # Ajustar los nombres de los journals largos con saltos de línea
    journals_wrapped = [textwrap.fill(journal, width=30) for journal in journals]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(24, 20))
    plt.title('Top 25 Journals by Citations')
    plt.xlabel('Count')
    plt.ylabel('Journals')

    # Generar una paleta de colores única para cada barra
    cmap = cm.get_cmap('tab20', len(journals))
    colors = [cmap(i) for i in range(len(journals))]

    # Crear el gráfico de barras horizontal con colores individuales
    bars = ax.barh(journals_wrapped, count_journals, color=colors)

    # Agregar el total al final de cada barra
    for bar, count in zip(bars, count_journals):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, str(count), 
                va='center', ha='left', fontsize=10)

    # Invertir el eje y para que el journal con más citaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que no se corte
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Guardar la figura
    plt.savefig('assets/graficas/journals.png')
    plt.show()
    
    
def graficate_authors(data):
    authors = {}

    for entry in data:
        if 'author' in entry and entry['author'].strip():
            # Obtener solo el primer autor y formatear
            first_author = entry['author'].split(' and ')[0].strip()
            # Formatear a 'inicial del nombre. apellido'
            parts = first_author.split()
            if parts and parts[0]:
                formatted_author = f"{parts[0][0].lower()}. {' '.join(parts[1:])}".lower() if len(parts) > 1 else parts[0].lower()
            else:
                formatted_author = "unknown"  # Valor predeterminado si no hay autor válido

            # Contar las citaciones del primer autor
            authors[formatted_author] = authors.get(formatted_author, 0) + 1

    # Ordenar los autores por el número de citaciones en orden descendente y tomar los 15 primeros
    top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:15]

    # Verificar que top_authors no esté vacío
    if not top_authors:
        print("No hay autores con suficientes datos para graficar.")
        return

    # Desempaquetar los datos de los 15 autores más citados
    authors, count_authors = zip(*top_authors)

    # Obtener una paleta de colores distinta para cada barra
    cmap = cm.get_cmap('tab20', len(authors))
    colors = [cmap(i) for i in range(len(authors))]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.title('Top 15 Authors by Citations')
    plt.xlabel('Count')
    plt.ylabel('Authors')

    # Crear el gráfico de barras horizontal con colores individuales
    bars = ax.barh(authors, count_authors, color=colors)

    # Añadir los valores al final de cada barra
    for bar, count in zip(bars, count_authors):
        ax.text(
            bar.get_width(),  # posición x, ligeramente a la derecha del final de la barra
            bar.get_y() + bar.get_height() / 2,  # posición y, al centro de la barra
            f'{count}',  # el texto a mostrar (conteo)
            va='center',  # alineación vertical centrada
            ha='left'  # alineación horizontal a la izquierda
        )

    # Invertir el eje y para que el autor con más citaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado para que la leyenda y los textos no se corten
    plt.tight_layout()

    # Guardar la figura
    plt.savefig('assets/graficas/authors.png', bbox_inches='tight')
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
            # Convertir a minúsculas para evitar duplicados por capitalización
            tipo = entry['type'].strip().lower()
            database = entry['database'].strip().lower()

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
    ax.tick_params(axis='y', labelsize=12)  # Ajustar el tamaño de la fuente de las etiquetas de los tipos

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
        # Convertir todas las palabras a minúsculas
        words = [word.lower() for word in words]
        # Contar la frecuencia total de las palabras de la categoría en todos los abstracts
        total_count = sum(
            sum(abstract.lower().count(word) for abstract in abstracts)
            for word in words
        )
        category_freq[category] = total_count

    # Ordenar las categorías por frecuencia en orden descendente
    sorted_categories = sorted(
        category_freq.items(), key=lambda x: x[1], reverse=True)

    # Desempaquetar los datos
    categories, count_categories = zip(*sorted_categories)

    # Envolver los nombres de las categorías largas
    categories_wrapped = [textwrap.fill(
        category, width=20) for category in categories]

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

    # Añadir los valores al final de cada barra
    for bar, count in zip(bars, count_categories):
        ax.text(
            bar.get_width() + 10,  # posición x, ligeramente a la derecha del final de la barra
            bar.get_y() + bar.get_height() / 2,  # posición y, al centro de la barra
            f'{count}',  # el texto a mostrar (conteo)
            va='center',  # alineación vertical centrada
            ha='left'  # alineación horizontal a la izquierda
        )

    # Añadir la leyenda con los colores respectivos
    ax.legend(bars, categories, title='Categories', bbox_to_anchor=(
        1.05, 1), loc='upper left', fontsize=10, ncol=1)

    # Invertir el eje y para que la categoría con más frecuencia esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que la leyenda no se corte
    # Ajustar la posición del gráfico para dejar espacio a la leyenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Guardar la figura
    plt.savefig('assets/graficas/words_by_category.png', bbox_inches='tight')

    plt.show()

def generate_table_words(data):
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
        # Convertir todas las palabras a minúsculas
        words = [word.lower() for word in words]
        # Contar la frecuencia total de las palabras de la categoría en todos los abstracts
        total_count = sum(
            sum(abstract.lower().count(word) for abstract in abstracts)
            for word in words
        )
        category_freq[category] = total_count

    # Ordenar las categorías por frecuencia en orden descendente
    sorted_categories = sorted(
        category_freq.items(), key=lambda x: x[1], reverse=True)

    # Crear un DataFrame de pandas para mostrar los datos en forma de tabla
    df = pd.DataFrame(sorted_categories, columns=['Category', 'Count'])

    # Mostrar la tabla como una gráfica usando matplotlib
    # Ajusta el tamaño de la figura según lo necesites
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')

    # Agregar la tabla a la figura
    table = ax.table(cellText=df.values, colLabels=df.columns,
                     cellLoc='center', loc='center')

    # Ajustar el tamaño de la fuente de la tabla
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)  # Ajustar el escalado de la tabla si es necesario

    # Guardar la imagen de la tabla
    plt.savefig('assets/graficas/words_by_category_table.png',
                bbox_inches='tight')


def graficate_publisher(data):
    publisher = {}

    for entry in data:
        if 'publisher' in entry:
            publisher[entry['publisher']] = publisher.get(entry['publisher'], 0) + 1

    # Ordenar los publishers por el número de apariciones en orden descendente
    sorted_publisher = sorted(publisher.items(), key=lambda x: x[1], reverse=True)

    # Desempaquetar los datos
    publishers, count_publishers = zip(*sorted_publisher)

    # Ajustar los nombres de los publishers largos con saltos de línea
    publishers_wrapped = [textwrap.fill(pub, width=30) for pub in publishers]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(24, 20))
    plt.title('Top Publishers')
    plt.xlabel('Count')
    plt.ylabel('Publishers')

    # Crear una paleta de colores distinta para cada barra
    cmap = cm.get_cmap('tab20', len(publishers))
    colors = [cmap(i) for i in range(len(publishers))]

    # Crear el gráfico de barras horizontal con colores individuales
    bars = ax.barh(publishers_wrapped, count_publishers, color=colors)

    # Añadir el valor al final de cada barra
    for bar, count in zip(bars, count_publishers):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, str(count),
                va='center', ha='left', fontsize=10)

    # Invertir el eje y para que el publisher con más citaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que no se corte
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Guardar la figura
    plt.savefig('assets/graficas/publishers.png')
    plt.show()

def graficate_top_cited(data):
    citations = {}

    # Extraer el número de citaciones del campo "note"
    for entry in data:
        if 'note' in entry:
            note = entry['note']
            # Usar una expresión regular para extraer el número de citaciones
            match = re.search(r'Cited by:\s*(\d+)', note)
            if match:
                citation_count = int(match.group(1))
                # Almacenar el título y el número de citaciones
                title = entry.get('title', 'Unknown Title')
                citations[title] = citation_count

    # Ordenar los artículos por el número de citaciones en orden descendente y tomar los 15 primeros
    top_cited = sorted(citations.items(), key=lambda x: x[1], reverse=True)[:15]

    # Desempaquetar los títulos y las citaciones
    titles, counts = zip(*top_cited)

    # Envolver títulos largos para mejorar la legibilidad
    wrapped_titles = [textwrap.fill(title, width=50) for title in titles]

    # Crear la gráfica de barras
    fig, ax = plt.subplots(figsize=(12, 10))  # Tamaño ajustado para mejorar la legibilidad
    colors = cm.get_cmap('tab20', len(counts))(range(len(counts)))  # Colores individuales para cada barra
    bars = ax.barh(wrapped_titles, counts, color=colors)
    ax.invert_yaxis()  # El artículo más citado estará en la parte superior

    plt.title('Top 15 Most Cited Articles', fontsize=16)
    plt.xlabel('Number of Citations', fontsize=14)
    plt.ylabel('Articles', fontsize=14)

    # Ajuste de etiquetas
    ax.tick_params(axis='y', labelsize=10)  # Tamaño de las etiquetas del eje Y

    # Ajuste del espaciado para evitar superposiciones
    plt.tight_layout()

    # Añadir una leyenda (opcional, si se desea indicar la posición)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 400, bar.get_y() + bar.get_height()/2,  # Ajuste de posición
                f'{count}', ha='center', va='center', fontsize=10, color='black')

    # Guardar la figura
    plt.savefig('assets/graficas/top_cited_articles.png', bbox_inches='tight')
    plt.show()



    
    

def graficate_type_year(data):
    type_year_count = {}

    # Contar la cantidad de publicaciones por tipo y año
    for entry in data:
        if 'type' in entry and 'year' in entry:
            # Convertir el tipo a minúsculas para evitar duplicados como "article" y "Article"
            pub_type = entry['type'].strip().lower()
            # Extraer solo los caracteres numéricos del año
            year = re.sub(r'\D', '', entry['year'])
            if year:
                year = int(year)
                type_year_count[(pub_type, year)] = type_year_count.get(
                    (pub_type, year), 0) + 1

    # Convertir el diccionario a un DataFrame de pandas para facilitar la visualización
    df = pd.DataFrame.from_dict(type_year_count, orient='index', columns=['Count']).reset_index()
    df[['Type', 'Year']] = pd.DataFrame(df['index'].tolist(), index=df.index)
    df = df.drop(columns='index')

    # Mostrar solo los últimos 35 años
    df = df[df['Year'] >= (max(df['Year']) - 35)]

    # Pivotar el DataFrame para que los tipos de publicaciones sean columnas
    df_pivot = df.pivot(index='Year', columns='Type', values='Count').fillna(0)

    # Crear la gráfica de barras apiladas
    df_pivot.plot(kind='bar', stacked=True, figsize=(18, 8), colormap='tab20')

    plt.title('Publications by Type and Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.legend(title='Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)

    # Guardar la figura
    plt.tight_layout()
    plt.savefig('assets/graficas/type_year.png')
    


def graficate_author_database(data):
    author_database_count = {}

    for entry in data:
        if 'author' in entry and entry['author'].strip() and 'database' in entry:
            # Obtener solo el primer autor y formatear
            first_author = entry['author'].split(' and ')[0].strip()
            parts = first_author.split()
            if parts and parts[0]:
                formatted_author = f"{parts[0][0].lower()}. {' '.join(
                    parts[1:])}".lower() if len(parts) > 1 else parts[0].lower()
            else:
                formatted_author = "unknown"

            database = entry['database'].strip()

            # Contar las publicaciones por autor y base de datos
            if formatted_author not in author_database_count:
                author_database_count[formatted_author] = {}
            author_database_count[formatted_author][database] = author_database_count[formatted_author].get(
                database, 0) + 1

    # Limitar a los 15 autores más mencionados
    top_authors = sorted(author_database_count.keys(), key=lambda author: sum(
        author_database_count[author].values()), reverse=True)[:15]

    # Crear la matriz de conteo
    databases = list(set(db for counts in author_database_count.values()
                     for db in counts.keys()))
    count_matrix = np.zeros((len(top_authors), len(databases)))

    for i, author in enumerate(top_authors):
        for j, db in enumerate(databases):
            count_matrix[i, j] = author_database_count[author].get(db, 0)

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(18, 10))
    colors = plt.cm.tab20.colors  # Usar una paleta de colores

    # Graficar cada base de datos como una barra apilada en cada autor
    for j, db in enumerate(databases):
        ax.barh(top_authors, count_matrix[:, j], label=textwrap.fill(db, width=15), left=np.sum(
            count_matrix[:, :j], axis=1), color=colors[j % len(colors)])

    plt.title('Top 15 Authors by Database')
    plt.xlabel('Number of Publications')
    plt.ylabel('Authors')
    ax.invert_yaxis()
    plt.xticks(rotation=45)
    plt.legend(title='Database', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Ajustar el espaciado para que la leyenda no se corte
    plt.tight_layout()

    # Guardar la figura
    plt.savefig('assets/graficas/author_database.png', bbox_inches='tight')

    plt.show()




def heatmap_author_journals(data, top_n_authors=20, top_n_journals=20, min_publications=2):
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt

    # Contador de publicaciones por autor y journal
    author_journal_count = {}
    for entry in data:
        if 'author' in entry and 'journal' in entry:
            first_author = entry['author'].split(' and ')[0].strip()
            parts = first_author.split()
            if parts and parts[0]:  # Verificar que parts no esté vacío y que parts[0] tenga contenido
                formatted_author = f"{parts[0][0].lower()}. {' '.join(parts[1:])}".lower() if len(parts) > 1 else parts[0].lower()
            else:
                formatted_author = "unknown"  # Valor predeterminado si no hay autor válido

            journal = entry['journal'].strip()

            if journal not in author_journal_count:
                author_journal_count[journal] = {}
            author_journal_count[journal][formatted_author] = author_journal_count[journal].get(formatted_author, 0) + 1

    # Convertir a DataFrame para la visualización en el heatmap
    df = pd.DataFrame(author_journal_count).fillna(0)

    # Filtrar los autores y journals con más de 'min_publications' publicaciones
    filtered_journals = df.columns[(df > 0).sum(axis=0) >= min_publications]
    filtered_authors = df.index[(df > 0).sum(axis=1) >= min_publications]
    df_filtered = df.loc[filtered_authors, filtered_journals]

    # Limitar el número de autores y journals a los top_n más relevantes
    top_journals = df_filtered.sum(axis=0).sort_values(ascending=False).head(top_n_journals).index
    top_authors = df_filtered.sum(axis=1).sort_values(ascending=False).head(top_n_authors).index
    df_filtered = df_filtered.loc[top_authors, top_journals]

    # Verificar si la matriz filtrada no está vacía
    if df_filtered.empty:
        print("No hay suficientes datos para generar un heatmap poblado.")
        return

    # Crear el heatmap
    plt.figure(figsize=(15, 10))
    sns.heatmap(df_filtered, annot=True, fmt="g", cmap='viridis')
    plt.title('Publications by Author and Journal')
    plt.xlabel('Journals')
    plt.ylabel('Authors')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Guardar la figura
    plt.savefig('assets/graficas/author_journal_heatmap.png')
    plt.show()



def stacked_bar_journal_entry_type_inverted(data, top_n_journals=10):
    # Crear un diccionario para contar las publicaciones por journal y tipo de entrada
    journal_type_count = {}

    for entry in data:
        if 'journal' in entry and 'type' in entry:
            journal = entry['journal']
            entry_type = entry['type'].lower()  # Normalizar el tipo a minúsculas
            if journal not in journal_type_count:
                journal_type_count[journal] = {}
            journal_type_count[journal][entry_type] = journal_type_count[journal].get(entry_type, 0) + 1

    # Convertir a DataFrame
    df = pd.DataFrame(journal_type_count).fillna(0)

    # Seleccionar los journals con más publicaciones
    top_journals = df.sum(axis=0).sort_values(ascending=False).head(top_n_journals).index
    df_top = df[top_journals].fillna(0)

    # Transponer el DataFrame para tener los journals en el eje Y y los tipos en el eje X
    df_top = df_top.transpose()

    # Crear colores para cada tipo de entrada
    entry_types = df_top.columns
    cmap = plt.get_cmap('tab20', len(entry_types))
    colors = [cmap(i) for i in range(len(entry_types))]

    # Crear el gráfico de barras apiladas con ejes invertidos
    ax = df_top.plot(kind='barh', stacked=True, figsize=(10, 12), color=colors, edgecolor='black')

    # Etiquetas y título
    plt.title(f'Top {top_n_journals} Journals by Publication Type')
    plt.ylabel('Journals')
    plt.xlabel('Number of Publications')

    # Mostrar la leyenda y ajustar el layout
    plt.legend(title='Entry Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Guardar la figura
    plt.savefig('assets/graficas/top_journals_by_entry_type_inverted.png', bbox_inches='tight')
    plt.show()
    

def heatmap_journal_entry_type_wrapped(data, top_n_journals=10):
    # Crear un diccionario para contar las publicaciones por journal y tipo de entrada
    journal_type_count = {}

    for entry in data:
        if 'journal' in entry and 'type' in entry:
            # Eliminar todo lo que esté dentro de paréntesis en el nombre del journal
            journal = re.sub(r'\(.*?\)', '', entry['journal']).strip()
            entry_type = entry['type'].lower()  # Normalizar el tipo a minúsculas
            if journal not in journal_type_count:
                journal_type_count[journal] = {}
            journal_type_count[journal][entry_type] = journal_type_count[journal].get(entry_type, 0) + 1

    # Convertir a DataFrame
    df = pd.DataFrame(journal_type_count).fillna(0)

    # Filtrar para eliminar tanto las filas como las columnas que contienen solo ceros
    df = df.loc[(df != 0).any(axis=1), (df != 0).any(axis=0)]

    # Seleccionar los journals con más publicaciones
    top_journals = df.sum(axis=0).sort_values(ascending=False).head(top_n_journals).index
    df_top = df[top_journals].fillna(0)

    # Transponer el DataFrame para tener los journals en el eje X y los tipos en el eje Y
    df_top = df_top.transpose()

    # Envolver los nombres de los journals para mejorar la legibilidad
    journals_wrapped = [textwrap.fill(journal, width=12) for journal in df_top.columns]
    df_top.columns = journals_wrapped

    # Crear el mapa de calor
    plt.figure(figsize=(15, 10))
    sns.heatmap(df_top, annot=True, cmap="YlGnBu", fmt=".0f", linewidths=.5, cbar_kws={'label': 'Number of Publications'})
    plt.title(f'Top {top_n_journals} Journals by Publication Type (Heatmap)')
    plt.xlabel('Journals')
    plt.ylabel('Entry Types')

    # Ajustar el espaciado de los elementos visuales para una mejor visualización
    plt.xticks(rotation=45, ha='right')  # Inclinar etiquetas en el eje X
    plt.yticks(rotation=0)  # Alinear las etiquetas del eje Y horizontalmente
    plt.tight_layout()

    # Guardar la figura
    plt.savefig('assets/graficas/journal_article.png', bbox_inches='tight')
    plt.show()