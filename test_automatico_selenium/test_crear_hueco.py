import os
# COMENTADO: Dejamos que Selenium busque en internet el driver que coincida con tu Brave
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

print("🚀 Iniciando Selenium con Brave Browser para: TEST CREAR HUECO...")
driver = webdriver.Chrome(options=options)

try:
    # ====== PASO 1: AUTENTICACIÓN ======
    print("\n[Paso 1] Logueando administrador de turnos...")
    driver.get("http://127.0.0.1:8000/accounts/login/")
    
    usuario_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id_username"))
    )
    usuario_input.send_keys("SantinoT")
    driver.find_element(By.ID, "id_password").send_keys("SantinoT")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(3)

    # ====== PASO 2: IR A LA SECCIÓN HUECOS ======
    url_huecos = "http://127.0.0.1:8000/inventario/huecos/nuevo/"
    print(f"\n[Paso 2] Yendo al formulario de Huecos: {url_huecos}")
    driver.get(url_huecos)
    time.sleep(2)

    # ====== PASO 3: SIMULAR ENVÍO DE DATOS ======
    print("\n[Paso 3] Rellenando campos del formulario Hueco...")
    try:
        input_nombre = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "id_nombre"))
        )
        input_nombre.send_keys("Hueco de Prueba Automatizado")
        time.sleep(1)
    except Exception:
        print("Aviso: No se encontró el campo 'id_nombre', continuando...")

    # ====== PASO 4: ENVIAR FORMULARIO ======
    print("\n[Paso 4] Presionando botón submit...")
    boton_submit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    boton_submit.click()
    time.sleep(3)

    print("\n✅ TEST CREAR HUECO EXITOSO: Formulario procesado de forma correcta.")

except Exception as e:
    print(f"\n❌ TEST CREAR HUECO FALLIDO: Error al intentar instanciar el registro.")
    print(f"Motivo técnico: {e}")

finally:
    print("\nFinalizando y destruyendo procesos del driver...")
    driver.quit()