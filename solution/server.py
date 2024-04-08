from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class Game:
   _instance = None
   
   games = {}
   
   def __new__(cls):
      if not cls._instance:
         cls._instance = super().__new__(cls)

   # Crear una partida
   def create_game(self, player):
      game_id = len(self.games) + 1
      number_to_guess = random.randint(1, 100)
      new_game = {
         "player": player,
         "number": number_to_guess,
         "attempts": [],
         "status": "En Progreso"
      }
      self.games[game_id] = new_game
      return new_game
   
   # Listar todas las partidas
   def list_games(self):
      return self.games
   
   # Buscar una partida por su id
   def search_game_by_id(self, game_id):
      return self.games.get(game_id)
   
   # Buscar una partida por el nombre del jugador
   def search_game_by_player(self, player):
      for game_id, game in self.games.items():
         if game["player"] == player:
            return game_id
      return None   
   # Actualizar los intentos de una partida
   def update_attempts(self, game_id, attempt):
      game = self.games.get(game_id)
      if game:
         game["attempts"].append(attempts)
         if attempt == game["number"]:
               game["status"] = "Finalizado"
               return {"message": "Felicitaciones!!! Has adivinado el número"}
         elif attempt < game["number"]:
               return {"message": "El número a adivinar es mayor"}
         else:
               return {"message": "El número a adivinar es menor"}
      else:
         return {"message": "Partida no encontrada"}
   # Eliminar una partida
   def delete_game(self, game_id):
      if game_id in self.games:
         del self.games[game_id]
         return {"message": "Partida Eliminada"}
      else:
         return {"message": "Partida No Encontrada"}
   

class HTTPDataHandler(BaseHTTPRequestHandler):
   @staticmethod
   def handler_response(handler, status, data):
      handler.send_response(status)
      handler.send_header("Content-type", "application/json")
      handler.end_headers()
      handler.wfile.write(json.dumps(data).encode("utf-8"))
   
   @staticmethod
   def handler_reader(handler):
      content_length = int(handler.headers["Content-Length"])
      post_data = handler.rfile.read(content_length)
      return json.loads(post_data.decode('utf-8'))


class GameHandler(BaseHTTPRequestHandler):
   def do_POST(self):
      if self.path == "/guess":
         data = HTTPDataHandler.handler_reader(self)
         new_game = self.game.create_game(data["player"])
         HTTPDataHandler.handler_response(self, 200, new_game)

   def do_GET(self):
      if self.path == "/guess":
         all_games = self.game.list_games()
         HTTPDataHandler.handler_response(self, 200, all_games)
      elif self.path.startswith("/guess/"):
         game_id = int(self.path.split("/")[-1])
         if game_id in self.game.games:
               game = self.game.search_game_by_id(game_id)
               HTTPDataHandler.handler_response(self, 200, {game_id: game})
         else:
               HTTPDataHandler.handler_response(self, 404, {"message": "Partida no encontrada"})
      elif self.path.startswith("/guess/?player="):
         player_name = self.path.split("=")[-1]
         game = self.game.search_game_by_player(player_name)
         if game:
               HTTPDataHandler.handler_response(self, 200, game)
         else:
               HTTPDataHandler.handler_response(self, 404, {"message": "Partida no encontrada"})
   
   def do_PUT(self):
      if self.path.startswith("/guess/"):
         game_id = int(self.path.split("/")[-1])
         data = HTTPDataHandler.handler_reader(self)
         result = self.game.update_attempts(game_id, int(data["attempt"]))
         HTTPDataHandler.handler_response(self, 200, result)

    def do_DELETE(self):
      if self.path.startswith("/guess/"):
         game_id = int(self.path.split("/")[-1])
         result = self.game.delete_game(game_id)
         HTTPDataHandler.handler_response(self, 200, result)


def run_server(port=8000):
   global player
   player = Player("Alice")
   
   try:
      server_address = ("", port)
      httpd = HTTPServer(server_address, GameHandler)
      print(f"Iniciando servidor web en https://localhost:{port}/")
      httpd.serve_forever()
   except KeyboardInterrupt:
      print("Apagando servidor...")
      httpd.socket.close()

if __name__ == "__main__":
   run_server()