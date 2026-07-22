# Suite de API Testing — Restful-Booker

![CI](https://github.com/Alan2527/booker-api-tests/actions/workflows/api-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Requests](https://img.shields.io/badge/requests-2.x-green)
![Allure](https://img.shields.io/badge/Reportes-Allure-orange)

Suite de pruebas de API REST sobre [Restful-Booker](https://restful-booker.herokuapp.com), construida con **Python + Pytest + requests**, validación de contrato con **jsonschema** y reportes **Allure** publicados en GitHub Pages.

📊 **[Ver el último reporte Allure →](https://alan2527.github.io/booker-api-tests/)**

## Qué demuestra este proyecto

- **Cliente de API encapsulado** (`BookerClient`): endpoints, headers y autenticación en un solo lugar; los tests no repiten plumbing HTTP.
- **Validación de contrato**: los responses se validan contra esquemas JSON (estructura, tipos y formatos de fecha), no solo contra valores puntuales.
- **Fixtures con limpieza garantizada**: cada reserva de prueba se elimina al finalizar el test, incluso si falla — la suite no deja basura en el sistema bajo prueba.
- **Casos negativos y de seguridad**: operaciones de escritura sin token (403), ids inexistentes (404), credenciales inválidas.
- **Quirks documentados en el código**: esta API pública tiene comportamientos no estándar (p. ej. `DELETE` responde `201`, credenciales inválidas responden `200` con `reason`). La suite los fija con asserts comentados: si el comportamiento cambia, la suite avisa.
- **Monitoreo programado**: además de cada push, el pipeline corre semanalmente contra la API pública.

## Cobertura

| Área | Casos | Qué valida |
|---|---|---|
| Salud y auth | 3 | Health check, obtención de token, credenciales inválidas |
| Crear y leer | 5 | POST con eco de datos, contrato del listado y del detalle, filtros, 404 |
| Actualizar y eliminar | 5 | PUT completo, PATCH parcial, DELETE, rechazo sin token |

## Estructura

```
├── conftest.py            # Cliente, cliente autenticado y reserva con auto-limpieza
├── utils/
│   ├── api_client.py      # BookerClient: encapsula la API
│   └── esquemas.py        # Esquemas JSON de contrato
├── tests/                 # Casos por área funcional
└── .github/workflows/     # CI + smoke semanal + reporte Allure
```

## Ejecución local

```bash
pip install -r requirements.txt
pytest --alluredir=allure-results
allure serve allure-results
```

---
*Proyecto de portfolio — [Alan Herrera](https://www.linkedin.com/in/alan-herrera-15b8a2215), Sr. QA Analyst.*
