# 🎧 Conversor y Concatenador de Audios de WhatsApp para NotebookLM

Este proyecto es una herramienta avanzada en Python diseñada para buscar archivos de audio de WhatsApp (formato OGG con extensión `.opus`), agruparlos dinámicamente por criterios temporales (semana, mes o año), ordenarlos cronológicamente y concatenarlos en archivos `.mp3` ligeros y optimizados. 

El objetivo principal es preparar y compactar años de historial de notas de voz para que puedan ser procesados y analizados sin inconvenientes dentro de **NotebookLM**.

El entorno y las dependencias están gestionados con **UV** y las tareas comunes están automatizadas a través de **Just**.

---

## 🧠 Entendiendo los Límites de NotebookLM

NotebookLM es una herramienta excepcional para analizar fuentes de información, pero cuenta con dos restricciones críticas al cargar archivos de audio:

1. **Límite de Fuentes (Máximo 50):** No puedes subir más de 50 archivos individuales a un mismo cuaderno. Si tienes un chat de varios años con cientos de audios, es imposible subirlos uno por uno.
2. **Límite de Tamaño (Máximo 200 MB por archivo):** Cada archivo de audio que subas no puede exceder los 200 Megabytes.

### 💡 Nuestra Solución
Este script resuelve ambos límites simultáneamente:
* **Evita el límite de fuentes** permitiéndote fusionar decenas de audios en un único bloque temporal (un mes entero de conversación, por ejemplo).
* **Controla el límite de tamaño** exportando en un bitrate eficiente (`64k`) ideal para voz humana y activando una alerta en la terminal si algún bloque supera los 200 MB, sugiriendo medidas de mitigación inmediatas.

---

## 📋 Requisitos Previos

Antes de iniciar, asegúrate de tener instalado lo siguiente en tu sistema:

1. **UV** (Gestor de paquetes de Python):
    ```bash
    # En macOS/Linux
    curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
    # En Windows (PowerShell)
    powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
    ```

2. **Just** (Ejecutor de comandos):

    ```bash
    # En macOS (Homebrew)
    brew install just
    # En Ubuntu/Debian
    sudo apt install just
    ```

3. **FFmpeg** (Librería del sistema multimedia indispensable para que `pydub` procese el audio):

    ```bash
   # En macOS
   brew install ffmpeg
   # En Ubuntu/Debian
   sudo apt install ffmpeg
    ```

> ⚠️ **Nota de compatibilidad:** Este proyecto requiere **Python 3.11 o 3.12**. No es compatible con Python 3.13 o superior debido a la eliminación del módulo nativo `audioop` en las versiones más recientes de Python, el cual es requerido internamente por la librería de manipulación de audio.

---

## 🚀 Instalación y Configuración

1. **Ubícate en la carpeta del proyecto:**

    ```bash
   cd conversor_audios_whatsapp
    ```

2. **Instala la versión correcta de Python:**
UV descargará un entorno aislado y seguro sin afectar tus configuraciones globales:

    ```bash
   uv python install 3.12
    ```

3. **Inicializa el entorno y las carpetas de trabajo:**
Ejecuta la receta por primera vez para comprobar que el entorno levante y se creen los directorios necesarios:

    ```bash
   just run
    ```

*(La primera vez verás un aviso indicando que no hay archivos `.opus` en la carpeta de entrada. Esto confirma que las carpetas de trabajo han sido creadas con éxito).*

---

## 💻 Modo de Uso

1. **Preparar tus audios:** Copia todos los archivos de audio de WhatsApp (`.opus`) que desees procesar dentro de la carpeta `audios_entrada/`. El script requiere el formato de nombre estándar de WhatsApp, por ejemplo: `00005396-AUDIO-2023-07-13-11-11-37.opus`.
2. **Ejecutar la conversión:** Corre el comando de automatización en tu terminal:

    ```bash
   just run
    ```

3. **Seleccionar granularidad:** El script se detendrá y te presentará un menú interactivo en la terminal:
* **1. Por Semana:** Excelente si el chat tiene un volumen masivo de audios por día.
* **2. Por Mes (Recomendado):** El punto de equilibrio perfecto para chats de varios años. Mantiene una excelente línea de tiempo sin saturar las fuentes.
* **3. Por Año:** Maximiza la unificación si el flujo de audios anual es moderado.


4. **Recoger los resultados:** Los audios se ordenarán cronológicamente para no perder el sentido de la conversación, se les añadirá un sutil espacio de silencio entre mensajes y se guardarán en `audios_salida/` con nombres limpios (ej. `Audios_2023_07.mp3`).

---

## 🚨 Manejo de Alertas de Tamaño

Si un archivo unificado resultante excede los 200 MB, el script imprimirá una advertencia visual en la terminal. Si esto sucede, puedes aplicar las siguientes soluciones de programación:

* **Disminuir el intervalo:** Vuelve a ejecutar el script utilizando una granularidad más fina (por ejemplo, si elegiste por Año y falló, cámbialo a por Mes).
* **Reducir el Bitrate:** Abre el archivo `convertir.py`, localiza la línea de exportación y reduce el parámetro a `bitrate="32k"`. Esto mantendrá la voz legible y reducirá el peso del archivo a la mitad.

---

## 🛠️ Comandos del Justfile

* `just` o `just --list`: Muestra la lista de comandos automatizados.
* `just run`: Lanza el menú interactivo y ejecuta el proceso de ordenamiento y concatenación.
* `just clean`: Remueve de forma segura las cachés de Python (`__pycache__`) y del entorno de UV.
* `just lint`: Realiza una verificación estática rápida de la sintaxis del código de programación.