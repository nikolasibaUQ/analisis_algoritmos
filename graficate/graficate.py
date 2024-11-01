
import re
from typing import List
import matplotlib.pyplot as plt
import data_models.normal_data as nd


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
    count_journals = {}
    for entry in data:
        if 'journal' in entry:
            
            journals[entry['journal']] = journals.get(entry['journal'], 0) + 1

    # Crear una lista con los tipos de entradas y sus conteos
    journals, count_journals = zip(*journals.items())

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title('Journals')
    plt.xlabel('Journals')
    plt.ylabel('Count')

    # Crear el gráfico de barras horizontal
    ax.barh(journals, count_journals, color='purple')

    # Guardar la figura
    plt.savefig('assets/graficas/journals.png')
