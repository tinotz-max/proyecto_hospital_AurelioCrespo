from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # ====== PASO 1: INICIO DE SESIÓN ======
    print("Abriendo la página de login...")
    driver.get("http://127.0.0.1:8000/accounts/login/")
    
    # Espera inteligente: Esperamos a que el cuadro de usuario aparezca en pantalla
    usuario_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_to_be_clickable((By.ID, "id_username"))
    )
    usuario_input.send_keys("SantinoT")  # Poné tu usuario administrador real
    
    clave_input = driver.find_element(By.ID, "id_password")
    clave_input.send_keys("SantinoT")  # Poné tu contraseña real
    
    driver.find_element(By.TAG_NAME, "button").click()
    print("Login enviado, esperando procesamiento de Django...")
    time.sleep(3)

    # ====== PASO 2: IR AL FORMULARIO DE SUPERVISOR ======
    # IMPORTANTE: Asegurate en tu navegador que la URL sea exactamente esta, 
    # si tu app se llama 'usuarios' cambiala por 'http://127.0.0.1:8000/usuarios/nuevo/'
    url_formulario = "http://127.0.0.1:8000/inventario/supervisores/nuevo/"
    print(f"Redirigiendo el robot a: {url_formulario}")
    driver.get(url_formulario)
    time.sleep(2)

    # ====== PASO 3: COMPLETAR EL FORMULARIO (Tu forms.py) ======
    print("Completando los campos del SupervisorForm...")
    driver.find_element(By.ID, "id_username").send_keys("valentin_supervisor")
    driver.find_element(By.ID, "id_password").send_keys("ClaveSegura123!")
    driver.find_element(By.ID, "id_email").send_keys("valentin@hospital.com")
    driver.find_element(By.ID, "id_legajo").send_keys("LEG-9942")
    driver.find_element(By.ID, "id_rol").send_keys("Supervisor")
    time.sleep(2)

    # ====== PASO 4: ENVIAR Y GUARDAR ======
    print("Esperando a que el botón de envío sea interactuable...")
    boton_guardar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    boton_guardar.click()
    time.sleep(3)

    print("✅ TEST EXITOSO: El robot completó el formulario de Perfil y registró al Supervisor sin trabarse.")

except Exception as e:
    print(f"❌ TEST FALLIDO: Ocurrió un problema en la simulación. Motivo: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()