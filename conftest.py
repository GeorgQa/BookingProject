import pytest


from datetime import datetime, timedelta
from faker import Faker

from core.clients.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture(scope="function")
def booking_dates():
    today = datetime.today()
    checkin_date = today + timedelta(days=10)
    checkout_date = checkin_date + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d")
    }


@pytest.fixture(scope="function")
def generate_random_booking_data(booking_dates):
    faker = Faker("ru_RU")
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence(ext_word_list=["Breakfast", "Lunch", "Dinner","Wifi"])

    date = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds,
    }

    return date

@pytest.fixture()
def booking_data_without_lastname(generate_random_booking_data):
    data = generate_random_booking_data
    data.pop("lastname", None)
    return data

@pytest.fixture(scope="session")
def booking_dates_with_wrong_dates():
    today = datetime.today()
    checkin_date = today + timedelta(days=5)
    checkout_date = checkin_date - timedelta(days=3)

    return {
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d")
    }

@pytest.fixture(scope="session")
def generate_random_booking_data_negative_dates(booking_dates_with_wrong_dates):
    faker = Faker("ru_RU")
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence(ext_word_list=["Breakfast", "Lunch", "Dinner","Wifi"])

    date = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates_with_wrong_dates,
        "additionalneeds": additionalneeds,
    }

    return date