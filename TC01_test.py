import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os


@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    request.cls.driver = driver
    request.addfinalizer(driver.quit) 

@pytest.mark.usefixtures("setup")
class TestComponents:
    URL = "https://www.siloamhospitals.com/"

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Ensures each test starts on the homepage."""
        self.driver.get(self.URL)
    
    def test_check_navbar(self):
        navbar = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]' )
        assert navbar.is_displayed(), "Navbar is not displayed"

    def test_pasien_pengunjung_button(self):
        text = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/a[1]')
        text_href = text.get_attribute("href")
        button = self.driver.find_element(By.XPATH, "//a[p[contains(text(), 'Pasien & Pengunjung')]]")
        expected_href = "https://www.siloamhospitals.com/"
        assert text_href == expected_href, f"wrong link! Found: {text_href}, Expected: {expected_href}"
        assert button.is_displayed(), "Button 'Pasien' is not visible on the page."
     
    def test_perusahaan_button(self):
        text = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/a[2]')
        text_href = text.get_attribute("href")
        button = self.driver.find_element(By.XPATH, "//a[p[contains(text(), 'Perusahaan')]]")
        expected_href = "https://www.siloamhospitals.com/tentang-kami"
        assert text_href == expected_href, f"wrong link! Found: {text_href}, Expected: {expected_href}"
        assert button.is_displayed(), "Button is not displayed"

    def test_healthpedia(self):
        text = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/a[3]')
        text_href = text.get_attribute("href")
        expected_href = "https://www.siloamhospitals.com/informasi-siloam/artikel"
        button = self.driver.find_element(By.XPATH, "//a[p[contains(text(), 'Healthpedia')]]")
        assert text_href == expected_href, f"wrong link! Found: {text_href}, Expected: {expected_href}"
        assert button.is_displayed(), "Button is not displayed"

    def test_ambulance_button(self):
        ambulance_logo = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/button[1]/a/img')
        ambulance_phone_number_text = emergency_phone_number = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/button[1]/a')
        ambulance_phone_number_href = ambulance_phone_number_text.get_attribute("href")
        ambulance_button = self.driver.find_element(By.XPATH, "//button[a[contains(text(), 'Emergensi 1-500-911')]]")
        expected_href = "tel:1500911"
        assert ambulance_logo.is_displayed(),"Logo is not found"
        assert ambulance_phone_number_text.text ==  "Emergensi 1-500-911","Text is invalid (the correct:  Emergensi 1-500-911)"
        assert ambulance_phone_number_href  == expected_href, f"Wrong phone link! Found: {ambulance_phone_number_href}, Expected: {expected_href}"
        assert ambulance_button.is_displayed(), "button is not displayed"
        
    def test_whatsapp_button(self):
        whatsapp_logo = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/button[2]/a/img')
        whatsapp_text = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/button[2]/a')
        whatsapp_button = self.driver.find_element(By.XPATH, "//a[.//span[contains(text(), 'WhatsApp')]]")
        whatsapp_href = whatsapp_text.get_attribute("href")
        expected_href = "https://api.whatsapp.com/send/?phone=628118951181&text&app_absent=0"
        assert whatsapp_logo.is_displayed(),"Logo is not found"
        assert whatsapp_text.text == "WhatsApp"
        assert whatsapp_href == expected_href, f"Wrong phone link! Found: {whatsapp_href}, Expected: {expected_href}"
        assert whatsapp_button.is_displayed(), "Button is not displayed"

    def test_hubungi_kami_button(self):
        hubungi_kami_logo = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/a/button/div/img')
        hubungi_kami_text = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/a')
        hubungi_kami_href = hubungi_kami_text.get_attribute("href")
        expected_href = "https://www.siloamhospitals.com/call-center"
        hubungi_kami_button = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/a/button')
        assert hubungi_kami_logo.is_displayed(),"Logo is not found"
        assert hubungi_kami_text.text == "Hubungi Kami"
        assert hubungi_kami_href == expected_href, f"Wrong phone link! Found: {hubungi_kami_href}, Expected: {expected_href}"
        assert hubungi_kami_button.is_displayed(), "button is not activate"

    def test_login_button(self):
        login_button = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[3]')
        assert login_button.is_displayed(), "Login button is not displayed"
        login_button.click()
        wait = WebDriverWait(self.driver, 10)
        login_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginPhone"]/fieldset/div[1]')))
        assert login_field.is_displayed(), "Login field is not displayed after clicking the button"


    # def test_check_logo(self):
    #     """Verifies that the hospital logo is displayed."""
    #     logo = self.driver.find_element(By.XPATH, "//img[@alt='Siloam Hospitals']")
    #     assert logo.is_displayed(), "Logo is not displayed"

    # def test_check_button(self):
    #     """Checks if a button is enabled."""
    #     button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Daftar Sekarang')]")
    #     assert button.is_enabled(), "Button is disabled"

    # def test_check_link(self):
    #     """Checks if a link contains a valid href attribute."""
    #     link = self.driver.find_element(By.XPATH, "//a[contains(text(),'Lihat Detail')]")
    #     assert link.get_attribute("href"), "Link does not have a valid href"

    def test_responsive(self):
        """Tests tablet responsiveness by resizing the window."""
        self.driver.set_window_rect(0, 0, 768, 1024) 
        assert self.driver.execute_script("return window.innerWidth <= 768"), "Tablet view failed"

if __name__ == "__main__":
    report_dir = os.path.abspath("test_reports")
    os.makedirs(report_dir, exist_ok=True)
    test_file_name = os.path.basename(__file__).replace(".py", "")
    report_file = os.path.join(report_dir, f"{test_file_name}_report.html")
    pytest.main([
        f"--html={report_file}",
        "--self-contained-html"
    ])