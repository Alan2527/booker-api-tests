"""Esquemas JSON para validación de contrato."""

RESERVA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
                "checkout": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
            },
        },
        "additionalneeds": {"type": "string"},
    },
}

RESERVA_CREADA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": RESERVA,
    },
}

LISTADO_DE_IDS = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["bookingid"],
        "properties": {"bookingid": {"type": "integer"}},
    },
}
