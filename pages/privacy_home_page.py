from selenium.webdriver.common.by import By
from utilities.webdriver_extension import WebDriverExtension


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.ext = WebDriverExtension(driver)
        self.create_card_button = (By.XPATH, "// button[text() = ' Create Card ']")
        self.card_number_we = (By.CSS_SELECTOR, "[data-test='card-pan']")
        self.card_exp_we = (By.CSS_SELECTOR, "[data-test='card-exp']")
        self.close_card_modal = (By.CSS_SELECTOR, "button[class='modal-close']")
        self.card_cvv_we = (By.XPATH, "(//div[@class='copyable']//span[@class='lighter'])[2]")
        self.new_card = (By.XPATH, "(//button[text()=' New Card '])[2]")
        self.card_number = None
        self.card_exp = None
        self.card_cvv = None

    def create_card(self):
        self.ext.find_and_click(self.new_card)
        self.ext.find_and_click(self.create_card_button)
        self.card_number = self.ext.get_element_text(self.card_number_we)
        self.card_exp = self.ext.get_element_text(self.card_exp_we)
        self.card_cvv = self.ext.get_element_text(self.card_cvv_we)
        self.ext.find_and_click(self.close_card_modal)

