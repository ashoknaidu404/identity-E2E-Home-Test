import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pages.motorway_page import MotorwayPage
from utils.data_reader import DataReader

CAR_INPUT_FILE = "car_input - V5.txt"
CAR_OUTPUT_FILE = "car_output - V5.txt"
ERROR_NOTIFICATION = (By.CLASS_NAME, "InfoBox-module__contentText-nlxc")

@pytest.fixture
def setup_browser():
    """
        Initializes and configures a Chrome WebDriver instance for testing.
        - Runs the browser in **incognito mode** to prevent caching issues.
        - **Disables extensions** for a clean test environment.
        - **Maximizes the browser window** for better element visibility.
        - Uses `yield` to ensure proper cleanup after test execution.

        Yields:
            WebDriver: An instance of Chrome WebDriver for use in tests.
    """
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_car_valuation(setup_browser):
    """
        Test case to validate car valuation details retrieved from Motorway against expected values.

        - Extracts registration numbers from the input file.
        - Searches for each vehicle on the Motorway website.
        - Retrieves and compares actual car details (Make, Model, Year) with expected values.
        - Handles "Too many requests" errors by stopping execution.
        - Fails the test if actual details do not match expected details.

        Raises:
            Exception: If the system detects too many requests and asks to try again later.

        Asserts:
            The actual car details match the expected details for each registration number.
    """
    driver = setup_browser
    motorway = MotorwayPage(driver)
    reg_numbers = DataReader.extract_reg_numbers(CAR_INPUT_FILE)
    expected_values = DataReader.load_expected_values(CAR_OUTPUT_FILE)

    for reg in reg_numbers:
        motorway.open_url("https://motorway.co.uk/")
        motorway.search_vehicle_by_reg_number(reg)
        actual_value = motorway.get_car_valuation()
        if "Too many requests" in actual_value:
            raise Exception ("We have detected you are making a lot of requests to Motorway. Please try again later.")
        expected_value = expected_values.get(reg, "N/A")
        assert actual_value == expected_value, f"Mismatch for {reg}: Expected {expected_value}, got {actual_value}"
