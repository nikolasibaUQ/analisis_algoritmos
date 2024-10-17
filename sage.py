

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from dotenv import load_dotenv


load_dotenv()



download_dir = "/Users/NicolasCw/Desktop/desarrollo/analisis_algoritmos/assets/sage" 
#TODO: cambiar la ruta de descarga dependiendo del sistema 
# operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto 
# download_dir = r"E:\celuweb\analisis_algoritmos\assets\sciense"  # Cambia a la ruta correcta#


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
driver.get("https://journals-sagepub-com.crai.referencistas.com/action/doSearch?AllField=computational+thinking&startPage=0&pageSize=20")

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
driver.implicitly_wait(10)

element = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
element.send_keys(os.getenv('PSWD'))
# Hacer clic en el botón "Siguiente"2
element = driver.find_element(by=By.XPATH, value='//*[@id="passwordNext"]/div/button')
element.click()

driver.implicitly_wait(10)
time.sleep(5)

# Localizar el elemento que contiene el número total de resultados (95214) por su clase
result_count_element = driver.find_element(By.CSS_SELECTOR, "span.result__count")

# Obtener el texto que contiene el número
result_count = result_count_element.text

# max_pages = int(result_count)/100 
i = 0
max_retries = 10  # Número máximo de reintentos por página
try:
    while i < 250:
        try:
            checkbox = driver.find_element(By.ID, "action-bar-select-all")

            # Asegurarse de que el checkbox esté marcado
            while not checkbox.is_selected():
                checkbox.click()
                time.sleep(2)
            
            print("Checkbox marcado.")
            if not checkbox.is_selected():
                print("Checkbox marcado.")  
                while not checkbox.is_selected():
                    checkbox.click()
                    time.sleep(2)
        
            # Continuar con el resto del código
            export = driver.find_element(By.CSS_SELECTOR, "a[data-id='srp-export-citations']")
            export.click()
    
            select_element = driver.find_element(By.ID, "citation-format")
            select = Select(select_element)
            time.sleep(3)
            select.select_by_value("bibtex") 
    
            time.sleep(2)
            try: 
                download_button = driver.find_element(By.CSS_SELECTOR, "a.download__btn")
                download_button.click()
            except:    
                wait = WebDriverWait(driver, 10)
                modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal__header")))

                close_button = modal.find_element(By.CSS_SELECTOR, "button.close")
                driver.execute_script("arguments[0].click();", close_button)    
    
            time.sleep(2)
            wait = WebDriverWait(driver, 10)
            modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal__header")))

            close_button = modal.find_element(By.CSS_SELECTOR, "button.close")
            driver.execute_script("arguments[0].click();", close_button)
    
            time.sleep(2)

            # Hacer clic en el botón "Next"
            next_button = driver.find_element(By.CSS_SELECTOR, "a[aria-label='next']")
            next_button.click()
            time.sleep(2)
            
            # Incrementar i solo si la iteración se completa sin errores
            i += 1
        
        except Exception as e:
            # Manejar la excepción, por ejemplo, registrar el error y reintentar
            print(f"Error en la página {i+1}: {str(e)}. Reintentando...")
            retries = 0
            while retries < max_retries:
                try:
                    # Intentar nuevamente después del error
                    time.sleep(5)
                    retries += 1
                    break  # Si tiene éxito, salir del bucle de reintentos
                except Exception as e:
                    print(f"Reintento {retries}/{max_retries} fallido: {str(e)}")
                    
            if retries == max_retries:
                print(f"No se pudo procesar la página {i+1} después de {max_retries} reintentos. Continuando...")
                i += 1  # Si no tuvo éxito después de reintentar, aumentar i y continuar
except Exception as e:
    print(f"Fin de la paginación o error crítico: {str(e)}")
    


# <div class="form-check article-actionbar__check-all"><input type="checkbox" name="markall" id="action-bar-select-all" value="1" class="form-check-input"><label for="action-bar-select-all" class="form-check-label"><span>Select all</span></label></div>