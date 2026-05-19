from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1. Abrir el navegador (Chrome/Chromium en Linux)
driver = webdriver.Chrome()

try:
    # 2. Ir a la página de login de tu servidor Django
    driver.get("http://127.0.0.1:8000/accounts/login/")
    time.sleep(2) # Pausa de 2 segundos para ver qué hace

    # 3. Buscar el cuadro de "Nombre de usuario" (por su ID de Django) e ingresar texto
    input_usuario = driver.find_element(By.ID, "id_username")
    input_usuario.send_keys("SantinoT") # Poné acá un usuario real que creaste
    time.sleep(1)

    # 4. Buscar el cuadro de "Contraseña" e ingresar texto
    input_clave = driver.find_element(By.ID, "id_password")
    input_clave.send_keys("SantinoT") # Poné la clave de ese usuario
    time.sleep(1)

    # 5. Buscar el botón de entrar y hacer clic
    boton_entrar = driver.find_element(By.TAG_NAME, "button")
    boton_entrar.click()
    time.sleep(3) # Pausa para ver si entramos al Dashboard

    # 6. Validar si entramos correctamente revisando la URL actual
    if "dashboard" in driver.current_url:
        print("✅ TEST EXITOSO: El robot se logueó y entró al Dashboard correctamente.")
    else:
        print("❌ TEST FALLIDO: No se pudo iniciar sesión.")

finally:
    # 7. Cerrar el navegador automáticamente al terminar
    driver.quit()   