# 🤖 Guía del Agente de Inteligencia Artificial (AI Agent Guide)

¡Hola loco! Si estás leyendo esto, sos el agente de IA asignado para dar soporte, expandir o refactorizar el código de **ADA - Piloto Auto v5.0**. Ponete las pilas, leé este documento con atención y respetá las directrices técnicas y de comportamiento del proyecto.

---

## 🛠️ Resumen Rápido del Entorno de Desarrollo

*   **Lenguaje Base:** Python 3.11+
*   **Entorno Operativo:** Exclusivo Windows (utiliza librerías y comandos específicos del sistema operativo de Microsoft como controladores ODBC de Access y procesos de consola como `attrib`).
*   **Punto de Entrada Principal:** [ADA - Piloto Auto v5.py](file:///c:/Users/vdominguez/OneDrive%20-%20infoplazas/AnalizadorDB%20by_VicTorD/AnalizadorBDbyVicTor/ADA%20-%20Piloto%20Auto%20v5.0/ADA%20-%20Piloto%20Auto%20v5.py)
*   **Módulo de Persistencia Local:** [sucursales_history.py](file:///c:/Users/vdominguez/OneDrive%20-%20infoplazas/AnalizadorDB%20by_VicTorD/AnalizadorBDbyVicTor/ADA%20-%20Piloto%20Auto%20v5.0/sucursales_history.py)
*   **Ficheros Auxiliares Obligatorios:** `settings.json`, `credentials_gebilo.json`, `VicTor.ico`, `historial_sucursales.db`.

---

## 🚨 Reglas de Oro para Modificaciones (¡No te las saltes!)

1.  **No Modificar sin Permiso Explícito:**
    *   *REGLA CRÍTICA:* Leé e investigá todo lo que necesites, pero **NO MODIFIQUES NINGÚN ARCHIVO DE CÓDIGO** a menos que el usuario lo pida explícitamente en el chat.
2.  **Preservar la Lógica de Negocio y Extracción de Datos:**
    *   *REGLA CRÍTICA:* **JAMÁS toques la lógica de negocio ni la forma de extraer la data de las bases de datos de Access (fórmulas, pyodbc, etc.)** a menos que el usuario lo indique de manera explícita en el chat.
3.  **Cero Atribución de IA:**
    *   No agregues "Co-Authored-By", firmas, ni atribuciones de Inteligencia Artificial en los comentarios del código o mensajes de commit. Usá commits convencionales únicamente.
4.  **No Compilar Automáticamente:**
    *   No ejecutes comandos de PyInstaller para compilar el ejecutable a menos que se te indique directamente. Preservá los archivos `.spec` intactos.
5.  **Idioma y Tono del Chat:**
    *   Comunicate con el usuario utilizando **Español Rioplatense (voseo)**. Utilizá modismos como *"dale"*, *"fantástico"*, *"ponete las pilas"*, o *"buenísimo"* para mantener una comunicación fluida y cercana, demostrando compromiso y un alto estándar técnico.
6.  **Verificación Antes de Afirmar:**
    *   Si el usuario hace un reclamo sobre un supuesto bug o comportamiento, nunca digas *"sí, tenés razón"* de inmediato. Respondé con un **"dejame verificar"**, analizá el archivo y las trazas, y luego respondé con evidencia.

---

## 💻 Convenciones y Patrones en el Código

Si tenés que realizar modificaciones en el código, debés respetar los siguientes patrones ya establecidos:

### A. Preservación del Controlador ODBC de Access
La conexión a las bases de datos locales `.mdb` se realiza mediante la siguiente cadena de conexión exacta en `extraer_datos_db`:
```python
conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};PWD={password};'
```
*   **Aviso:** No intentes cambiar el controlador por integraciones puras de Python. La lectura de archivos `.mdb` con contraseñas en Windows requiere obligatoriamente el Microsoft Access Driver de 32 o 64 bits.

### B. Comando OneDrive-Safe
Cualquier función que acceda a archivos en directorios locales de OneDrive debe pasar primero por la función `asegurar_archivo_local`. Esta ejecuta de manera controlada el proceso `attrib +p [archivo]` en Windows para forzar la sincronización local asíncrona:
```python
subprocess.run(['attrib', '+p', archivo], check=True, shell=True)
```
*   **Regla:** Asegurá siempre la animación de la GUI viva pasándole la instancia de la aplicación `app_instance` a la función durante las esperas prolongadas.

### C. Lógica de Deduplicación de Datos
Cuando actualices los motores de subida a Google Sheets, tené en cuenta:
*   Las hojas de cálculo mensuales (`Los Santos`, `Chiriqui`, etc.) solo sobrescriben registros si el nuevo conteo de transacciones es **estrictamente mayor** al existente.
*   Los logs diarios de sincronización se filtran por sucursal y día, conservando únicamente la **última ejecución diaria** (`keep='last'`).

---

## 🔧 Guía de Mantenimiento y Puntos de Extensión

Cuando se te solicite realizar mejoras, típicamente trabajarás en:

1.  **Refactor del Envío SMTP (`enviar_correo_notificacion`):**
    *   Ubicación: `ADA - Piloto Auto v5.py` (Línea 699 aproximadamente).
    *   Cuidado: El correo utiliza un puerto `587` con TLS. Las contraseñas de las aplicaciones de Gmail (`password_app`) están en duro en el código por razones de simplicidad operativa actual. Si vas a abstraerlas a variables de entorno o archivos cifrados, recordá mantener un fallback seguro.
2.  **Gestión de Destinatarios de Correo (`create_recipients_tab`):**
    *   Ubicación: `ADA - Piloto Auto v5.py` (Línea 1167 aproximadamente).
    *   Detalle: Maneja edición interactiva por doble clic sobre las filas de la tabla de tkinter (`Treeview`). Cualquier cambio en esta vista debe guardarse de inmediato en el fichero local invocando a `self.save_settings()`.
3.  **Esquemas de SQLite (`sucursales_history.py`):**
    *   Ubicación: Módulo independiente.
    *   Regla: Asegurá siempre la llamada a `init_db()` antes de cualquier operación de escritura (`registrar_historial`) o lectura (`obtener_estadisticas`) para autogenerar la tabla si el usuario borra accidentalmente el archivo `.db`.
