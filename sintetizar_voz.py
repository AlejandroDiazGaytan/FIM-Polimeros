"""
=============================================================================
PIPELINE DE EXPOSICIÓN ACADÉMICA - FASE 3: SÍNTESIS DE VOZ NEURONAL
Maestría en Ciencias Aplicadas
Expositor: I.Q.S. Miguel Alejandro Díaz Gaytán
Síntesis con red neuronal de Microsoft Edge TTS (acento natural en español)
=============================================================================
"""

import os
import re
import sys
import asyncio
import argparse

# Voz predeterminada en español (México) - Red neuronal natural masculina
DEFAULT_VOICE = "es-MX-JorgeNeural"
# Alternativas de alta fidelidad:
# "es-MX-DaliaNeural" (Femenina, México)
# "es-ES-AlvaroNeural" (Masculina, España)


def parsear_speech(speech_file_path):
    """
    Lee speech_exposicion.txt y lo fragmenta en un diccionario ordenado
    donde la clave es el número de diapositiva (int) y el valor es el texto.
    """
    if not os.path.exists(speech_file_path):
        raise FileNotFoundError(f"No se encontró el archivo de speech en: {speech_file_path}")

    with open(speech_file_path, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Patrón para identificar secciones: [DIAPOSITIVA XX]
    patron = r"\[DIAPOSITIVA\s+(\d+)\]"
    secciones = re.split(patron, contenido)

    diapositivas = {}
    # re.split con grupo de captura produce: [preambulo, id1, texto1, id2, texto2, ...]
    for i in range(1, len(secciones), 2):
        num_diap = int(secciones[i])
        texto = secciones[i + 1].strip()
        # Limpieza básica para síntesis fluida
        texto_limpio = re.sub(r"\s+", " ", texto)
        diapositivas[num_diap] = texto_limpio

    return diapositivas


async def sintetizar_texto_edge(texto, archivo_salida, voz=DEFAULT_VOICE, rate="+0%", pitch="+0Hz"):
    """
    Sintetiza una cadena de texto a un archivo de audio MP3 usando edge-tts.
    """
    try:
        import edge_tts
    except ImportError:
        raise ImportError(
            "La librería 'edge-tts' no está instalada. Ejecuta: pip install edge-tts"
        )

    communicate = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch)
    await communicate.save(archivo_salida)


def sintetizar_texto_gtts(texto, archivo_salida, lang="es"):
    """
    Método de contingencia usando gTTS en caso de ausencia de edge-tts.
    """
    try:
        from gtts import gTTS
    except ImportError:
        raise ImportError(
            "Ni 'edge-tts' ni 'gTTS' están disponibles. Instala edge-tts: pip install edge-tts"
        )
    tts = gTTS(text=texto, lang=lang, slow=False)
    tts.save(archivo_salida)


async def procesar_sintesis_completa(
    speech_path=None,
    output_dir=None,
    voz=DEFAULT_VOICE,
    diapositivas_seleccionadas=None,
    usar_gtts=False,
):
    """
    Ejecuta el procesamiento de síntesis para todas o un subconjunto de diapositivas.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if speech_path is None:
        speech_path = os.path.join(base_dir, "speech_exposicion.txt")
    elif not os.path.isabs(speech_path):
        speech_path = os.path.join(base_dir, speech_path)

    if output_dir is None:
        output_dir = os.path.join(base_dir, "audios_exposicion")
    elif not os.path.isabs(output_dir):
        output_dir = os.path.join(base_dir, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n" + "=" * 70)
    print("FASE 3: SÍNTESIS DE VOZ NEURONAL POR DIAPOSITIVA")
    print("=" * 70)
    print(f"Archivo de texto fuente: {speech_path}")
    print(f"Directorio de audios:   {output_dir}")
    print(f"Motor de síntesis:      {'gTTS' if usar_gtts else f'edge-tts ({voz})'}")

    diapositivas = parsear_speech(speech_path)
    print(f"Diapositivas detectadas en el guion: {len(diapositivas)}")

    # Filtrar si se solicitó un subconjunto
    if diapositivas_seleccionadas:
        keys_a_procesar = [k for k in sorted(diapositivas.keys()) if k in diapositivas_seleccionadas]
    else:
        keys_a_procesar = sorted(diapositivas.keys())

    archivos_generados = []

    for num in keys_a_procesar:
        texto = diapositivas[num]
        nombre_archivo = f"audio_diapositiva_{num:02d}.mp3"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        palabras = len(texto.split())

        print(f"\n[Diapositiva {num:02d}] Sintetizando ({palabras} palabras)...")
        try:
            if usar_gtts:
                sintetizar_texto_gtts(texto, ruta_salida)
            else:
                await sintetizar_texto_edge(texto, ruta_salida, voz=voz)

            tamano_kb = os.path.getsize(ruta_salida) / 1024
            print(f" -> Generado con éxito: {nombre_archivo} ({tamano_kb:.1f} KB)")
            archivos_generados.append(ruta_salida)
        except Exception as e:
            print(f" [!] Error en diapositiva {num:02d}: {e}")
            if not usar_gtts:
                print(" -> Intentando fallback con gTTS...")
                try:
                    sintetizar_texto_gtts(texto, ruta_salida)
                    print(f" -> Recuperado con gTTS: {nombre_archivo}")
                    archivos_generados.append(ruta_salida)
                except Exception as e2:
                    print(f" [X] Fallback también falló: {e2}")

    print("\n" + "=" * 70)
    print(f"[FASE 3 COMPLETADA] {len(archivos_generados)} de {len(keys_a_procesar)} audios sintetizados.")
    print(f"Carpeta de almacenamiento: {output_dir}")
    print("=" * 70)
    return archivos_generados


def ejecutar_sintesis(speech_path=None, output_dir=None, voz=DEFAULT_VOICE, diapositivas=None, usar_gtts=False):
    """
    Función de entrada síncrona que envuelve la corutina asíncrona.
    """
    return asyncio.run(
        procesar_sintesis_completa(
            speech_path=speech_path,
            output_dir=output_dir,
            voz=voz,
            diapositivas_seleccionadas=diapositivas,
            usar_gtts=usar_gtts,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Síntesis de voz neuronal para la exposición de Maestría.")
    parser.add_argument("--speech", type=str, default=None, help="Ruta al archivo speech_exposicion.txt")
    parser.add_argument("--output-dir", type=str, default=None, help="Directorio para guardar los MP3")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help="Voz neural de edge-tts (ej. es-MX-JorgeNeural)")
    parser.add_argument("--slides", type=str, default=None, help="Diapositivas específicas separadas por coma (ej. 1,2,3)")
    parser.add_argument("--gtts", action="store_true", help="Usar gTTS en lugar de edge-tts")

    args = parser.parse_args()

    slides_list = None
    if args.slides:
        slides_list = [int(s.strip()) for s in args.slides.split(",") if s.strip().isdigit()]

    ejecutar_sintesis(
        speech_path=args.speech,
        output_dir=args.output_dir,
        voz=args.voice,
        diapositivas=slides_list,
        usar_gtts=args.gtts,
    )
