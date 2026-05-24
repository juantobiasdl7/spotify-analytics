import requests
import datetime
import csv
import sys
import os


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
            tr_time_add = track_object["time_add"]
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
                tr_artist_name,
                tr_album_title,
            ]
            track_list.append(track_row)
    except TypeError:
        print(f"El argumento playlist_object no es del tipo 'dict': {TypeError}")
    except Exception as e:
        print(f"Error al obtener carcaterísticas de la playlist: {type(e)}, {e}")
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
):
    """Crea un archivo CSV a partir de una lista. Opcionalmente se puede especificar la ruta de almacenamiento"""

    try:
        # Fecha de creación de archivo csv.
        if not isinstance(lista_de_elementos, list):
            raise TypeError

        # Crear la carpeta si no existe
        if folder_name:
            os.makedirs(folder_name, exist_ok=True)
            print(f"\nLa carpeta {folder_name} fue creada exitosamente.")

        csv_creation_date_utc = datetime.datetime.now(tz=datetime.UTC).strftime(
            "%Y-%m-%d-%H-%M%z"
        )
        utc_file_path = f"{folder_name}/{file_name}({csv_creation_date_utc}).csv"
        with open(file=utc_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for elemento in lista_de_elementos:
                if isinstance(elemento, dict):
                    writer.writerow(list(elemento.items()))
                else:
                    writer.writerow(elemento)
    except TypeError:
        print(f"\nEl argumento lista_de_elementos no es del tipo 'list':{TypeError}")
    except Exception as e:
        print(f"\nError al crear archivo csv: type{e}, {e}")
    else:
        print(f"\nEl archivo '{utc_file_path}' ha sido creado.")
    finally:
        print(f"Función '{sys._getframe().f_code.co_name}' finalizada.\n")


if __name__ == "__main__":
    id_playlist_top_50_mexico = "1111142361"
    playlist_object_top_50 = obtener_playlist_object(
        id_playlist=id_playlist_top_50_mexico, num=10
    )
    top_50_tracks_list = generar_lista_tracks(playlist_object=playlist_object_top_50)
    print(
        "\nGenerando CSV de Top 50 canciones diarias en Deezer mas escuchadas en México"
    )
    lista_a_csv(
        lista_de_elementos=top_50_tracks_list,
        file_name="top-50-mexico-daily-by-deezer",
        folder_name="csv-files",
    )
