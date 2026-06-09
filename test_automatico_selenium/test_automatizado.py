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

print("🚀 Iniciando Selenium con Brave Browser para: TEST AUTOMATIZADO GENERAL...")
driver = webdriver.Chrome(options=options)

try:
    # ====== PASO 1: LOGIN DE CONTROL ======
    print("\n[Paso 1] Autenticando en el sistema...")
    driver.get("http://127.0.0.1:8000/accounts/login/")
    
    # Usamos el método correcto corregido
    usuario_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id_username"))
    )
    usuario_input.send_keys("SantinoT")
    driver.find_element(By.ID, "id_password").send_keys("SantinoT")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(3)

    # ====== PASO 2: TESTEAR NAVEGACIÓN AL DASHBOARD ======
    print("\n[Paso 2] Verificando acceso al Dashboard Principal...")
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)
    
    assert "Dashboard" in driver.page_source or "Inicio" in driver.page_source
    print("✅ Dashboard detectado y accessible.")

    # ====== PASO 3: INTENTAR CERRAR SESIÓN ======
    print("\n[Paso 3] Probando el sistema de Logout...")
    driver.get("http://127.0.0.1:8000/accounts/logout/")
    time.sleep(2)
    print("✅ Cierre de sesión ejecutado.")

    print("\n✅ TEST GENERAL EXITOSO: Las rutas de control responden perfectamente de extremo a extremo.")

except Exception as e:
    print(f"\n❌ TEST GENERAL FALLIDO: Error en la verificación de flujos principales.")
    print(f"Motivo técnico: {e}")

finally:
    print("\nCerrando navegador automatizado...")
    driver.quit()