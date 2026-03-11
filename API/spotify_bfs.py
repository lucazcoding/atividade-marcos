import urllib.request
import urllib.parse
import json
import sys
import base64
from collections import deque



CLIENT_ID     = "13d607624a244caeb13545cf17e9f867"
CLIENT_SECRET = "a1516c3d2ba94f1f836685d371db6543"



BASE_URL = "https://api.spotify.com/v1"




def get_token() -> str:
    """
    Obtém token de acesso usando Client Credentials.
    Não requer login do usuário — ideal para dados públicos.
    """
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()

    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=data,
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]



def search_artist(name: str, token: str) -> dict | None:
    """
    Busca um artista pelo nome e retorna {id, name}.
    """
    params = urllib.parse.urlencode({"q": name, "type": "artist", "limit": 1})
    req = urllib.request.Request(
        f"{BASE_URL}/search?{params}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    items = data.get("artists", {}).get("items", [])
    if not items:
        return None
    return {"id": items[0]["id"], "name": items[0]["name"]}


def get_related_artists(artist_id: str, token: str) -> list:
    """
    Retorna lista de artistas relacionados ao artista dado.
    Cada item: {id, name}
    """
    req = urllib.request.Request(
        f"{BASE_URL}/artists/{artist_id}/related-artists",
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        return [{"id": a["id"], "name": a["name"]} for a in data.get("artists", [])]
    except Exception:
        return []




def bfs_artists(start: dict, end_name: str, token: str) -> list | None:
    """
    BFS no grafo de artistas do Spotify.

    Cada nó é um artista {id, name}.
    Cada aresta é uma relação "artistas relacionados".

    Retorna o menor caminho (lista de nomes) ou None se não encontrar.

    Complexidade:
        Tempo:  O(V + E)
        Espaço: O(V)
    """
   
    queue = deque([[start]])
    
    visited = {start["id"]}

    MAX_DEPTH = 4  

    print(f"\n🔍 Buscando caminho: {start['name']} → {end_name}")
    print("   (isso pode levar alguns segundos...)\n")

    while queue:
        path = queue.popleft()
        current = path[-1]

        if len(path) > MAX_DEPTH:
            continue

        related = get_related_artists(current["id"], token)
        print(f"   Visitando: {current['name']} ({len(related)} relacionados)")

        for artist in related:
            
            if end_name.lower() in artist["name"].lower():
                final_path = path + [artist]
                return [a["name"] for a in final_path]

            if artist["id"] not in visited:
                visited.add(artist["id"])
                queue.append(path + [artist])

    return None



MOCK_GRAPH = {
    "Drake": ["Travis Scott", "J. Cole", "Lil Wayne", "Future", "21 Savage"],
    "Travis Scott": ["Drake", "Kanye West", "Future", "Young Thug", "Gunna"],
    "Kanye West": ["Travis Scott", "Jay-Z", "Kendrick Lamar", "Kid Cudi", "Pusha T"],
    "J. Cole": ["Drake", "Kendrick Lamar", "Big Sean", "Wale"],
    "Kendrick Lamar": ["J. Cole", "Kanye West", "ScHoolboy Q", "Ab-Soul", "Jay Rock"],
    "Jay-Z": ["Kanye West", "Beyoncé", "Nas", "Eminem"],
    "Eminem": ["Jay-Z", "50 Cent", "Dr. Dre", "Royce da 5'9\""],
    "Dr. Dre": ["Eminem", "Snoop Dogg", "50 Cent", "Kendrick Lamar"],
    "Snoop Dogg": ["Dr. Dre", "Jay-Z", "Ice Cube"],
    "Future": ["Drake", "Travis Scott", "Young Thug", "Metro Boomin"],
    "21 Savage": ["Drake", "Metro Boomin", "Post Malone"],
    "Post Malone": ["21 Savage", "Swae Lee", "Ozzy Osbourne"],
    "Kid Cudi": ["Kanye West", "Travis Scott", "Childish Gambino"],
    "Childish Gambino": ["Kid Cudi", "Kendrick Lamar", "Flying Lotus"],
    "Beyoncé": ["Jay-Z", "Rihanna", "Nicki Minaj"],
    "Rihanna": ["Beyoncé", "Drake", "Eminem"],
    "Nicki Minaj": ["Drake", "Lil Wayne", "Beyoncé"],
    "Lil Wayne": ["Drake", "Nicki Minaj", "Young Thug"],
    "Young Thug": ["Travis Scott", "Future", "Lil Wayne", "Gunna"],
    "Gunna": ["Young Thug", "Travis Scott", "Lil Baby"],
    "Lil Baby": ["Gunna", "Future", "Drake"],
    "Metro Boomin": ["Future", "21 Savage", "Drake"],
    "Big Sean": ["J. Cole", "Kanye West", "Jhené Aiko"],
    "Nas": ["Jay-Z", "Kendrick Lamar", "Dr. Dre"],
    "Ice Cube": ["Snoop Dogg", "Dr. Dre", "NWA"],
    "50 Cent": ["Eminem", "Dr. Dre", "Jay-Z"],
    "ScHoolboy Q": ["Kendrick Lamar", "Ab-Soul", "Jay Rock"],
    "Ab-Soul": ["Kendrick Lamar", "ScHoolboy Q", "Jay Rock"],
    "Jay Rock": ["Kendrick Lamar", "ScHoolboy Q", "Ab-Soul"],
}


def bfs_mock(start_name: str, end_name: str) -> list | None:
    """BFS no grafo simulado (modo offline)."""
    if start_name not in MOCK_GRAPH:
        print(f"  ❌ Artista '{start_name}' não encontrado no grafo simulado.")
        return None

    queue = deque([[start_name]])
    visited = {start_name}

    while queue:
        path = queue.popleft()
        current = path[-1]

        for neighbor in MOCK_GRAPH.get(current, []):
            if end_name.lower() in neighbor.lower():
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None




def print_result(path: list | None, start: str, end: str) -> None:
    print("\n" + "=" * 50)
    print(f"🎵 {start}  →  {end}")
    print("=" * 50)

    if not path:
        print("  ❌ Caminho não encontrado (limite de profundidade atingido)")
        return

    distancia = len(path) - 1
    print(f"  ✅ Distância: {distancia} salto(s)\n")
    print("  Caminho encontrado (BFS — menor caminho garantido):")
    for i, artist in enumerate(path):
        if i == 0:
            print(f"    🟢 {artist}  (origem)")
        elif i == len(path) - 1:
            print(f"    🔴 {artist}  (destino)")
        else:
            print(f"     ↓  {artist}")
    print("=" * 50)




def main():
    offline = "--offline" in sys.argv

    
    pares = [
        ("Drake",   "Kanye West"),
        ("Eminem",  "Kendrick Lamar"),
    ]

    if offline:
        print("\n⚡ Modo OFFLINE — grafo simulado")
        print("   (para usar a API real, remova --offline e configure CLIENT_ID/SECRET)\n")

        for start, end in pares:
            print(f"\n🔍 Buscando: {start} → {end}")
            path = bfs_mock(start, end)
            print_result(path, start, end)

    else:
        print("\n🌐 Modo ONLINE — Spotify Web API")

        if CLIENT_ID == "SEU_CLIENT_ID_AQUI":
            print("\n❌ Configure CLIENT_ID e CLIENT_SECRET no início do arquivo!")
            print("   Acesse: https://developer.spotify.com/dashboard")
            sys.exit(1)

        print("🔑 Obtendo token de acesso...")
        token = get_token()
        print("✅ Token obtido!\n")

        for start_name, end_name in pares:
            start_artist = search_artist(start_name, token)
            if not start_artist:
                print(f"❌ Artista '{start_name}' não encontrado.")
                continue

            path = bfs_artists(start_artist, end_name, token)
            print_result(path, start_name, end_name)


if __name__ == "__main__":
    main()