import os
# Desactivamos el modo offline para que Selenium use las configuraciones del sistema
# os.environ["SE_OFFLINE"] = "true"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Configuración nativa para Linux Zorin OS usando Brave Browser
options = Options()
options.binary_location = "/usr/bin/brave-browser"
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-allow-origins=*")

print("🚀 Iniciando Selenium con Brave Browser para: TEST SUPERVISORES...")
driver = webdriver.Chrome(options=options)

try:
    # ====== PASO 1: INICIO DE SESIÓN ======
    print("\n[Paso 1] Abriendo la página de login...")
    driver.get("http://127.0.0.1:8000/accounts/login/")
    
    print("Esperando la carga del formulario de login...")
    # PARCHEADO: Cambiado a element_to_be_clickable (el método correcto de Selenium)
    usuario_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id_username"))
    )
    usuario_input.send_keys("SantinoT")
    
    clave_input = driver.find_element(By.ID, "id_password")
    clave_input.send_keys("SantinoT")
    
    print("Enviando credenciales...")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(3)

    # ====== PASO 2: NAVEGAR AL FORMULARIO DE SUPERVISOR ======
    url_formulario = "http://127.0.0.1:8000/usuarios/supervisores/nuevo/"
    print(f"\n[Paso 2] Redirigiendo el robot a: {url_formulario}")
    driver.get(url_formulario)
    time.sleep(2)

    # ====== PASO 3: COMPLETAR EL FORMULARIO DE SUPERVISOR ======
    print("\n[Paso 3] Completando los campos del SupervisorForm...")
    driver.find_element(By.ID, "id_username").send_keys("ValentinM")
    driver.find_element(By.ID, "id_password").send_keys("ValentinM123")
    driver.find_element(By.ID, "id_email").send_keys("valentin@hospital.com")
    driver.find_element(By.ID, "id_legajo").send_keys("LEG-9942")
    driver.find_element(By.ID, "id_rol").send_keys("SUPERVISOR")
    time.sleep(2)

    # ====== PASO 4: ENVIAR Y GUARDAR ======
    print("\n[Paso 4] Localizando botón de guardado...")
    boton_guardar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    print("Haciendo clic en 'Guardar'...")
    boton_guardar.click()
    time.sleep(3)

    print("\n✅ TEST EXITOSO: El robot completó el ABML de supervisores sin trabas en Brave.")

except Exception as e:  
    print(f"\n❌ TEST FALLIDO: Se interrumpió la simulación de Supervisores.")
    print(f"Motivo técnico: {e}")

finally:
    print("\nFinalizando proceso de prueba...")
    driver.quit()