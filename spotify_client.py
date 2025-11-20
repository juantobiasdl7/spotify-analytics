import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI


def get_spotify_client():
    """
    Crea y retorna un cliente autenticado de Spotify
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


def get_user_top_tracks(sp, limit=10):
    """
    Obtiene las canciones más escuchadas del usuario
    """
    results = sp.current_user_top_tracks(limit=limit, time_range="short_term")
    return results["items"]


if __name__ == "__main__":
    # Prueba de conexión
    print("Conectando a Spotify...")
    client = get_spotify_client()
    print("✓ Conexión exitosa!")

    print("\nTus top 5 canciones:")
    tracks = get_user_top_tracks(client, limit=5)
    for i, track in enumerate(tracks, 1):
        print(f"{i}. {track['name']} - {track['artists'][0]['name']}")
