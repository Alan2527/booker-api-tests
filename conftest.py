"""Fixtures compartidas: cliente, cliente autenticado y reserva de prueba con limpieza."""
import pytest

from utils.api_client import BookerClient


@pytest.fixture(scope="session")
def cliente():
    """Cliente sin autenticar (suficiente para GET y POST)."""
    return BookerClient()


@pytest.fixture(scope="session")
def cliente_autenticado():
    """Cliente con token en cookie, requerido para PUT, PATCH y DELETE."""
    api = BookerClient()
    api.autenticar()
    return api


@pytest.fixture
def payload_reserva():
    """Datos base de una reserva de prueba."""
    return {
        "firstname": "Alan",
        "lastname": "Herrera",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-08-01", "checkout": "2026-08-10"},
        "additionalneeds": "Desayuno",
    }


@pytest.fixture
def reserva_creada(cliente_autenticado, payload_reserva):
    """Crea una reserva y la elimina al finalizar el test (limpieza garantizada)."""
    respuesta = cliente_autenticado.crear_reserva(payload_reserva)
    assert respuesta.status_code == 200, "No se pudo crear la reserva de prueba"
    reserva_id = respuesta.json()["bookingid"]
    yield reserva_id, payload_reserva
    cliente_autenticado.eliminar_reserva(reserva_id)
