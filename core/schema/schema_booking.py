BOOKING_BODY_SCHEMA  = {
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

BOOKING_CREATE_RESPONSE_SCHEMA  = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_BODY_SCHEMA,
    },
    "required": ["bookingid", "booking"],
    "additionalProperties": False,
}
