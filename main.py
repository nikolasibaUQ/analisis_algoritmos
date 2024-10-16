
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



#download_dir = "/Users/NicolasCw/Desktop/desarrollo/analisis_algoritmos/assets" 
#TODO: cambiar la ruta de descarga dependiendo del sistema 
# operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto
download_dir = r"E:\celuweb\analisis_algoritmos\assets"  # Cambia a la ruta correcta


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
driver.get("https://www-scopus-com.crai.referencistas.com/search/form.uri?display=basic#basic")

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




# time.sleep(20)
driver.implicitly_wait(20)

# Buscar el campo de búsqueda
input_element = driver.find_element(by=By.CLASS_NAME, value="styleguide-input-module___SqPU")
print('encontrado')
input_element.send_keys("computational thinking")
print('escrito')



#presionar boton buscar
search_button = driver.find_element(by=By.XPATH, value="//button[span[text()='Search']]")
search_button.click()

driver.implicitly_wait(15)
element = driver.find_element("xpath", '//input[@aria-label="from"]')
element.send_keys('2020')

element2 = driver.find_element("xpath", '//input[@aria-label="to"]')
element2.send_keys('')
element2.send_keys('2024')

time.sleep(1)
search_button = driver.find_element(by=By.XPATH, value="//button[span[text()='Search']]")
search_button.click()
time.sleep(1)

apply_button = driver.find_element(By.XPATH, "//button[@data-testid='apply-facet-range']")
apply_button.click()





documents =  driver.find_element(by= By.CLASS_NAME , value='SearchResultsHeader-module__Qq2ZF' )  
print ('numero de documentos:' + documents.text)
data = re.findall(r'\d+', documents.text.replace(',',''))
docs = int(data[0])
print('numero de documentos:  '+ str(docs))

time.sleep(5)

dropdown = driver.find_element(by=By.XPATH, value="//button[span[text()='Export']]")
print('encontrado')
dropdown.click()
print('click')

time.sleep(5)

csv = driver.find_element(by=By.XPATH, value="//button[span[text()='CSV']]")
print('encontrado')
csv.click()
print('click')
    
radioButtom = driver.find_element(by=By.ID, value="select-range")
radioButtom.click()
    
fromData = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="From"]')
fromData.send_keys('1')
    
    
toData = driver.find_element(By.CSS_SELECTOR, value="input[placeholder=To]")
toData.send_keys(str(docs))
    
time.sleep(2)
submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='submit-export-button']")
if submit_button.is_enabled():
    submit_button.click()

time.sleep(10)

progress_bar = driver.find_element(By.CSS_SELECTOR, "progress.PercentageBar-module__98Jio")
percent = float(progress_bar.get_attribute("value"))

while percent < 100:
    time.sleep(1)
    try:
        progress_bar = driver.find_element(By.CSS_SELECTOR, "progress.PercentageBar-module__98Jio")
        percent = float(progress_bar.get_attribute("value"))
    
        print('valor: ' + str(percent))
    except:
        percent = 100
        break
    
time.sleep(5)
     
# Espera implícita para el resto de la página

driver.quit()






