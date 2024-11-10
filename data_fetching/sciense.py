
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv


load_dotenv()


def download_sciense_articles():
    # TODO: cambiar la ruta de descarga dependiendo del sistema
    # operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto
    download_dir = "/Users/NicolasCw/Desktop/desarrollo/analisis_algoritmos/assets/sciense"
    # download_dir = r"E:\celuweb\analisis_algoritmos\assets\sciense"  # Cambia a la ruta correcta#

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Carpeta de descargas
        "download.prompt_for_download": False,  # No mostrar cuadros de diálogo
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        # Deshabilitar ventanas emergentes para descargas
        "profile.default_content_settings.popups": 0
    })

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)


# Abrir la página
    driver.get(
        "https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking&show=100")

# Espera implícita para cargar elementos de la página
# driver.implicitly_wait(10)

# Buscar y hacer clic en el botón para iniciar sesión con Google
    element = driver.find_element(by=By.ID, value="btn-google")
    element.click()

    # Buscar el campo de correo electrónico
    element = driver.find_element(by=By.ID, value="identifierId")
    element.send_keys(os.getenv('EMAIL'))

  # Hacer clic en el botón "Siguiente"
    element = driver.find_element(by=By.ID, value="identifierNext")
    element.click()

    time.sleep(5)
    element = driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    element.send_keys(os.getenv('PSWD'))
# Hacer clic en el botón "Siguiente"2
    element = driver.find_element(
        by=By.XPATH, value='//*[@id="passwordNext"]/div/button')
    element.click()

    driver.implicitly_wait(10)

# results_per_page_100 = driver.find_element(By.CSS_SELECTOR, "a[data-aa-name='srp-100-results-per-page']")
# results_per_page_100.click()

    pagination_info = driver.find_element(
        By.CSS_SELECTOR, "ol#srp-pagination li")

# Extraer el texto del elemento
    pagination_text = pagination_info.text

# Extraer el número máximo de páginas del texto "Page 1 of 60"
# Dividimos la cadena para obtener el número final
    max_pages = pagination_text.split(' ')[-1]

    i = 1

    while i <= int(max_pages):
        # checkbox = driver.find_element(By.ID, "select-all-results")
        label = driver.find_element(
            By.CSS_SELECTOR, "label[for='select-all-results']")
        label.click()
    # checkbox.click()
        export_btn = driver.find_element(
            By.XPATH, '//*[@id="srp-toolbar"]/div[1]/span/span[1]/div[3]/button')
        export_btn.click()
        export_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-aa-button='srp-export-multi-bibtex']")
    # Hacer clic en el botón
        export_button.click()
        time.sleep(2)
    # driver.implicitly_wait(5)
        next_button = driver.find_element(
            By.CSS_SELECTOR, 'a[data-aa-name="srp-next-page"]')

# Forzar el clic en el botón "Next" utilizando JavaScript
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2)
        i += 1

    time.sleep(40)
