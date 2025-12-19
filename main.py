import spotipy
import datetime
import csv
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI


def get_spotify_client():
    """
    Crea y retorna un cliente autenticado de Spotify.
    """
    scope = "user-top-read user-read-recently-played"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
        )
    )
    return sp


def get_top_n_mexico_weekly(sp, pl_id, top=5) -> list[dict]:
    """
    Obtiene un objeto que contiene el top n de canciones de una playlist de Spotify.

    Parámetros:
    sp -- Autenticación de Spotify.
    pl_id -- ID de alguna playlist de Spotify.
    top -- Default 5. Establece el número de canciones.
    """
    results = sp.playlist_tracks(playlist_id=pl_id, limit=top)
    return results["items"]


if __name__ == "__main__":
    # Prueba de conexión
    print("Conectando a Spotify...")
    client_personal = get_spotify_client()
    print("✓ Conexión exitosa!")

    # Lista de Spotify de Diskover Co.
    id_top_100_mexico_weekly_discover_co = "5KLKS1zjjeqSe6oRgsdUMb"
    url_top_100_mexico_weekly_discover_co = (
        "https://open.spotify.com/playlist/5KLKS1zjjeqSe6oRgsdUMb"
    )

    tracks_object = get_top_n_mexico_weekly(
        client_personal, pl_id=id_top_100_mexico_weekly_discover_co, top=50
    )

    # Lista de canciones.
    tracks_list = []
    header = ["posición", "canción", "albúm", "artista(s)"]
    tracks_list.append(header)

    for i, track_object in enumerate(tracks_object):
        posicion = i + 1
        cancion = track_object["track"]["name"]
        album = track_object["track"]["album"]["name"]

        artists_objects = track_object["track"]["artists"]
        artistas = [artist["name"] for artist in artists_objects]

        track_row = [posicion, cancion, album, artistas]
        tracks_list.append(track_row)

    # Creación de CSV.
    try:
        print(
            "\nGenerando CSV de Top 50 canciones de Spotify mas escuchadas semanalmente en México \npor Discover Co."
        )
        file_name = "top-50-mexico-weekly"
        csv_creation_date_utc = datetime.datetime.now(tz=datetime.UTC).strftime(
            "%Y-%m-%d-%H-%M%z"
        )
        utc_file_path = f"{file_name}({csv_creation_date_utc}).csv"

        with open(file=utc_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for track in tracks_list:
                writer.writerow(track)
    except Exception as e:
        print(f"\nError: {e}")
    else:
        print(f"\nEl archivo '{utc_file_path}' ha sido creado.")
