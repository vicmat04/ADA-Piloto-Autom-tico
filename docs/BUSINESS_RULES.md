# 🎯 Reglas de Negocio: ADA - Piloto Auto v5.0

Las reglas de negocio estructuran y regulan la lógica de procesamiento, auditoría y métricas de ADA. Estas reglas aseguran la homogeneidad de la información y previenen reportes erróneos.

> [!IMPORTANT]
> **REGLA DE DESARROLLO INMUTABLE:** Jamás se debe modificar la lógica de negocio ni la forma de extraer los datos desde las bases de datos Microsoft Access (`.mdb`/`pyodbc`), a menos que el usuario lo indique de manera explícita en el chat.

---

## 🏬 1. Clasificación del Estado de Sincronización de Sucursales

Cada sucursal (carpeta física dentro del directorio regional) es evaluada dinámicamente bajo criterios secuenciales para determinar su salud operativa:

1.  **Cerrada Definitivamente:**
    *   **Criterio:** Presencia del archivo vacío `CERRADA DEFINITIVAMENTE.txt` en el directorio de la sucursal.
    *   **Acción:** La sucursal es omitida en el cálculo de estadísticas porcentuales del reporte ejecutivo y correo, pero se almacena en el log local/nube con la observación `"CERRADA DEFINITIVAMENTE"`.
2.  **Carpeta Vacía / Sin Base de Datos:**
    *   **Criterio:** No existen archivos con extensión `.mdb` dentro de la carpeta.
    *   **Acción:** Se cataloga con la observación `"Carpeta Vacía"` (o el nombre de cualquier archivo `.txt` que describa una justificación en la carpeta). Se cuenta dentro de las operativas pero entra en el conteo de **Para Revisión**.
3.  **Fuera de Periodo / Retraso Crítico:**
    *   **Criterio:** Existe base de datos `.mdb` pero la fecha de modificación del archivo es mayor a **10 días** con respecto a la fecha de análisis actual.
    *   **Acción:** Se cataloga en la sección **Para Revisión** y se resalta en color naranja en las tablas de correo y reportes.
4.  **Sincronizada (En Periodo):**
    *   **Criterio:** La fecha del archivo `.mdb` tiene un desfase de **10 días o menos** con respecto al día del análisis.
    *   **Acción:** Considerada al día. Se cataloga en **En Periodo** y se muestra en verde.

---

## 👤 2. Auditoría y Extracción de Perfil de Usuario (`ITEMNAME`)

El campo `ITEMNAME` de la tabla `SALES` es un string ingresado manualmente que codifica el perfil demográfico. Se procesa mediante un algoritmo extractor con tolerancia a fallos:

*   **Limpieza de Texto:** Se eliminan caracteres dobles, guiones sobrantes y espacios en blanco. Los caracteres de control no legibles para XML/Excel son removidos preventivamente.
*   **Clasificación de Género (`SEXO`):**
    *   Se buscan los tokens independientes `M` (Masculino) o `F` (Femenino) al final del string.
    *   **Regla de Alternancia (Fallback):** Si no se puede deducir el género por ausencia de token, el sistema asigna alternadamente `M` o `F` de forma secuencial entre registros anómalos (`alternador_sexo = not alternador_sexo`), garantizando una distribución estadística neutra.
*   **Clasificación de Nivel Educativo (`TIPO U`):**
    *   Se buscan los siguientes tokens válidos:
        *   `P`: Primaria
        *   `S`: Secundaria
        *   `U`: Universitario
        *   `D`: Docente
        *   `TE`: Tercera Edad
        *   `PG`: Público General
    *   **Regla por Defecto (Fallback):** Si no se encuentra ningún token válido en el string, el registro se asigna automáticamente a **`PG` (Público General)**.
*   **Flag de Observación:**
    *   Si el formato contiene la combinación de tipo de usuario y sexo esperado (ej: `*-P-M` o `*-S-F`), se marca como **`OK`**.
    *   En caso de requerir la aplicación de algún fallback (alternancia o tipo por defecto), se marca el registro individual con la etiqueta **`VERIFICAR`**.

---

## 📊 3. Modelo de Avance de Metas (Cálculos de Desempeño)

De acuerdo con el documento de análisis conceptual (`ANALISIS_CALCULOS_METAS.md`), la evaluación temporal abarca el periodo **Noviembre 2024 - Diciembre 2025 (14 meses totales)**:

*   **Avance Mensual Esperado:**
    $$\text{Avance Mensual Esperado} = \frac{\text{Meta Total}}{\text{14 meses}}$$
    *(Ejemplo: Meta de 100 usuarios en Plataformas Virtuales $\rightarrow$ $100 / 14 = 7.14$ usuarios mensuales esperados).*
*   **Avance Real Mensual:**
    $$\text{Avance Real Mensual} = \frac{\text{Realizado Acumulado}}{\text{Meses Completados}}$$
*   **Rendimiento del Ritmo Mensual:**
    $$\text{Progreso Mensual (\%)} = \left( \frac{\text{Avance Real Mensual}}{\text{Avance Mensual Esperado}} \right) \times 100$$
*   **Avance Global del Período:**
    *   **Relativo (Ritmo Esperado a la Fecha):**
        $$\text{Avance Global Relativo (\%)} = \left( \frac{\text{Realizado Acumulado}}{\text{Avance Mensual Esperado} \times \text{Meses Completados}} \right) \times 100$$
    *   **Absoluto (Con respecto a la Meta Anual):**
        $$\text{Avance Global Absoluto (\%)} = \left( \frac{\text{Realizado Acumulado}}{\text{Meta Total}} \right) \times 100$$
*   **Metas Puntuales (Eventos Únicos):**
    Metas como el *"Día del Internet"* o *"Mesas de Transformación"* son puntuales. No aplican promedios mensuales; su avance es absoluto: $(\text{Realizado} / \text{Meta}) \times 100$.

---

## ☁️ 4. Reglas de Deduplicación y Consistencia en Google Sheets

La consistencia en la nube se rige por procesos automáticos de comparación y reemplazo de celdas para evitar inflar las estadísticas:

1.  **Pestañas Regionales (Resumen Mensual de Métricas):**
    *   **Identificador Único:** Combinación de `Infoplaza` + `Año` + `Mes`.
    *   **Regla de Reemplazo:** Si ya existe un registro en la hoja para la misma sucursal y mes:
        *   Se compara el campo `Total` de usuarios registrado con el nuevo cálculo.
        *   **SOLO** se actualiza y reemplaza la fila si los nuevos datos contienen un volumen de transacciones **MAYOR** al que ya estaba en la hoja (`nuevo_total > total_existente`). Si es menor o igual, se conserva el registro previo para resguardar la consistencia histórica.
2.  **Pestañas `Historial_{Regional}` (Logs de Ejecución Diaria):**
    *   **Identificador Único:** Combinación de `Sucursal` + `FechaAnalisis` (YYYY-MM-DD, ignorando la hora).
    *   **Regla de Reemplazo:** Solo se permite **un registro por sucursal al día**. Si se ejecuta ADA varias veces en una misma fecha, la base de datos de Google Sheets elimina la fila anterior y conserva únicamente la **última ejecución diaria** (`keep='last'`).
3.  **Pestaña Global `PorcSinc` (Cumplimiento de Sincronización):**
    *   **Identificador Único:** Combinación de `Regional` + `Fecha` (YYYY-MM-DD).
    *   **Regla de Reemplazo:** Si se ejecuta el análisis de una misma regional múltiples veces el mismo día, se actualiza el registro existente sobrescribiendo los porcentajes de sincronización sobre la misma fila, evitando duplicar registros diarios de métricas.
