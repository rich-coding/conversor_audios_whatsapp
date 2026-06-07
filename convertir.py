import os
from pathlib import Path
from pydub import AudioSegment

def preparar_entorno():
    """Crea las carpetas de entrada y salida si no existen."""
    entrada = Path("audios_entrada")
    salida = Path("audios_salida")
    
    entrada.mkdir(exist_ok=True)
    salida.mkdir(exist_ok=True)
    
    return entrada, salida

def convertir_opus_a_mp3():
    # 1. Obtener y asegurar las rutas de los directorios
    dir_entrada, dir_salida = preparar_entorno()
    
    # 2. Buscar todos los archivos .opus en la carpeta de entrada
    archivos_opus = list(dir_entrada.glob("*.opus"))
    
    if not archivos_opus:
        print(f" No se encontraron archivos .opus en '{dir_entrada}'.")
        print("Por favor, copia tus audios de WhatsApp en esa carpeta e intenta de nuevo.")
        return

    print(f" Se encontraron {len(archivos_opus)} archivos para procesar.\n")

    # 3. Ciclo de conversión
    for index, ruta_audio in enumerate(archivos_opus, start=1):
        nombre_base = ruta_audio.stem  # Ejemplo: 00005396-AUDIO-2023-07-13-11-11-37
        ruta_mp3_salida = dir_salida / f"{nombre_base}.mp3"
        
        print(f"[{index}/{len(archivos_opus)}] Convirtiendo: {ruta_audio.name}...")
        
        try:
            # Cargar el archivo de audio original (.opus)
            audio = AudioSegment.from_file(ruta_audio, codec="opus")
            
            # Exportar a MP3 ligero. 
            # '64k' es excelente para voz humana, reduce drásticamente el peso sin perder claridad.
            audio.export(
                ruta_mp3_salida, 
                format="mp3", 
                bitrate="64k"
            )
            print(f"   Hecho -> {ruta_mp3_salida.name}")
            
        except Exception as e:
            print(f" ❌ Error al procesar {ruta_audio.name}: {e}")
            
    print("\n¡Proceso de conversión finalizado con éxito!")

if __name__ == "__main__":
    convertir_opus_a_mp3()