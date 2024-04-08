import requests

url = "http://localhost:8000/"

# Crear una partida
print("\n----------- POST ---------")

new_player = {
    "player": "julian"
}
response = requests.post(url + "guess", json=new_player)
print("Respuesta del servidor:")
print(response.text)
# Listar todas las partidas
print("\n----------- GET ---------")
response = requests.get(url=url + "guess")
print(response.text)

# Buscar una partida por su id
print("\n----------- GET ---------")

# Buscar una partida por el nombre del jugador
print("\n----------- GET ---------")

# Actualizar los intentos de una partida
print("\n----------- PUT ---------")

# Eliminar una partida
print("\n----------- DELETE ---------")

