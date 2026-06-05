# 📦 Instrucciones para Empaquetar ADA - Piloto Auto v5.0

## Requisitos Previos

1. **Instalar PyInstaller** (si no lo tienes):
```bash
pip install pyinstaller
```

2. **Verificar que todas las dependencias estén instaladas**:
```bash
pip install pandas pyodbc ttkbootstrap pillow gspread google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openpyxl
```

## 🚀 Comando de Empaquetado

Ejecuta el siguiente comando desde la carpeta del proyecto:

```bash
pyinstaller --onefile --windowed --name="ADA_PilotoAuto_v5" --icon="VicTor.ico" --add-data="VicTor.ico;." --add-data="credentials_gebilo.json;." --add-data="sucursales_history.py;." --hidden-import=ttkbootstrap --hidden-import=babel.numbers --hidden-import=gspread --hidden-import=google.oauth2.service_account --hidden-import=googleapiclient.discovery --collect-all ttkbootstrap "ADA - Piloto Auto v5.py"
```

## 📝 Explicación de Parámetros

- `--onefile`: Genera UN SOLO archivo .exe
- `--windowed`: Oculta la consola de comandos (modo GUI)
- `--name`: Nombre del ejecutable final
- `--icon`: Icono de la aplicación
- `--add-data`: Incluye archivos necesarios (formato: "origen;destino")
- `--hidden-import`: Importaciones que PyInstaller no detecta automáticamente
- `--collect-all ttkbootstrap`: Incluye todos los recursos de ttkbootstrap (temas, etc.)

## 📂 Archivos Generados

Después de ejecutar el comando, encontrarás:

- **`dist/ADA_PilotoAuto_v5.exe`** ← Este es tu ejecutable final
- `build/` - Archivos temporales (puedes borrar esta carpeta)
- `ADA_PilotoAuto_v5.spec` - Archivo de configuración de PyInstaller

## 🎯 Distribución

### Opción 1: Ejecutable + Archivos de Configuración
Para distribuir la aplicación, comparte:
1. `ADA_PilotoAuto_v5.exe`
2. `credentials_gebilo.json` (en la misma carpeta)
3. `VicTor.ico` (en la misma carpeta)

### Opción 2: Solo Ejecutable
El .exe ya incluye los archivos incorporados, pero necesitará:
- `credentials_gebilo.json` en la misma carpeta (para acceso a Google Sheets)

## ⚙️ Primera Ejecución en Otro PC

1. Copia `ADA_PilotoAuto_v5.exe` al PC de destino
2. Copia `credentials_gebilo.json` a la misma carpeta
3. Ejecuta el .exe (doble clic)
4. Configura rutas y opciones desde la interfaz

## 🔧 Notas Importantes

- **Antivirus**: Algunos antivirus pueden marcar el .exe como sospechoso. Es normal con PyInstaller. Agrega excepciones si es necesario.
- **Primera ejecución**: Puede tardar unos segundos en abrir la primera vez.
- **Tamaño**: El .exe será grande (~100-200 MB) porque incluye Python y todas las librerías.
- **Credenciales Google**: El archivo `credentials_gebilo.json` es CRÍTICO para el funcionamiento. Sin él, no podrá subir datos a Google Sheets.

## 🐛 Solución de Problemas

### Error: "No module named 'ttkbootstrap'"
Ejecuta con `--collect-all ttkbootstrap` (ya incluido en el comando arriba)

### Error: "Failed to execute script"
1. Prueba ejecutar sin `--windowed` para ver errores en consola
2. Verifica que `credentials_gebilo.json` esté en la carpeta correcta

### El .exe es muy grande
Es normal. PyInstaller incluye Python completo y todas las dependencias.

## 📌 Comandos Alternativos

### Con Consola (para debug)
```bash
pyinstaller --onefile --name="ADA_PilotoAuto_v5" --icon="VicTor.ico" --add-data="VicTor.ico;." --add-data="credentials_gebilo.json;." --add-data="sucursales_history.py;." --hidden-import=ttkbootstrap --hidden-import=babel.numbers --hidden-import=gspread --collect-all ttkbootstrap "ADA - Piloto Auto v5.py"
```

### Para Actualizar el Build
Si ya generaste el .exe y quieres regenerarlo:
```bash
pyinstaller ADA_PilotoAuto_v5.spec
```

---

**¡Listo para distribuir!** 🚀
