import csv
import datetime
import os
import sys
from fpdf import FPDF
import requests


def obtener_playlist_object(id_playlist: int, num: int = 1) -> dict:
    """Convierte un Objeto Playlist a un diccionario."""

    url = f"https://api.deezer.com/playlist/{id_playlist}"
    parametros = {"limit": num}

    try:
        response = requests.get(url, params=parametros)
        response.raise_for_status()
        playlist_object = response.json()
    except Exception as e:
        print(f"Error al obtener canciones de playlist: type{e}, {e}")
    else:
        pl_title = playlist_object["title"]
        print(f"Objeto Playlist '{pl_title}' correctamente generado.")
        return playlist_object
    finally:
        print(f"Función '{sys._getframe().f_code.co_name}' finalizada.\n")


def generar_lista_tracks(playlist_object: dict) -> list:
    """Genera una lista compuesta por la descripción de la Playlist y las canciones incluidas en la misma."""
    tracks_full_info = []
    try:
        # Información de playlist.
        playlist_info = {
            "pl_id": playlist_object["id"],
            "pl_title": playlist_object["title"],
            "pl_description": playlist_object["description"],
            "pl_nb_track_objects": playlist_object["nb_tracks"],
            "pl_link": playlist_object["link"],
            "pl_creator_name": playlist_object["creator"]["name"],
        }

        # Información de canciones de playlist
        tracks_object = playlist_object["tracks"]["data"]
        track_list = []
        tr_header = [
            "tr_daily_rank",
            "tr_id",
            "tr_title",
            "tr_duration",
            "tr_explicit",
            "tr_time_add",
            "tr_artist_name",
            "tr_album_title",
        ]
        track_list.append(tr_header)

        for i, track_object in enumerate(tracks_object):
            tr_daily_rank = i + 1
            tr_id = track_object["id"]
            tr_title = track_object["title"]
            tr_duration = track_object["duration"]
            tr_explicit = track_object["explicit_lyrics"]
            tr_time_add = track_object.get("time_add", "")
            tr_artist_name = track_object["artist"]["name"]
            tr_album_title = track_object["album"]["title"]

            track_row = [
                tr_daily_rank,
                tr_id,
                tr_title,
                tr_duration,
                tr_explicit,
                tr_time_add,
                tr_artist_name,
                tr_album_title,
            ]
            track_list.append(track_row)
    except TypeError:
        print(
            f"El argumento playlist_object no es del tipo 'dict': {TypeError}"
        )
    except Exception as e:
        print(
            f"Error al obtener carcaterísticas de la playlist: {type(e)}, {e}"
        )
    else:
        tracks_full_info.append(playlist_info)
        tracks_full_info.extend(track_list)

        print("Descripción de la Playlist generada exitosamente:")
        for k, v in playlist_info.items():
            print(f"\t{k}: {v}")
        print(f"Lista con {tr_daily_rank} canciones creada correctamente.")
        return tracks_full_info
    finally:
        print(f"Función '{sys._getframe().f_code.co_name}' finalizada.\n")


def lista_a_csv(
    lista_de_elementos: list, file_name: str = "Lista", folder_name: str = ""
) -> str:
    """Crea un archivo CSV a partir de una lista. Regresa la ruta del archivo generado."""

    try:
        if not isinstance(lista_de_elementos, list):
            raise TypeError

        if folder_name:
            os.makedirs(folder_name, exist_ok=True)
            print(f"\nLa carpeta '{folder_name}' fue verificada/creada exitosamente.")

        csv_creation_date_utc = datetime.datetime.now(tz=datetime.UTC).strftime(
            "%Y-%m-%d-%H-%M%z"
        )
        utc_file_path = f"{folder_name}/{file_name}({csv_creation_date_utc}).csv"

        with open(
            file=utc_file_path, mode="w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            for elemento in lista_de_elementos:
                if isinstance(elemento, dict):
                    writer.writerow(list(elemento.items()))
                else:
                    writer.writerow(elemento)

        print(f"El archivo CSV '{utc_file_path}' ha sido creado.")
        return utc_file_path

    except TypeError:
        print(
            f"\nEl argumento lista_de_elementos no es del tipo 'list':{TypeError}"
        )
        return ""
    except Exception as e:
        print(f"\nError al crear archivo csv: type{e}, {e}")
        return ""
    finally:
        print(f"Función '{sys._getframe().f_code.co_name}' finalizada.\n")


def lista_a_pdf(lista_de_elementos: list, csv_file_path: str, folder_name: str = ""):
    """Crea un archivo PDF ordenado en su propia carpeta basándose en el nombre de archivo del CSV."""
    if not csv_file_path or not lista_de_elementos:
        print("No se pudo generar el PDF debido a datos vacíos o error en CSV.")
        return

    if folder_name:
        os.makedirs(folder_name, exist_ok=True)
        print(f"La carpeta '{folder_name}' fue verificada/creada exitosamente.")

    # Extraemos solo el nombre del archivo (ej. "top-50-mexico-daily-by-deezer(2026-...).csv")
    nombre_archivo_csv = os.path.basename(csv_file_path)
    
    # Cambiamos la extensión final y anteponemos la nueva carpeta de PDFs
    nombre_archivo_pdf = nombre_archivo_csv.replace(".csv", ".pdf")
    pdf_file_path = f"{folder_name}/{nombre_archivo_pdf}"

    try:
        playlist_info = lista_de_elementos[0]
        canciones = lista_de_elementos[2:]

        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Título del Reporte
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(
            0,
            10,
            f"Reporte de Playlist: {playlist_info.get('pl_title', 'Deezer')}",
            ln=True,
            align="L",
        )
        pdf.ln(4)

        # Información General
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(
            0, 5, f"Creador: {playlist_info.get('pl_creator_name', 'N/A')}", ln=True
        )
        pdf.cell(
            0,
            5,
            f"Descripción: {playlist_info.get('pl_description', 'Sin descripción')}",
            ln=True,
        )
        pdf.cell(
            0,
            5,
            f"Total de canciones extraídas: {playlist_info.get('pl_nb_track_objects', 0)}",
            ln=True,
        )
        pdf.ln(8)

        # Tabla de Canciones
        columnas = [
            "Rank",
            "ID Track",
            "Título de la Canción",
            "Duración (s)",
            "Explicit",
            "Artista",
            "Álbum",
        ]
        anchos = [15, 25, 65, 25, 18, 62, 62]

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(240, 240, 240)
        for col, ancho in zip(columnas, anchos):
            pdf.cell(ancho, 8, col, border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 9)
        for fila in canciones:
            datos_limpios = [
                str(fila[0]),
                str(fila[1]),
                str(fila[2]),
                f"{fila[3]}s",
                "Sí" if fila[4] else "No",
                str(fila[6]),
                str(fila[7]),
            ]

            for dato, ancho in zip(datos_limpios, anchos):
                dato_seguro = dato.encode("latin-1", "replace").decode("latin-1")
                if len(dato_seguro) > 33:
                    dato_seguro = dato_seguro[:30] + "..."
                pdf.cell(ancho, 7, dato_seguro, border=1)
            pdf.ln()

        pdf.output(pdf_file_path)
        print(f"El archivo PDF '{pdf_file_path}' ha sido creado exitosamente.")

    except Exception as e:
        print(f"Error al crear archivo PDF: type{e}, {e}")
    finally:
        print(f"Función '{sys._getframe().f_code.co_name}' finalizada.\n")


if __name__ == "__main__":
    id_playlist_top_50_mexico = "1111142361"
    playlist_object_top_50 = obtener_playlist_object(
        id_playlist=id_playlist_top_50_mexico, num=10
    )
    top_50_tracks_list = generar_lista_tracks(
        playlist_object=playlist_object_top_50
    )

    print("\nGenerando archivos de Top 50 canciones diarias en Deezer...")

    # 1. Creamos el CSV pasándole la carpeta "csv-files"
    ruta_csv_final = lista_a_csv(
        lista_de_elementos=top_50_tracks_list,
        file_name="top-50-mexico-daily-by-deezer",
        folder_name="csv-files",
    )

    # 2. Generamos el PDF pasándole la nueva carpeta "pdf-files"
    lista_a_pdf(
        lista_de_elementos=top_50_tracks_list,
        csv_file_path=ruta_csv_final,
        folder_name="pdf-files",
    )