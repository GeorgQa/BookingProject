from core.schema.schema_booking import BOOKING_SCHEMA_GET_ID

BOOKING_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_SCHEMA_GET_ID
    },
    "required": ["bookingid","booking"],
    "additionalProperties": False
}