
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

# Abrir la página
driver.get("https://www-scopus-com.crai.referencistas.com/search/form.uri?display=basic#basic")

# Espera implícita para cargar elementos de la página
driver.implicitly_wait(30)

# Buscar y hacer clic en el botón para iniciar sesión con Google
element = driver.find_element(by=By.ID, value="btn-google")
element.click()

# Buscar el campo de correo electrónico
element = driver.find_element(by=By.ID, value="identifierId")
element.send_keys("nicolasr.ibanezp@uqvirtual.edu.co")

# Hacer clic en el botón "Siguiente"
element = driver.find_element(by=By.ID, value="identifierNext")
element.click()

#mostarr alerta ingrese la contraseña 
# show_alert()


time.sleep(5)
# Buscar el campo de búsqueda
input_element = driver.find_element(by=By.CLASS_NAME, value="styleguide-input-module___SqPU")
print('encontrado')
input_element.send_keys("algoritmos")
print('escrito')



#presionar boton buscar
search_button = driver.find_element(by=By.XPATH, value="//button[span[text()='Search']]")
search_button.click()

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

submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='submit-export-button']")
if submit_button.is_enabled():
    submit_button.click()


time.sleep(10)





# Espera implícita para el resto de la página
driver.implicitly_wait(10)




