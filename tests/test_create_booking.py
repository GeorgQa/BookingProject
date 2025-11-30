import jsonschema
import allure
import pytest
import requests

from conftest import api_client
from core.schema.schema_booking import BOOKING_CREATE_RESPONSE_SCHEMA


@allure.feature("Test create booking")
@allure.story("Test core pozitive an validation schema")
def test_create_booking(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    jsonschema.validate(instance=response["json"], schema=BOOKING_CREATE_RESPONSE_SCHEMA)
    assert response["status_code"] == 200, f"Expected status 200 but got {response['status_code']}"

@allure.feature("Test create booking")
@allure.story("Test server unavailable")
def test_create_booking_server_unavailable(api_client,mocker, generate_random_booking_data):
    mocker.patch.object(api_client.session, "post", side_effect=Exception("Server unavailable"))
    with  pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(generate_random_booking_data)

@allure.feature("Test create booking")
@allure.story("Test not data")
def test_create_booking(api_client):
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_booking(booking_data=None)

    assert exc_info.value.response.status_code == 500, f"Expected 500 but got {exc_info.value.response.status_code}"

@allure.feature("Test create booking")
@allure.story("Test not attribute for data lastname")
def test_create_booking(api_client, booking_data_without_lastname):
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_booking(booking_data=booking_data_without_lastname)

    assert exc_info.value.response.status_code == 500, f"Expected 500 but got {exc_info.value.response.status_code}"


@allure.feature("Test create booking")
@allure.story("Test negative date checkin and checkout")
def test_create_booking(api_client, generate_random_booking_data_negative_dates):
    """Негативный тест на даты (checkin > checkout), но сервер не валидирует такие кейсы — ожидается 200."""
    response = api_client.create_booking(booking_data=generate_random_booking_data_negative_dates)
    assert response["status_code"] == 200, f"Expected status 200 but got {response['status_code']}"


@allure.feature("Test create booking")
@allure.story("Test timeout create booking")
def test_ping_timeout(api_client, mocker, generate_random_booking_data):
    mocker.patch.object(api_client.session, "post" , side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(booking_data=generate_random_booking_data)
