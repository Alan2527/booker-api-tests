"""Cliente HTTP de Restful-Booker: encapsula endpoints, headers, autenticacion
y adjunta cada request/response como evidencia en el reporte Allure.
"""
import json

import allure
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def _adjuntar_evidencia(metodo, url, payload, respuesta):
    """Adjunta el detalle de la llamada HTTP al paso de Allure actual."""
    cuerpo_enviado = json.dumps(payload, indent=2, ensure_ascii=False) if payload else "(sin body)"
    try:
        cuerpo_recibido = json.dumps(respuesta.json(), indent=2, ensure_ascii=False)
    except ValueError:
        cuerpo_recibido = respuesta.text or "(sin body)"

    detalle = (
        f"{metodo} {url}\n"
        f"Status: {respuesta.status_code}\n\n"
        f"--- Request ---\n{cuerpo_enviado}\n\n"
        f"--- Response ---\n{cuerpo_recibido}"
    )
    allure.attach(detalle, name=f"{metodo} {url}", attachment_type=allure.attachment_type.TEXT)


class BookerClient:
    def __init__(self):
        self.sesion = requests.Session()
        self.sesion.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    @allure.step("GET /ping")
    def ping(self):
        respuesta = self.sesion.get(f"{BASE_URL}/ping")
        _adjuntar_evidencia("GET", "/ping", None, respuesta)
        return respuesta

    @allure.step("POST /auth")
    def obtener_token(self, usuario="admin", password="password123"):
        payload = {"username": usuario, "password": password}
        respuesta = self.sesion.post(f"{BASE_URL}/auth", json=payload)
        _adjuntar_evidencia("POST", "/auth", payload, respuesta)
        return respuesta

    def autenticar(self):
        """Obtiene un token valido y lo deja listo como cookie para PUT/PATCH/DELETE."""
        token = self.obtener_token().json()["token"]
        self.sesion.headers.update({"Cookie": f"token={token}"})
        return token

    @allure.step("GET /booking")
    def listar_reservas(self, **filtros):
        respuesta = self.sesion.get(f"{BASE_URL}/booking", params=filtros or None)
        _adjuntar_evidencia("GET", "/booking", filtros, respuesta)
        return respuesta

    @allure.step("GET /booking/{reserva_id}")
    def obtener_reserva(self, reserva_id):
        respuesta = self.sesion.get(f"{BASE_URL}/booking/{reserva_id}")
        _adjuntar_evidencia("GET", f"/booking/{reserva_id}", None, respuesta)
        return respuesta

    @allure.step("POST /booking")
    def crear_reserva(self, payload):
        respuesta = self.sesion.post(f"{BASE_URL}/booking", json=payload)
        _adjuntar_evidencia("POST", "/booking", payload, respuesta)
        return respuesta

    @allure.step("PUT /booking/{reserva_id}")
    def actualizar_reserva(self, reserva_id, payload):
        respuesta = self.sesion.put(f"{BASE_URL}/booking/{reserva_id}", json=payload)
        _adjuntar_evidencia("PUT", f"/booking/{reserva_id}", payload, respuesta)
        return respuesta

    @allure.step("PATCH /booking/{reserva_id}")
    def actualizar_parcial(self, reserva_id, payload):
        respuesta = self.sesion.patch(f"{BASE_URL}/booking/{reserva_id}", json=payload)
        _adjuntar_evidencia("PATCH", f"/booking/{reserva_id}", payload, respuesta)
        return respuesta

    @allure.step("DELETE /booking/{reserva_id}")
    def eliminar_reserva(self, reserva_id):
        respuesta = self.sesion.delete(f"{BASE_URL}/booking/{reserva_id}")
        _adjuntar_evidencia("DELETE", f"/booking/{reserva_id}", None, respuesta)
        return respuesta
