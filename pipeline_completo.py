"""
=============================================================================
PIPELINE MAESTRO DE AUTOMATIZACIÓN - EXPOSICIÓN DE MAESTRÍA EN CIENCIAS APLICADAS
Ciencia e Ingeniería de Polímeros: Askeland vs. Callister vs. Shackelford
Expositor: I.Q.S. Miguel Alejandro Díaz Gaytán
=============================================================================

Este script orquesta las 3 fases del proyecto de manera modular:
  - Fase 1: Generación de la presentación académica .pptx con python-pptx
  - Fase 2: Verificación e inspección del guion formal (speech_exposicion.txt)
  - Fase 3: Síntesis neuronal de voz en español natural con edge-tts / gTTS
"""

import os
import sys
import time
import argparse
from generar_presentacion import crear_presentacion
from sintetizar_voz import ejecutar_sintesis, DEFAULT_VOICE, parsear_speech


def ejecutar_pipeline(fase="all", voz=DEFAULT_VOICE, slides=None, usar_gtts=False, output_dir=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if output_dir is None:
        output_dir = base_dir

    ruta_pptx = os.path.join(output_dir, "presentacion_polimeros_maestria.pptx")
    ruta_speech = os.path.join(base_dir, "speech_exposicion.txt")
    carpeta_audios = os.path.join(output_dir, "audios_exposicion")

    t_inicio_total = time.time()
    print("=" * 75)
    print(" PIPELINE DE EXPOSICIÓN: MAESTRÍA EN CIENCIAS APLICADAS")
    print(" Expositor: I.Q.S. Miguel Alejandro Díaz Gaytán")
    print(" Tema: Polímeros | Askeland vs. Callister vs. Shackelford")
    print("=" * 75)

    # -----------------------------------------------------------------------
    # FASE 1: PRESENTACIÓN PPTX
    # -----------------------------------------------------------------------
    if fase in ["all", "1", "pptx"]:
        print("\n>>> INICIANDO FASE 1: GENERACIÓN DE PRESENTACIÓN (.PPTX)...")
        t0 = time.time()
        crear_presentacion(ruta_pptx)
        t_f1 = time.time() - t0
        print(f" -> Fase 1 finalizada con éxito en {t_f1:.2f} s")
    else:
        print("\n[-] Fase 1 omitida por configuración de argumentos.")

    # -----------------------------------------------------------------------
    # FASE 2: VERIFICACIÓN DEL GUION (SPEECH)
    # -----------------------------------------------------------------------
    if fase in ["all", "2", "speech"]:
        print("\n>>> INICIANDO FASE 2: INSPECCIÓN DEL GUION ACADÉMICO (SPEECH)...")
        if not os.path.exists(ruta_speech):
            print(f"[!] Error: No se encontró el archivo de speech en {ruta_speech}")
            return
        diaps = parsear_speech(ruta_speech)
        total_palabras = sum(len(txt.split()) for txt in diaps.values())
        print(f" -> Guion validado: {len(diaps)} diapositivas detectadas.")
        print(f" -> Total de palabras del discurso: {total_palabras} palabras (~{(total_palabras/130):.1f} min de exposición).")
        print(f" -> Archivo fuente: {ruta_speech}")
    else:
        print("\n[-] Fase 2 omitida por configuración de argumentos.")

    # -----------------------------------------------------------------------
    # FASE 3: SÍNTESIS DE VOZ NEURONAL
    # -----------------------------------------------------------------------
    if fase in ["all", "3", "audio", "tts"]:
        print("\n>>> INICIANDO FASE 3: SÍNTESIS DE VOZ NEURONAL...")
        t0 = time.time()
        archivos = ejecutar_sintesis(
            speech_path=ruta_speech,
            output_dir=carpeta_audios,
            voz=voz,
            diapositivas=slides,
            usar_gtts=usar_gtts,
        )
        t_f3 = time.time() - t0
        print(f" -> Fase 3 finalizada con éxito en {t_f3:.2f} s ({len(archivos)} audios listos).")
    else:
        print("\n[-] Fase 3 omitida por configuración de argumentos.")

    tiempo_total = time.time() - t_inicio_total
    print("\n" + "=" * 75)
    print(" RESUMEN DE EJECUCIÓN DEL PIPELINE")
    print("=" * 75)
    print(f"• Tiempo total de ejecución: {tiempo_total:.2f} s")
    print(f"• Presentación PowerPoint:   {ruta_pptx}")
    print(f"• Guion de Defensa Askeland: {ruta_speech}")
    print(f"• Carpeta de Pistas de Audio: {carpeta_audios}")
    print("=" * 75)
    print("¡Éxito en tu presentación del martes ante el comité evaluador!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pipeline automatizado para la exposición de Maestría en Ciencias Aplicadas."
    )
    parser.add_argument(
        "--phase",
        type=str,
        default="all",
        choices=["all", "1", "2", "3", "pptx", "speech", "audio"],
        help="Fase a ejecutar (all, 1, 2, 3)",
    )
    parser.add_argument(
        "--voice",
        type=str,
        default=DEFAULT_VOICE,
        help=f"Voz neural para edge-tts (default: {DEFAULT_VOICE})",
    )
    parser.add_argument(
        "--slides",
        type=str,
        default=None,
        help="Lista de diapositivas a sintetizar separadas por coma (ej. 1,2,3). Default: todas",
    )
    parser.add_argument(
        "--gtts",
        action="store_true",
        help="Usar gTTS como alternativa a edge-tts",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directorio de salida para los archivos generados",
    )

    args = parser.parse_args()

    slides_list = None
    if args.slides:
        slides_list = [int(s.strip()) for s in args.slides.split(",") if s.strip().isdigit()]

    ejecutar_pipeline(
        fase=args.phase,
        voz=args.voice,
        slides=slides_list,
        usar_gtts=args.gtts,
        output_dir=args.output_dir,
    )
