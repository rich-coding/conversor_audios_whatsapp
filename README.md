# 🎧 Conversor de Audios de WhatsApp para NotebookLM

Este proyecto es una herramienta ligera en Python diseñada para buscar archivos de audio de WhatsApp (formato OGG con extensión `.opus`), convertirlos masivamente a un formato `.mp3` de alta compresión y optimizarlos para ser procesados o analizados dentro de **NotebookLM**.

El entorno y las dependencias están gestionados de forma ultra veloz utilizando **UV** y las tareas comunes están automatizadas con **Just**.

---

## 📋 Requisitos Previos

Antes de iniciar, asegúrate de tener instalado lo siguiente en tu sistema operativo:

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


3. **FFmpeg** (Librería del sistema fundamental para que `pydub` pueda descodificar audio):
    ```bash
    # En macOS
    brew install ffmpeg
    # En Ubuntu/Debian
    sudo apt install ffmpeg
    ```



> ⚠️ **Nota de compatibilidad:** Este proyecto requiere **Python 3.11 o 3.12**. No es compatible con Python 3.13 o superior debido a la eliminación del módulo nativo `audioop` requerido por la dependencia interna de compresión.

---

## 🚀 Instalación y Configuración

1. **Clona o ubícate en la carpeta del proyecto:**
    ```bash
    cd conversor_audios_whatsapp
    ```


2. **Instala la versión correcta de Python y levanta el entorno:**
UV se encargará de descargar la versión exacta de Python requerida sin alterar el resto de tu sistema:
    ```bash
    uv python install 3.12
    ```


3. **Inicializa las carpetas del proyecto:**
Ejecuta la receta de inicio para que el script cree automáticamente los directorios de trabajo:
    ```bash
    just run
    ```


*(La primera vez verás un aviso indicando que no hay archivos `.opus` en la carpeta de entrada, esto es normal y confirma que las carpetas ya se crearon)*.

---

## 💻 Modo de Uso

El flujo de trabajo es muy sencillo:

1. **Preparar tus audios:** Copia todos los archivos de audio de WhatsApp (`.opus`) que descargaste de tu chat dentro de la carpeta recién creada llamada `audios_entrada/`. Un ejemplo de nombre válido es: `00005396-AUDIO-2023-07-13-11-11-37.opus`.
2. **Ejecutar la conversión:** Corre el comando de automatización en tu terminal:
    ```bash
    just run
    ```


3. **Obtener resultados:** El script procesará cada archivo y exportará una versión en formato `.mp3` dentro de la carpeta `audios_salida/`.

El bitrate está configurado a `64k`, lo cual reduce drásticamente el peso del archivo manteniendo una nitidez impecable para la voz humana, ideal para subir decenas de audios a NotebookLM sin agotar cuotas de almacenamiento.

---

## 🛠️ Comandos Disponibles (`Justfile`)

El proyecto incluye recetas listas para usar mediante `just`:

* `just` o `just --list`: Muestra la lista de comandos disponibles.
* `just run`: Ejecuta el script de conversión de audios en el entorno aislado de UV.
* `just clean`: Elimina los archivos temporales (`__pycache__`) y limpia el entorno de caché del proyecto.
* `just lint`: Realiza una comprobación rápida de la compilación del código.

---

## 🔒 Privacidad y Git

Los audios personales de tu chat de WhatsApp **nunca** se subirán a tu proveedor de Git (como GitHub o GitLab). El archivo `.gitignore` ya viene preconfigurado para ignorar por completo las carpetas `audios_entrada/` y `audios_salida/`, así como cualquier archivo individual con extensión `.opus` o `.mp3`.
