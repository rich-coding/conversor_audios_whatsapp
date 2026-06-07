# Receta por defecto: muestra la ayuda
default:
    @just --list

# Ejecuta el script de conversión usando el entorno virtual de UV
run:
    uv run python convertir.py

# Limpia los archivos temporales de Python y la caché
clean:
    rm -rf .uv
    rm -rf __pycache__
    rm -rf .pytest_cache
    find . -type d -name "__pycache__" -exec rm -r {} +

# Verifica y formatea el código (Usa las herramientas nativas de UV si están configuradas, o comandos estándar)
lint:
    uv run python -m compileall .