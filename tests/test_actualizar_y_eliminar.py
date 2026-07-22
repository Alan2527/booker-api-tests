"""Actualización (total y parcial) y baja de reservas."""
import allure
import pytest


@allure.feature("Actualizar y eliminar reservas")
class TestActualizarYEliminar:

    @allure.title("PUT reemplaza la reserva completa")
    @pytest.mark.actualizar
    @allure.severity(allure.severity_level.CRITICAL)
    def test_actualizacion_total(self, cliente_autenticado, reserva_creada):
        reserva_id, payload = reserva_creada
        payload_nuevo = dict(payload, firstname="Carlos", totalprice=2000)
        respuesta = cliente_autenticado.actualizar_reserva(reserva_id, payload_nuevo)
        assert respuesta.status_code == 200
        assert respuesta.json()["firstname"] == "Carlos"
        assert respuesta.json()["totalprice"] == 2000

    @allure.title("PATCH modifica solo los campos enviados")
    @pytest.mark.actualizar
    @allure.severity(allure.severity_level.CRITICAL)
    def test_actualizacion_parcial(self, cliente_autenticado, reserva_creada):
        reserva_id, payload = reserva_creada
        respuesta = cliente_autenticado.actualizar_parcial(reserva_id, {"lastname": "Gómez"})
        assert respuesta.status_code == 200
        assert respuesta.json()["lastname"] == "Gómez"
        assert respuesta.json()["firstname"] == payload["firstname"], "PATCH alteró un campo no enviado"

    @allure.title("PUT sin token es rechazado con 403")
    @pytest.mark.actualizar
    @allure.severity(allure.severity_level.CRITICAL)
    def test_actualizar_sin_token(self, cliente, reserva_creada):
        reserva_id, payload = reserva_creada
        respuesta = cliente.actualizar_reserva(reserva_id, payload)
        assert respuesta.status_code == 403

    @allure.title("DELETE elimina la reserva y la API responde 201 (quirk documentado)")
    @pytest.mark.eliminar
    @allure.severity(allure.severity_level.CRITICAL)
    def test_eliminar(self, cliente_autenticado, payload_reserva):
        reserva_id = cliente_autenticado.crear_reserva(payload_reserva).json()["bookingid"]
        respuesta = cliente_autenticado.eliminar_reserva(reserva_id)
        # Quirk conocido de la API: devuelve 201 en lugar de 200/204
        assert respuesta.status_code == 201
        assert cliente_autenticado.obtener_reserva(reserva_id).status_code == 404

    @allure.title("DELETE sin token es rechazado con 403")
    @pytest.mark.eliminar
    @allure.severity(allure.severity_level.CRITICAL)
    def test_eliminar_sin_token(self, cliente, reserva_creada):
        reserva_id, _ = reserva_creada
        assert cliente.eliminar_reserva(reserva_id).status_code == 403
