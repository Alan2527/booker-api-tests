"""Health check y autenticación."""
import allure
import pytest


@allure.feature("Salud y autenticación")
class TestSaludYAuth:

    @allure.title("La API responde al health check")
    @pytest.mark.salud
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ping(self, cliente):
        assert cliente.ping().status_code == 201  # Quirk documentado: /ping responde 201

    @allure.title("Credenciales válidas devuelven un token")
    @pytest.mark.auth
    @allure.severity(allure.severity_level.BLOCKER)
    def test_token_valido(self, cliente):
        respuesta = cliente.obtener_token()
        assert respuesta.status_code == 200
        assert respuesta.json().get("token"), "La respuesta no incluye token"

    @allure.title("Credenciales inválidas no devuelven token")
    @pytest.mark.auth
    @allure.severity(allure.severity_level.CRITICAL)
    def test_credenciales_invalidas(self, cliente):
        respuesta = cliente.obtener_token(usuario="admin", password="incorrecta")
        # Quirk documentado: responde 200 con {"reason": "Bad credentials"} en vez de 401
        assert respuesta.status_code == 200
        assert respuesta.json().get("reason") == "Bad credentials"
        assert "token" not in respuesta.json()
