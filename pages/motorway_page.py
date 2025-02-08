from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class MotorwayPage(BasePage):
    """
        This class is about  a start  page on the Motorway website.
        It provides methods to search for a vehicle by registration number and retrieve vehicle valuation details.
    """
    SEARCH_BOX = (By.NAME, "vrm-input")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    MAKE_MODEL = (By.CLASS_NAME, "HeroVehicle__title-FAmG")
    YEAR = (By.CLASS_NAME, "HeroVehicle__details-XpAI")
    ERROR_NOTIFICATION = (By.CLASS_NAME, "Toast-shared-module__toastHeading-ozew")

    def search_vehicle_by_reg_number(self, reg_number):
        """
            This method will use for search by vehicle registration numbers and submit the button
        """
        reg_input_field = self.driver.find_element(By.ID, "vrm-input")
        reg_input_field.clear()
        self.enter_text(self.SEARCH_BOX, reg_number)
        self.click_element(self.SUBMIT_BUTTON)


    def get_car_valuation(self):
        """
            This method used for get car valuation like YEAR and MODEL
        """
        error_notification = self.find_element(self.ERROR_NOTIFICATION)
        if error_notification.is_displayed():
            return error_notification.text
        make_model = self.find_element(self.MAKE_MODEL).text
        year = self.find_element(self.YEAR).text.strip().split("\n")[0]
        return {"MAKE_MODEL": make_model, "YEAR": year}




