# Proyecto de Scraping y Análisis Bibliométrico 

Este proyecto tiene como objetivo la implementación de técnicas de busqueda 🔍 para la descarga de archivos BibTeX desde cuatro bases de datos: **Scopus**, **IEEE**, **ScienceDirect** y **SAGE**. Posteriormente, se realizan análisis 📊 y se generan diversos reportes 📈 según una serie de requerimientos funcionales.

## Requerimientos Funcionales

1. **Unificación de datos**: Integrar y unificar la información descargada de las bases de datos en una única fuente que garantice la completitud de los datos 🗒️ y evite duplicados ❌.
2. **Estadísticos descriptivos**:
   - 👤 Primer autor del producto (15 autores más citados).
   - 📅 Año de publicación.
   - 📑 Tipo de producto (artículos, conferencias, capítulos de libro).
   - 🏢 Afiliación del primer autor (institución).
   - 📑 Journal y publisher.
   - 📂 Base de datos.
   - ⬆️🔹 Cantidad de citaciones por artículo (15 artículos más citados).
   - ⚙️ Consultas combinadas entre las variables.
3. **Análisis de abstracts**: Frecuencia de aparición de variables clave 🧰 relacionadas con habilidades, conceptos computacionales, actitudes, etc., identificando sinónimos 🛠️.
4. **Nube de palabras**: Generación de una nube de palabras ☁️ basada en el contenido de los abstracts.
5. **Análisis de journals**: Identificación de los 10 journals con más publicaciones y un grafo 🔀 que muestre la relación con los artículos más citados y el país 🌍 de afiliación del primer autor.
6. **Despliegue del proyecto**: La aplicación debe estar desplegada 🛠️ en un entorno accesible.

## Instalación del Entorno Virtual

Es recomendable instalar un entorno virtual 🔧 para mantener las dependencias del proyecto aisladas. A continuación, se explican los pasos para configurar un entorno virtual tanto en macOS como en Windows.

### macOS/Linux
1. 💻 Abre una terminal.
2. 🔍 Navega al directorio de tu proyecto.
3. Crea un entorno virtual con:
   ```bash
   python3 -m venv env
   ```
4. ⚡ Activa el entorno virtual:
   ```bash
   source env/bin/activate
   ```
5. ⬇️ Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Windows
1. 💻 Abre una ventana de **PowerShell** o **CMD**.
2. 🔍 Navega al directorio de tu proyecto.
3. Crea un entorno virtual con:
   ```bash
   python -m venv env
   ```
4. ⚡ Activa el entorno virtual:
   ```bash
   .\env\Scripts\activate
   ```
5. ⬇️ Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Archivo `requirements.txt`
El archivo `requirements.txt` contiene todas las bibliotecas necesarias para ejecutar el proyecto, entre las cuales se encuentran:
- `matplotlib` 🎨
- `selenium` 🚗
- `bibtexparser` 🔖
- `webdriver_manager` 🚧
- y otras dependencias necesarias para la manipulación y análisis de datos 📊.

## Uso
1. Asegúrate de que el entorno virtual esté activado ⚡.
2. Ejecuta los scripts de scraping 🔍 para descargar los archivos BibTeX de las bases de datos 📂.
3. Realiza el análisis de los datos según los requerimientos 🗒️ y genera los reportes y gráficas 📈 correspondientes.


