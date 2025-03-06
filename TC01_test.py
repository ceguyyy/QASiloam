import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
        expected_href = "https://www.siloamhospitals.com/"
        assert text_href == expected_href, f"wrong link! Found: {text_href}, Expected: {expected_href}"
     
    def test_perusahaan_button(self):
        text = self.drive.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/a[2]')
        text_href = text.get_attribute("href")
        expected_href = "https://www.siloamhospitals.com/tentang-kami"
        assert text_href == expected_href, f"wrong link! Found: {text_href}, Expected: {expected_href}"

    def test_healthpedia(self):
        text = self.drive.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/a[3]/p')
        text_href = text.get_attribute("href")
        expected_href = "https://www.siloamhospitals.com/informasi-siloam/artikel"
        assert text_href == expected_href, f"wrong link! Found: {text_href}, Expected: {expected_href}"

    def test_ambulance_button(self):
        ambulance_logo = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/button[1]/a/img')
        assert ambulance_logo.is_displayed(),"Logo is not found"
        
    def test_phone_number_button(self):
        emergency_phone_number_logo = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[2]/a/img')
        emergency_phone_number = self.driver.find_element(By.XPATH,'//*[@id="navbar"]/div/div[1]/nav/div[1]/button[1]/a')
        phone_href = emergency_phone_number.get_attribute("href")
        expected_href = "tel:1500911"
        assert phone_href == expected_href, f"Wrong phone link! Found: {phone_href}, Expected: {expected_href}"
        assert emergency_phone_number.text == "Emergensi 1-500-911","Text is invalid (the correct:  Emergensi 1-500-911)"
        assert emergency_phone_number_logo.is_displayed(), "Image is not found"


    def test_check_logo(self):
        """Verifies that the hospital logo is displayed."""
        logo = self.driver.find_element(By.XPATH, "//img[@alt='Siloam Hospitals']")
        assert logo.is_displayed(), "Logo is not displayed"

    def test_check_button(self):
        """Checks if a button is enabled."""
        button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Daftar Sekarang')]")
        assert button.is_enabled(), "Button is disabled"

    def test_check_link(self):
        """Checks if a link contains a valid href attribute."""
        link = self.driver.find_element(By.XPATH, "//a[contains(text(),'Lihat Detail')]")
        assert link.get_attribute("href"), "Link does not have a valid href"

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