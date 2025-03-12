import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import getpass
import os


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

    def test_check_navbar(self):
        navbar = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]')
        assert navbar.is_displayed(), "Navbar is not displayed"

    def test_pasien_pengunjung_button(self):
        text = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/a[1]')
        text_href = text.get_attribute("href")
        button = self.driver.find_element(By.XPATH, "//a[p[contains(text(), 'Pasien & Pengunjung')]]")
        expected_href = "https://www.siloamhospitals.com/"
        assert text_href == expected_href, f"Wrong link! Found: {text_href}, Expected: {expected_href}"
        assert button.is_displayed(), "Button 'Pasien' is not visible on the page."

    def test_perusahaan_button(self):
        text = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/a[2]')
        text_href = text.get_attribute("href")
        button = self.driver.find_element(By.XPATH, "//a[p[contains(text(), 'Perusahaan')]]")
        expected_href = "https://www.siloamhospitals.com/tentang-kami"
        assert text_href == expected_href, f"Wrong link! Found: {text_href}, Expected: {expected_href}"
        assert button.is_displayed(), "Button is not displayed"

    def test_healthpedia(self):
        text = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/a[3]')
        text_href = text.get_attribute("href")
        expected_href = "https://www.siloamhospitals.com/informasi-siloam/artikel"
        button = self.driver.find_element(By.XPATH, "//a[p[contains(text(), 'Healthpedia')]]")
        assert text_href == expected_href, f"Wrong link! Found: {text_href}, Expected: {expected_href}"
        assert button.is_displayed(), "Button is not displayed"

    def test_ambulance_button(self):
        wait = WebDriverWait(self.driver, 10)
        ambulance_logo = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[1]/a/img')))
        ambulance_phone_number_text = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[1]/a')))
        ambulance_phone_number_href = ambulance_phone_number_text.get_attribute("href")
        ambulance_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[a[contains(text(), 'Emergensi 1-500-911')]]")))
        expected_href = "tel:1500911"
        assert ambulance_logo.is_displayed(), "Logo is not found"
        assert ambulance_phone_number_text.text == "Emergensi 1-500-911", "Text is incorrect"
        assert ambulance_phone_number_href == expected_href, f"Wrong phone link! Found: {ambulance_phone_number_href}, Expected: {expected_href}"
        assert ambulance_button.is_displayed(), "Button is not displayed"

    def test_whatsapp_button(self):
        wait = WebDriverWait(self.driver, 10)
        whatsapp_logo = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[2]/a/img')))
        whatsapp_text = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[2]/a')))
        whatsapp_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[.//span[contains(text(), 'WhatsApp')]]")))
        whatsapp_href = whatsapp_text.get_attribute("href")
        expected_href = "https://api.whatsapp.com/send/?phone=628118951181&text&app_absent=0"
        assert whatsapp_logo.is_displayed(), "Logo is not found"
        assert whatsapp_text.text == "WhatsApp"
        assert whatsapp_href == expected_href, f"Wrong phone link! Found: {whatsapp_href}, Expected: {expected_href}"
        assert whatsapp_button.is_displayed(), "Button is not displayed"

    def test_hubungi_kami_button(self):
        wait = WebDriverWait(self.driver, 10)
        hubungi_kami_logo = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/a/button/div/img')))
        hubungi_kami_text = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/a')))
        hubungi_kami_href = hubungi_kami_text.get_attribute("href")
        expected_href = "https://www.siloamhospitals.com/call-center"
        hubungi_kami_button = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/a/button')
        assert hubungi_kami_logo.is_displayed(), "Logo is not found"
        assert hubungi_kami_text.text == "Hubungi Kami"
        assert hubungi_kami_href == expected_href, f"Wrong link! Found: {hubungi_kami_href}, Expected: {expected_href}"
        assert hubungi_kami_button.is_displayed(), "Button is not activated"

    def test_login_button(self):
        """Login using dynamic username and password"""
        wait = WebDriverWait(self.driver, 10)

        phone_input = input("Enter login (e.g., phone number or username): ")
        password_input = getpass.getpass("Enter password: ")

        # Klik tombol login dengan menunggu hingga bisa diklik
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/button[3]')))
        login_button.click()

        # Masukkan username/phone
        login_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginPhone"]/fieldset/div[1]/input')))
        login_field.send_keys(phone_input)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modalLoginRevamp"]/div[2]/div/button')))
        next_button.click()

        # Masukkan password
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modalLoginRevamp"]/div[2]/div/div[2]/div[2]/div/div[1]/fieldset/div/input')))
        password_field.send_keys(password_input)

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modalLoginRevamp"]/div[2]/div/div[2]/div[3]/button')))
        submit_button.click()

        # Cek apakah login berhasil dengan menunggu elemen yang menunjukkan status login
        try:
            data_login = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/div/div[1]/nav/div[1]/div/button/div/p')))
            assert data_login.is_displayed(), "Login Failed"
            print("Login Successful")
        except Exception as e:
            print("Login Failed:", str(e))


        

    def test_responsive(self):
        """Tests tablet responsiveness by resizing the window."""
        self.driver.set_window_size(768, 1024)
        assert self.driver.execute_script("return window.innerWidth") <= 768, "Tablet view width check failed"

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