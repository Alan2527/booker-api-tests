"""Cliente HTTP de Restful-Booker: encapsula endpoints, headers y autenticación."""
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


class BookerClient:
    def __init__(self):
        self.sesion = requests.Session()
        self.sesion.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def ping(self):
        return self.sesion.get(f"{BASE_URL}/ping")

    def obtener_token(self, usuario="admin", password="password123"):
        respuesta = self.sesion.post(
            f"{BASE_URL}/auth",
            json={"username": usuario, "password": password},
        )
        return respuesta

    def autenticar(self):
        """Obtiene un token válido y lo deja listo como cookie para PUT/PATCH/DELETE."""
        token = self.obtener_token().json()["token"]
        self.sesion.headers.update({"Cookie": f"token={token}"})
        return token

    def listar_reservas(self, **filtros):
        return self.sesion.get(f"{BASE_URL}/booking", params=filtros or None)

    def obtener_reserva(self, reserva_id):
        return self.sesion.get(f"{BASE_URL}/booking/{reserva_id}")

    def crear_reserva(self, payload):
        return self.sesion.post(f"{BASE_URL}/booking", json=payload)

    def actualizar_reserva(self, reserva_id, payload):
        return self.sesion.put(f"{BASE_URL}/booking/{reserva_id}", json=payload)

    def actualizar_parcial(self, reserva_id, payload):
        return self.sesion.patch(f"{BASE_URL}/booking/{reserva_id}", json=payload)

    def eliminar_reserva(self, reserva_id):
        return self.sesion.delete(f"{BASE_URL}/booking/{reserva_id}")
