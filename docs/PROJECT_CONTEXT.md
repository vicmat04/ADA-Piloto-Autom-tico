# 📋 Contexto del Proyecto: ADA - Piloto Auto v5.0

## 🎯 ¿Qué es ADA?

**ADA (Analizador de Bases de Datos)** es una solución integral de escritorio desarrollada en Python diseñada específicamente para **Infoplazas**, una red de centros comunitarios tecnológicos y de acceso a información en Panamá.

La aplicación tiene como propósito principal automatizar y auditar la recopilación de datos transaccionales de uso de los usuarios procedentes de múltiples sucursales distribuidas en diferentes regiones del país. En versiones anteriores, esta auditoría se realizaba de manera sumamente manual, lo que generaba demoras, errores humanos y dificultades para medir de forma ágil el avance real de las metas de cada regional.

Con la versión **5.0.0**, ADA se ha consolidado como un **Piloto Automático robusto** capaz de procesar bases de datos de Access de forma desatendida, aplicar validaciones de negocio complejas en tiempo de ejecución, persistir historiales en SQLite local, centralizar estadísticas en la nube a través de Google Sheets, y notificar a los supervisores regionales con reportes interactivos en formato HTML enviados directamente por correo electrónico.

---

## 🔍 Problema de Negocio

El sistema administrativo de Infoplazas requiere mantener un control estricto sobre:
1. **Sincronización de Sucursales:** Detectar qué sucursales están subiendo sus bases de datos a tiempo y cuáles tienen retrasos significativos.
2. **Auditoría de Registros de Usuarios:** Las sucursales registran las transacciones locales en archivos de Access (`.mdb`). El campo `ITEMNAME` de estas transacciones contiene información demográfica codificada (Género, Nivel Educativo, etc.) escrita por facilitadores. Si el formato no se audita, se pierde consistencia estadística.
3. **Control y Reporte Regional:** Los coordinadores de cada regional (Los Santos, Chiriquí, Veraguas, Panamá) necesitan estar informados semanal o mensualmente de la salud operativa de sus sucursales sin necesidad de extraer reportes de forma manual.

---

## 💡 La Solución ADA

ADA resuelve de punta a punta este flujo operativo mediante las siguientes características:

*   **Auditoría y Normalización de ITEMNAME:** Limpia caracteres de control XML/Excel no legibles y analiza los campos transaccionales de Access, clasificando de forma inteligente el perfil del usuario incluso cuando existen imperfecciones en el registro manual (aplicando reglas de alternancia de género y tipos de usuario por defecto).
*   **Mecanismo OneDrive-Safe:** Al estar las bases de datos en carpetas compartidas de OneDrive, la app fuerza la descarga local de archivos que estén "solo en la nube" utilizando comandos del sistema (`attrib +p`), evitando bloqueos en la lectura de archivos Access locales.
*   **Centralización en la Nube (Google Sheets):** Centraliza de manera automática los resúmenes agregados en una hoja de cálculo unificada de Google Sheets mediante APIs de servicio, garantizando un dashboard accesible para la directiva nacional.
*   **Doble Capa de Históricos:** Registra un histórico local en SQLite (`historial_sucursales.db`) para análisis estadístico de tendencias de retrasos, al mismo tiempo que alimenta un log de auditoría diaria e histórico de sincronización en Google Sheets.
*   **Sistema de Notificaciones por Correo:** Redacta y despacha automáticamente correos interactivos y responsivos con formato HTML enriquecido a los supervisores y enlaces de cada regional afectada, adjuntando el reporte de Excel consolidado de la ejecución.

---

## 🛠️ Stack Tecnológico

La aplicación se construyó con un enfoque pragmático para el entorno Windows, asegurando portabilidad e independencia de dependencias de servidor complejas:

*   **Lenguaje:** Python 3.11+
*   **Interfaz Gráfica (GUI):** `tkinter` potenciado por `ttkbootstrap` (utilizando el tema oscuro profesional *Darkly*), ofreciendo una estética moderna con transiciones suaves, barras de carga animadas y modales interactivos.
*   **Procesamiento de Datos:** `pandas` y `openpyxl` para manipulación de DataFrames y generación nativa de hojas de cálculo estructuradas.
*   **Acceso a Datos (Access):** `pyodbc` utilizando los controladores ODBC nativos de Microsoft Access para Windows.
*   **Base de Datos Histórica:** `sqlite3` para persistencia interna ágil sin requerir servidores adicionales.
*   **Integración con Google Cloud:** API de Google Sheets y Google Drive (`gspread` y `googleapiclient`) mediante autenticación por cuentas de servicio (`credentials_gebilo.json`).
*   **Protocolo de Correo:** Servidor SMTP (Gmail TLS seguro) con envío de plantillas HTML optimizadas para Microsoft Outlook.
*   **Empaquetamiento:** `PyInstaller` para compilar todo el entorno de Python y dependencias en un único ejecutable standalone (`.exe`), eliminando la necesidad de instalar software en las computadoras de destino.
