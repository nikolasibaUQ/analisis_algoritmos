
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv

def donwloadData():
    load_dotenv()



    download_dir = "/Users/NicolasCw/Desktop/desarrollo/analisis_algoritmos/assets" 
    #TODO: cambiar la ruta de descarga dependiendo del sistema 
    # operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto 
    # download_dir = r"E:\celuweb\analisis_algoritmos\assets\IEEE"  # Cambia a la ruta correcta#

    

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Carpeta de descargas
    "download.prompt_for_download": False,  # No mostrar cuadros de diálogo
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "profile.default_content_settings.popups": 0  # Deshabilitar ventanas emergentes para descargas
    })



    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


    # Abrir la página
    driver.get("https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=computational%20thinking")

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
    element = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    element.send_keys(os.getenv('PSWD'))
# Hacer clic en el botón "Siguiente"2
    element = driver.find_element(by=By.XPATH, value='//*[@id="passwordNext"]/div/button')
    element.click()

    driver.implicitly_wait(10)

# results_per_page_100 = driver.find_element(By.CSS_SELECTOR, "a[data-aa-name='srp-100-results-per-page']")
# results_per_page_100.click()


    time.sleep(25)


    total_results_span = driver.find_element(By.XPATH, "(//span[@class='strong'])[2]")
# Extraer el texto del elemento
    total_results = total_results_span.text.replace(",", "")

    max_pages = int(total_results)/25
    i = 1


    while i <= int(max_pages):
        checkbox = driver.find_element(By.CLASS_NAME, 'results-actions-selectall')
        checkbox.click()

        export_btn = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[1]/ul/li[3]/xpl-export-search-results')
        export_btn.click()
        if i == 1:
            citation_btn = driver.find_element(By.XPATH, '//*[@id="ngb-nav-0"]')
            citation_btn.click()

        time.sleep(2)

        radio_button = driver.find_element(By.CSS_SELECTOR, "label[for='download-bibtex'] input")
        radio_button.click()

        radio_type = driver.find_element(By.CSS_SELECTOR, "label[for='citation-abstract'] input")
        radio_type.click()


        download_button = driver.find_element(By.CSS_SELECTOR, "button.stats-SearchResults_Citation_Download")
        download_button.click()

        time.sleep(2)


    #  Localizar el ícono
        close_icon = driver.find_element(By.CSS_SELECTOR, "i.fas.fa-times")

    # Usar JavaScript para forzar el clic en el ícono
        driver.execute_script("arguments[0].click();", close_icon)
        print('cerrando ventana')
        close_icon = driver.find_element(By.CSS_SELECTOR, "i.fas.fa-times")

        close_icon.click()

        try:
            next_button = driver.find_element(By.XPATH, "//button[contains(text(), '>')]")

    # Hacer clic en el botón "Next"
            next_button.click()
        except:
            print('No hay mas paginas')
            break
        i += 1
        time.sleep(4)


    time.sleep(20)



