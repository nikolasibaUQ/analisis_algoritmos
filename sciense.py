
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv


load_dotenv()



download_dir = "/Users/NicolasCw/Desktop/desarrollo/analisis_algoritmos/assets" 
#TODO: cambiar la ruta de descarga dependiendo del sistema 
# operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto 
# download_dir = r"E:\celuweb\analisis_algoritmos\assets"  # Cambia a la ruta correcta#


def wait_for_downloads(download_dir):
    # Esperar mientras haya archivos con la extensión ".crdownload"
    while any([filename.endswith(".crdownload") for filename in os.listdir(download_dir)]):
        print("Esperando a que la descarga termine...")
        time.sleep(1)  # Espera un segundo antes de volver a comprobar
        

    print("Descarga completa.")

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
driver.get("https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking")

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

results_per_page_100 = driver.find_element(By.CSS_SELECTOR, "a[data-aa-name='srp-100-results-per-page']")
results_per_page_100.click()

checkbox = driver.find_element(By.ID, "select-all-results")
checkbox.click()


export_btn = driver.find_element(By.XPATH, '//*[@id="srp-toolbar"]/div[1]/span/span[1]/div[3]/button')
export_btn.click()




time.sleep(40)


# <div class="checkbox SelectAllCheckbox"><label class="checkbox-label" for="select-all-results"><input id="select-all-results" type="checkbox" class="checkbox-input" aria-checked="false" aria-disabled="false" aria-label="Select all articles for download" autocomplete="off"><span class="checkbox-check"></span><span class="checkbox-label-value">Select all articles</span></label></div>