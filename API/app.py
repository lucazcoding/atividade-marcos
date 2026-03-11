from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.request
import urllib.parse
import json
import base64
import sys
from collections import deque

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)


CLIENT_ID     = "13d607624a244caeb13545cf17e9f867"
CLIENT_SECRET = "a1516c3d2ba94f1f836685d371db6543"


BASE_URL = "https://api.spotify.com/v1"
_token_cache = {"token": None}



GRAPH = {
  
    "Drake":             ["Travis Scott", "J. Cole", "Lil Wayne", "Future", "21 Savage",
                          "Nicki Minaj", "Eminem", "Rihanna", "Jay-Z"],
    "Travis Scott":      ["Drake", "Kanye West", "Future", "Young Thug", "Gunna",
                          "Kid Cudi", "Bad Bunny"],
    "Kanye West":        ["Travis Scott", "Jay-Z", "Kendrick Lamar", "Kid Cudi",
                          "Pusha T", "J. Cole", "Paul McCartney"],
    "J. Cole":           ["Drake", "Kendrick Lamar", "Big Sean", "Kanye West", "21 Savage"],
    "Kendrick Lamar":    ["J. Cole", "Kanye West", "ScHoolboy Q", "Jay Rock",
                          "Dr. Dre", "Drake", "Taylor Swift"],
    "Jay-Z":             ["Kanye West", "Beyoncé", "Nas", "Eminem", "Drake",
                          "Justin Timberlake", "Rihanna"],
    "Eminem":            ["Jay-Z", "50 Cent", "Dr. Dre", "Rihanna", "Ed Sheeran"],
    "Dr. Dre":           ["Eminem", "Snoop Dogg", "50 Cent", "Kendrick Lamar"],
    "Snoop Dogg":        ["Dr. Dre", "Jay-Z", "Ice Cube", "Eminem", "Katy Perry"],
    "Future":            ["Drake", "Travis Scott", "Young Thug", "Metro Boomin", "21 Savage"],
    "21 Savage":         ["Drake", "Metro Boomin", "Post Malone", "Future", "J. Cole"],
    "Post Malone":       ["21 Savage", "Swae Lee", "Future", "Justin Bieber", "The Weeknd"],
    "Kid Cudi":          ["Kanye West", "Travis Scott", "Childish Gambino"],
    "Childish Gambino":  ["Kid Cudi", "Kendrick Lamar"],
    "Nicki Minaj":       ["Drake", "Lil Wayne", "Beyoncé", "Ariana Grande"],
    "Lil Wayne":         ["Drake", "Nicki Minaj", "Young Thug"],
    "Young Thug":        ["Travis Scott", "Future", "Lil Wayne", "Gunna"],
    "Gunna":             ["Young Thug", "Travis Scott", "Lil Baby"],
    "Lil Baby":          ["Gunna", "Future", "Drake"],
    "Metro Boomin":      ["Future", "21 Savage", "Drake"],
    "Big Sean":          ["J. Cole", "Kanye West"],
    "Nas":               ["Jay-Z", "Kendrick Lamar", "Dr. Dre"],
    "Ice Cube":          ["Snoop Dogg", "Dr. Dre"],
    "50 Cent":           ["Eminem", "Dr. Dre", "Jay-Z"],
    "ScHoolboy Q":       ["Kendrick Lamar", "Jay Rock"],
    "Jay Rock":          ["Kendrick Lamar", "ScHoolboy Q"],
    "Swae Lee":          ["Post Malone"],
    "Pusha T":           ["Kanye West"],

    
    "Taylor Swift":      ["Ed Sheeran", "Kendrick Lamar", "Justin Bieber"],
    "Ed Sheeran":        ["Taylor Swift", "Eminem", "Justin Bieber", "Beyoncé",
                          "Camila Cabello", "Bad Bunny"],
    "Justin Bieber":     ["Post Malone", "Ed Sheeran", "Taylor Swift",
                          "Ariana Grande", "DJ Khaled"],
    "Ariana Grande":     ["Nicki Minaj", "Justin Bieber", "The Weeknd",
                          "Iggy Azalea"],
    "The Weeknd":        ["Post Malone", "Ariana Grande", "Daft Punk",
                          "Beyoncé", "Drake"],
    "Beyoncé":           ["Jay-Z", "Rihanna", "Nicki Minaj", "Ed Sheeran",
                          "The Weeknd", "J Balvin"],
    "Rihanna":           ["Beyoncé", "Drake", "Eminem", "Jay-Z", "Paul McCartney"],
    "Katy Perry":        ["Snoop Dogg", "Juicy J", "Zedd"],
    "Justin Timberlake": ["Jay-Z", "Timbaland"],
    "Timbaland":         ["Justin Timberlake"],
    "Iggy Azalea":       ["Ariana Grande"],
    "Paul McCartney":    ["Kanye West", "Rihanna"],
    "Zedd":              ["Katy Perry", "Camila Cabello"],
    "Camila Cabello":    ["Ed Sheeran", "Zedd", "J Balvin"],
    "Daft Punk":         ["The Weeknd", "Pharrell Williams"],
    "Pharrell Williams": ["Daft Punk", "Jay-Z"],
    "DJ Khaled":         ["Justin Bieber", "Beyoncé"],

    
    "Metallica":         ["Lou Reed", "Lady Gaga"],
    "Nirvana":           ["David Bowie"],
    "David Bowie":       ["Nirvana", "Queen", "Mick Jagger"],
    "Queen":             ["David Bowie"],
    "Lady Gaga":         ["Metallica", "Ariana Grande", "Tony Bennett"],
    "Tony Bennett":      ["Lady Gaga"],
    "Lou Reed":          ["Metallica"],
    "Mick Jagger":       ["David Bowie"],

    
    "Bad Bunny":         ["Travis Scott", "Ed Sheeran", "J Balvin",
                          "Becky G", "Daddy Yankee", "Romeo Santos"],
    "J Balvin":          ["Bad Bunny", "Beyoncé", "Camila Cabello",
                          "Daddy Yankee", "Cardi B"],
    "Daddy Yankee":      ["Bad Bunny", "J Balvin", "Luis Fonsi"],
    "Luis Fonsi":        ["Daddy Yankee"],
    "Becky G":           ["Bad Bunny", "Natti Natasha"],
    "Natti Natasha":     ["Becky G", "Daddy Yankee"],
    "Cardi B":           ["J Balvin", "Drake", "Megan Thee Stallion"],
    "Megan Thee Stallion":["Cardi B", "Beyoncé"],
    "Juicy J":           ["Katy Perry"],

    
    "Romeo Santos":      ["Bad Bunny", "Drake", "Usher",
                          "Nicki Minaj", "Marc Anthony"],
    "Marc Anthony":      ["Romeo Santos", "Daddy Yankee"],
    "Usher":             ["Romeo Santos", "Justin Bieber", "Jay-Z"],

    
    "Harry Styles":      ["Niall Horan", "Liam Payne", "Louis Tomlinson",
                          "Zayn", "Kacey Musgraves", "Lizzo"],
    "Niall Horan":       ["Harry Styles", "Liam Payne", "Louis Tomlinson", "Zayn"],
    "Liam Payne":        ["Harry Styles", "Niall Horan", "Louis Tomlinson",
                          "Zayn", "Quavo"],
    "Louis Tomlinson":   ["Harry Styles", "Niall Horan", "Liam Payne", "Zayn"],
    "Zayn":              ["Harry Styles", "Niall Horan", "Liam Payne",
                          "Louis Tomlinson", "Taylor Swift"],
    "Lizzo":             ["Harry Styles", "Ariana Grande"],
    "Kacey Musgraves":   ["Harry Styles"],
    "Quavo":             ["Liam Payne", "Drake"],
}



def get_token():
    if _token_cache["token"]:
        return _token_cache["token"]
    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded = base64.b64encode(credentials.encode()).decode()
        data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
        req = urllib.request.Request(
            "https://accounts.spotify.com/api/token", data=data,
            headers={"Authorization": f"Basic {encoded}",
                     "Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req) as resp:
            token = json.loads(resp.read())["access_token"]
            _token_cache["token"] = token
            return token
    except Exception:
        return None


def get_artist_image(name, token):
    if not token:
        return None
    try:
        params = urllib.parse.urlencode({"q": name, "type": "artist", "limit": 1})
        req = urllib.request.Request(f"{BASE_URL}/search?{params}",
            headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        items = data.get("artists", {}).get("items", [])
        if items and items[0].get("images"):
            return items[0]["images"][0]["url"]
    except Exception:
        pass
    return None



def normalizar(nome):
    nome_lower = nome.lower().strip()
    for key in GRAPH:
        if key.lower() == nome_lower:
            return key
        if nome_lower in key.lower():
            return key
    return None



def bfs(inicio, destino):
    queue = deque([[inicio]])
    visited = {inicio}
    while queue:
        caminho = queue.popleft()
        atual = caminho[-1]
        for vizinho in GRAPH.get(atual, []):
            if vizinho.lower() == destino.lower():
                return caminho + [vizinho]
            if vizinho not in visited:
                visited.add(vizinho)
                queue.append(caminho + [vizinho])
    return None



@app.route("/vizinhos", methods=["GET"])
def vizinhos():
    nome = request.args.get("artista", "").strip()
    real = normalizar(nome)
    if not real:
        return jsonify({"erro": f"'{nome}' não encontrado"}), 404
    return jsonify({"artista": real, "vizinhos": GRAPH.get(real, [])})


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/buscar", methods=["GET"])
def buscar():
    origem  = request.args.get("origem", "").strip()
    destino = request.args.get("destino", "").strip()

    if not origem or not destino:
        return jsonify({"erro": "Informe origem e destino"}), 400

    origem_real  = normalizar(origem)
    destino_real = normalizar(destino)

    if not origem_real:
        return jsonify({"erro": f"'{origem}' não encontrado no grafo"}), 404
    if not destino_real:
        return jsonify({"erro": f"'{destino}' não encontrado no grafo"}), 404
    if origem_real == destino_real:
        return jsonify({"erro": "Origem e destino são o mesmo artista!"}), 400

    caminho = bfs(origem_real, destino_real)
    if not caminho:
        return jsonify({"erro": f"Nenhuma colaboração conecta '{origem_real}' a '{destino_real}'"}), 404

    token = get_token()
    resultado = [{"name": n, "image": get_artist_image(n, token)} for n in caminho]

    return jsonify({"distancia": len(resultado) - 1, "caminho": resultado})


@app.route("/artistas", methods=["GET"])
def listar_artistas():
    return jsonify({"artistas": sorted(GRAPH.keys())})


if __name__ == "__main__":
    if CLIENT_ID == "SEU_CLIENT_ID_AQUI":
        print("\n❌ Configure CLIENT_ID e CLIENT_SECRET no arquivo app.py!")
        sys.exit(1)
    print(f"\n🎵 Servidor: http://localhost:5000")
    print(f"   {len(GRAPH)} artistas no grafo\n")
    app.run(debug=False, port=5000)