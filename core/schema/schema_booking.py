BOOKING_SCHEMA_NOT_FULL = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
            },
            "required": ["checkin", "checkout"],
            "additionalProperties": False,
        },
        "additionalneeds": {"type": "string"},
    },
    "required": [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
        "additionalneeds",
    ],
    "additionalProperties": False,
}

BOOKING_SCHEMA_FULL = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_SCHEMA_NOT_FULL,
    },
    "required": ["bookingid", "booking"],
    "additionalProperties": False,
}
