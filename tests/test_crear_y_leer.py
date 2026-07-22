"""Creación y consulta de reservas, con validación de contrato."""
import allure
import pytest
from jsonschema import validate

from utils import esquemas


@allure.feature("Crear y consultar reservas")
class TestCrearYLeer:

    @allure.title("Crear una reserva devuelve id y refleja los datos enviados")
    @pytest.mark.crear
    @allure.severity(allure.severity_level.BLOCKER)
    def test_crear_reserva(self, cliente_autenticado, payload_reserva):
        respuesta = cliente_autenticado.crear_reserva(payload_reserva)
        assert respuesta.status_code == 200
        cuerpo = respuesta.json()
        validate(cuerpo, esquemas.RESERVA_CREADA)
        assert cuerpo["booking"] == payload_reserva
        cliente_autenticado.eliminar_reserva(cuerpo["bookingid"])

    @allure.title("El listado de reservas cumple el contrato")
    @pytest.mark.leer
    @pytest.mark.contrato
    @allure.severity(allure.severity_level.CRITICAL)
    def test_listado(self, cliente):
        respuesta = cliente.listar_reservas()
        assert respuesta.status_code == 200
        validate(respuesta.json(), esquemas.LISTADO_DE_IDS)
        assert len(respuesta.json()) > 0

    @allure.title("Consultar una reserva por id cumple el contrato")
    @pytest.mark.leer
    @pytest.mark.contrato
    @allure.severity(allure.severity_level.CRITICAL)
    def test_obtener_por_id(self, cliente, reserva_creada):
        reserva_id, payload = reserva_creada
        respuesta = cliente.obtener_reserva(reserva_id)
        assert respuesta.status_code == 200
        validate(respuesta.json(), esquemas.RESERVA)
        assert respuesta.json()["firstname"] == payload["firstname"]

    @allure.title("Filtrar reservas por nombre devuelve la reserva creada")
    @pytest.mark.leer
    @allure.severity(allure.severity_level.NORMAL)
    def test_filtrar_por_nombre(self, cliente, reserva_creada):
        reserva_id, payload = reserva_creada
        respuesta = cliente.listar_reservas(
            firstname=payload["firstname"], lastname=payload["lastname"]
        )
        assert respuesta.status_code == 200
        ids = [r["bookingid"] for r in respuesta.json()]
        assert reserva_id in ids

    @allure.title("Consultar un id inexistente devuelve 404")
    @pytest.mark.leer
    @allure.severity(allure.severity_level.NORMAL)
    def test_id_inexistente(self, cliente):
        assert cliente.obtener_reserva(999999999).status_code == 404
