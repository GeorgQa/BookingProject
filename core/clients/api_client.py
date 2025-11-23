
import  requests
import os
from  dotenv import load_dotenv
import allure
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeout
from core.settings.environment import  Environment
import jsonschema
from  core.schema.schema_booking import BOOKING_SCHEMA_GET_ID

load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise  ValueError(f"Unsupported environment value: {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json"
        }

    def get_base_url(self, environment: Environment ) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise Exception(f"Unsupported environment: {environment}")

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING}"
            response = self.session.get(url= url)
            response.raise_for_status()
        with allure.step("Assert ststus code"):
            assert  response.status_code == 201 , f"Expected status 201 but got {response.status_code}"
        return  response.status_code

    def auth(self):
        with allure.step("Getting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url=url, json=payload, timeout= Timeout.TIMEOUT)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert  response.status_code == 200 , f"Expected status 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step("Updating header with authorization"):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_booking_by_id(self, bookind_id):
        with allure.step("Send request got"):
            url  = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{bookind_id}"
            response = self.session.get(url=url, timeout=Timeout.TIMEOUT)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert  response.status_code == 200 ,  f"Expected status 200 but got {response.status_code}"
        with allure.step("Validate body response"):
            jsonschema.validate(instance=response.json(), schema= BOOKING_SCHEMA_GET_ID)

