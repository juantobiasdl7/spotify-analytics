import requests

def obtener_id_artista(nombre_artista):
    """Busca el ID del artista en Deezer usando el nombre."""
    url = "https://api.deezer.com/search/artist"
    parametros = {'q': nombre_artista}
    
    try:
        response = requests.get(url, params=parametros)
        response.raise_for_status()
        datos = response.json()
        
        if datos['data']:
            return datos['data'][0]['id']
        else:
            print(f"Artista '{nombre_artista}' no encontrado.")
            return None
    except Exception as e:
        print(f"Error al buscar el artista: {e}")
        return None

def obtener_albumes(artist_id):
    """Obtiene la lista de álbumes de un artista mediante su ID."""
    url = f"https://api.deezer.com/artist/{artist_id}/albums"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()
        
        lista_albumes = []
        if 'data' in datos:
            for album in datos['data']:
                lista_albumes.append({
                    "id_album": album['id'],
                    "titulo": album['title'],
                    "fecha_lanzamiento": album.get('release_date', 'Desconocida')
                })
        return lista_albumes
    except Exception as e:
        print(f"Error al obtener álbumes: {e}")
        return []

def obtener_top_canciones(artist_id):
    """Obtiene las 5 canciones más escuchadas de un artista."""
    url = f"https://api.deezer.com/artist/{artist_id}/top"
    parametros = {'limit': 5} # Limitamos a los 5 primeros resultados
    
    try:
        response = requests.get(url, params=parametros)
        response.raise_for_status()
        datos = response.json()
        
        lista_canciones = []
        if 'data' in datos:
            for track in datos['data']:
                lista_canciones.append({
                    "id_track": track['id'],
                    "titulo": track['title'],
                    "duracion_segundos": track['duration'],
                    "reproducciones": track.get('rank', 'N/A')
                })
        return lista_canciones
    except Exception as e:
        print(f"Error al obtener las canciones: {e}")
        return []

# --- Bloque Principal ---
if __name__ == "__main__":
    nombre = "Queen"
    
    print(f"Procesando información de: {nombre}...")
    
    # 1. Obtener ID
    id_artista = obtener_id_artista(nombre)
    
    if id_artista:
        print(f"\nID del artista en Deezer: {id_artista}")
        
        # 2. Obtener Álbumes
        albumes = obtener_albumes(id_artista)
        print(f"\n--- Álbumes Encontrados: {len(albumes)} ---")
        for i, album in enumerate(albumes[:3], 1): # Mostramos los 3 primeros para no saturar la consola
            print(f"{i}. {album['titulo']} | Lanzamiento: {album['fecha_lanzamiento']}")
            
        # 3. Obtener Top 5 canciones
        canciones = obtener_top_canciones(id_artista)
        print("\n--- Top 5 Canciones Más Escuchadas ---")
        for i, cancion in enumerate(canciones, 1):
            print(f"{i}. {cancion['titulo']} | Duración: {cancion['duracion_segundos']}s | Popularidad: {cancion['reproducciones']}")