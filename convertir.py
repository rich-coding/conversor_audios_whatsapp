import os
import re
import datetime
from pathlib import Path
from collections import defaultdict
from pydub import AudioSegment

# Límite de NotebookLM en Bytes (200 Megabytes)
LIMITE_NOTEBOOK_LM_BYTES = 200 * 1024 * 1024  

def preparar_entorno():
    """Asegura la existencia de las carpetas de trabajo."""
    entrada = Path("audios_entrada")
    salida = Path("audios_salida")
    entrada.mkdir(exist_ok=True)
    salida.mkdir(exist_ok=True)
    return entrada, salida

def extraer_fecha_de_nombre(nombre_archivo):
    """
    Extrae la fecha de un nombre tipo: 00005396-AUDIO-2023-07-13-11-11-37.opus
    Retorna un objeto datetime.date o None si no coincide.
    """
    patron = r"AUDIO-(\d{4})-(\d{2})-(\d{2})"
    coincidencia = re.search(patron, nombre_archivo)
    if coincidencia:
        año, mes, dia = map(int, coincidencia.groups())
        try:
            return datetime.date(año, mes, dia)
        except ValueError:
            return None
    return None

def obtener_clave_agrupacion(fecha, opcion):
    """Genera la clave de agrupación y el formato del nombre de salida."""
    if opcion == "año":
        return f"{fecha.year}", f"Audios_{fecha.year}"
    elif opcion == "mes":
        return f"{fecha.year}-{fecha.month:02d}", f"Audios_{fecha.year}_{fecha.month:02d}"
    elif opcion == "semana":
        # Retorna el año y el número de semana ISO
        año_iso, semana, _ = fecha.isocalendar()
        return f"{año_iso}-W{semana:02d}", f"Audios_{año_iso}_Semana_{semana:02d}"
    return "Otros", "Audios_Desconocidos"

def solicitar_opcion_usuario():
    """Pregunta al usuario cómo desea agrupar los audios."""
    print("📋 Selecciona la granularidad para agrupar y concatenar tus audios:")
    print("1. Por Semana (Ideal si hay muchísimos audios al día)")
    print("2. Por Mes    (Recomendado para chats de varios años)")
    print("3. Por Año    (Para unificar todo al máximo)")
    
    while True:
        seleccion = input("Ingresa el número de tu opción (1, 2 o 3): ").strip()
        if seleccion == "1": return "semana"
        if seleccion == "2": return "mes"
        if seleccion == "3": return "año"
        print("❌ Opción inválida. Intenta de nuevo.")

def procesar_y_concatenar():
    dir_entrada, dir_salida = preparar_entorno()
    archivos_opus = list(dir_entrada.glob("*.opus"))
    
    if not archivos_opus:
        print(f"❌ No se encontraron archivos .opus en '{dir_entrada}'.")
        return

    opcion_grupo = solicitar_opcion_usuario()
    print(f"\nSorting y agrupando audios por {opcion_grupo}...")

    # Estructura para agrupar: { clave: [(fecha, ruta_archivo), ...] }
    grupos = defaultdict(list)
    
    for ruta in archivos_opus:
        fecha = extraer_fecha_de_nombre(ruta.name)
        if fecha:
            clave, _ = obtener_clave_agrupacion(fecha, opcion_grupo)
            grupos[clave].append((fecha, ruta))
        else:
            # Si no tiene el formato de WhatsApp, se va a un grupo genérico
            grupos["Sin_Fecha"].append((datetime.date.min, ruta))

    print(f"Se generarán {len(grupos)} archivo(s) unificado(s).\n")

    # Procesar cada grupo
    for clave, elementos in sorted(grupos.items()):
        # Ordenar cronológicamente los audios dentro del mismo grupo
        elementos_ordenados = sorted(elementos, key=lambda x: x[0])
        
        # Obtener el nombre limpio del archivo de salida usando el primer elemento
        _, primer_formato = obtener_clave_agrupacion(elementos_ordenados[0][0], opcion_grupo)
        if clave == "Sin_Fecha":
            primer_formato = "Audios_Sin_Fecha_Identificada"
            
        ruta_mp3_salida = dir_salida / f"{primer_formato}.mp3"
        
        print(f"📦 Procesando grupo [{clave}] - Uniendo {len(elementos_ordenados)} audios...")
        
        audio_unificado = AudioSegment.empty()
        errores = 0

        for _, ruta_audio in elementos_ordenados:
            try:
                audio_segmento = AudioSegment.from_file(ruta_audio, codec="opus")
                audio_unificado += audio_segmento
                # Opcional: añade 500ms de silencio entre audios para notar la transición
                silencio = AudioSegment.silent(duration=500)
                audio_unificado += silencio
            except Exception as e:
                print(f"   ⚠️ Error leyendo {ruta_audio.name}: {e}")
                errores += 1

        if len(audio_unificado) == 0:
            print(f"   ❌ El grupo {clave} no contiene audio válido.")
            continue

        # Exportar el archivo unificado
        print(f"   💾 Exportando a {ruta_mp3_salida.name} (Bitrate: 64k)...")
        audio_unificado.export(ruta_mp3_salida, format="mp3", bitrate="64k")
        
        # Verificar tamaño del archivo resultante
        tamano_bytes = ruta_mp3_salida.stat().st_size
        tamano_mb = tamano_bytes / (1024 * 1024)
        
        if tamano_bytes > LIMITE_NOTEBOOK_LM_BYTES:
            print("\n" + "!" * 60)
            print(f"🚨 ¡ALERTA DE LÍMITE SUPERADO en {ruta_mp3_salida.name}!")
            print(f"   Tamaño actual: {tamano_mb:.2f} MB (El límite de NotebookLM es de 200 MB).")
            print("💡 PROPUESTA DE SOLUCIÓN:")
            print("   1. Vuelve a ejecutar el script y elige una granularidad menor (ej. 'semana' en vez de 'mes').")
            print("   2. Modifica el código para bajar el bitrate de exportación a '32k' (audio.export(..., bitrate='32k')).")
            print("!" * 60 + "\n")
        else:
            print(f"   ✅ ¡Éxito! Archivo creado con {tamano_mb:.2f} MB.")

    print("\n🎉 ¡Todo el proceso de unificación ha concluido!")

if __name__ == "__main__":
    procesar_y_concatenar()