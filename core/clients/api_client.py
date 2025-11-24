
import  requests
import os
from  dotenv import load_dotenv
import allure
from requests.auth import HTTPBasicAuth

from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeout
from core.settings.environment import  Environment


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
            "Content-Type": "application/json",
            "Accept":"application/json"
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
        with allure.step("Assert status code"):
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
        if not token:
            raise ValueError("No token received")

    def get_booking_by_id(self, booking_id: int):
        with allure.step("Send request got"):
            url  = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.get(url=url)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert  response.status_code == 200 ,  f"Expected status 200 but got {response.status_code}"
        # Вот это надо вынести в тесты
        # with allure.step("Validate body response"):
        #     jsonschema.validate(instance=response.json(), schema= BOOKING_SCHEMA_GET_ID)
        return response.json()

    def delete_booking(self, booking_id):
        with allure.step("Delete booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.delete(url=url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert  response.status_code == 201 , f"Expected status code 201 but got {response.status_code}"
        return  response.status_code

    def update_booking(self, booking_id, booking_data ):
        with allure.step("Update booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.put(url=url, json=booking_data,
                                          auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()

    def create_booking(self, booking_data):
        # #вот это надо вынести в тесты
        # with allure.step("Validate booking data"):
        #     jsonschema.validate(instance=booking_data, schema=BOOKING_SCHEMA_GET_ID)
        with allure.step("Create booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}"
            response = self.session.post(url=url , json= booking_data)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert  response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        # Вот это надо вынести в тесты
        # with allure.step("Validate body response"):
        #     jsonschema.validate(instance=response.json() , schema=BOOKING_RESPONSE_SCHEMA)
        return  response.json()

    def get_booking_ids(self, booking_params = None):
        with allure.step("Get booking ID"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}"
            response = self.session.get(url= url, params= booking_params)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert  response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return  response.json()

    def practical_update_booking(self, booking_id, booking_data= None):
        with allure.step("Update booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.patch(url = url , json= booking_data, auth= HTTPBasicAuth(Users.USERNAME,Users.PASSWORD))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()


