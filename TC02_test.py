import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import getpass
import os
import time

@pytest.fixture(scope="class")
def setup(request):
    """Sets up the WebDriver and ensures it quits after tests are done."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.quit()  # Ensures driver quits after tests

@pytest.mark.usefixtures("setup")
class TestComponents:
    URL = "https://www.siloamhospitals.com/"

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Ensures each test starts on the homepage."""
        self.driver.get(self.URL)

    def test_login_button(self):
        """Login using dynamic username and password"""
        wait = WebDriverWait(self.driver, 10)

        phone_input = input("Enter login (e.g., phone number or username): ")
        password_input = getpass.getpass("Enter password: ")

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[2]')))
        login_button.click()

        login_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginPhone"]/fieldset/div[1]/input')))
        login_field.send_keys(phone_input)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modalLoginRevamp"]/div[2]/div/button')))
        next_button.click()

        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modalLoginRevamp"]/div[2]/div/div[2]/div[2]/div/div[1]/fieldset/div/input')))
        password_field.send_keys(password_input)

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modalLoginRevamp"]/div[2]/div/div[2]/div[3]/button')))
        submit_button.click()

        try:
            data_login = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/div/button/div/p')))
            assert data_login.is_displayed(), "Login Failed"
            print("Login Successful")
        except Exception as e:
            print("Login Failed:", str(e))

    def test_MCU(self):
        wait = WebDriverWait(self.driver, 10)

        # Locate the MCU button
        mcu_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="homepage"]/div[2]/div/div/div[3]/a')))
        mcu_href = mcu_button.get_attribute("href")
        expected_href = "https://www.siloamhospitals.com/mcu/cari-paket"

        assert mcu_button.is_displayed(), "MCU button not displayed"
        assert mcu_href == expected_href, f"Wrong link! Found: {mcu_href}, Expected: {expected_href}"

        # Click the MCU button
        mcu_button.click()

        # Try to handle modal if it's present
        try:
            # Check if the modal is present
            time.sleep(5)
            modal_overlay = self.driver.find_element(EC.visibility_of_element_located((By.XPATH, '//*[@id="modal"]')))
            if modal_overlay.is_displayed():
                # Find and click the location button inside the modal
                location_button = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="modal"]/div/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/fieldset/div/input')
                ))
                location_button.click()

                # Find and click the first checkbox (city button) inside the modal
                firstcheckbox_city_button = wait.until(EC.visibility_of_element_located(
                    (By.XPATH,'//*[@id="modal"]/div/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[3]/div[2]/div[1]')
                ))
                firstcheckbox_city_button.click()

        except:
            # If the modal is not displayed or the modal is not found, print a message and continue
            print("Modal not found or not displayed, proceeding without it.")
    
        # Ensure that the first product is displayed and click it
        first_product = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Home"]/main/div[1]/section[3]/div/div/div[4]/div/div[1]/div[2]/div[1]/div/a')))
        assert first_product.is_displayed(), "Product 1 not found"
        first_product.click()


        title_text = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="info"]/h2')))
        assert title_text.is_displayed(), "Title didn't show"


        keranjang_buttons = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="buttonCart"]')))
        assert keranjang_buttons, "Button not found"  # Ensure the list is not empty
        assert keranjang_buttons[0].is_displayed(), "Button is disabled"  # Check the first button


        keranjang_buttons[0].click()

        time.sleep(5)


if __name__ == "__main__":
    report_dir = os.path.abspath("test_reports")
    os.makedirs(report_dir, exist_ok=True)
    test_file_name = os.path.basename(__file__).replace(".py","")
    
    report_file = os.path.join(report_dir, f"{test_file_name}_report.html")
    
    pytest.main([
        "-s",
        "--html=" + report_file,
        "--self-contained-html"
    ])