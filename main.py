from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import os


PROMISED_DOWN = 100     # Velocidade de download cobrada pelo provedor.
PROMISED_UP = 100
TWITTER_EMAIL = os.getenv("EMAIL")
TWITTER_USERNAME = os.getenv("USERNAME")
TWITTER_PASSWORD = os.getenv("PASSWORD")
DRIVER_PATH = os.getenv("DRIVER_PATH")


class InternetSpeedTwitterBot:
    def __init__(self):
        self.service = Service(executable_path=DRIVER_PATH)
        self.driver = WebDriver(service=self.service)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        """Compara a velocidade da internet atual com a prometida pelo provedor.
        Se for menor, executa self.tweet_at_provider()."""
        self.driver.get("https://www.speedtest.net/")
        time.sleep(5)
        self.driver.find_element(By.CLASS_NAME, "start-text").click()
        time.sleep(50)  # 50 segundos de espera para realizar o teste de velocidade de internet.
        result = self.driver.find_elements(By.CLASS_NAME, "result-data-value ")
        self.down = float(result[1].text)   # Velocidade de download.
        self.up = float(result[2].text)     # Velocidade de upload.
        # print(f"Download: {self.down}\nUpload: {self.up}")
        if self.down < PROMISED_DOWN and self.up < PROMISED_UP:
            self.tweet_at_provider()

    def tweet_at_provider(self):
        """Twitta a velocidade da internet prometida e a velocidade da internet entregue pelo provedor."""
        self.driver.get("https://twitter.com/")
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/'
                                           'div[1]/div/div[3]/div[5]/a/div/span').click()
        time.sleep(3)
        self.driver.find_element(By.CLASS_NAME, "r-30o5oe").send_keys(TWITTER_EMAIL, Keys.ENTER)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "input").send_keys(TWITTER_USERNAME, Keys.ENTER)
        time.sleep(2)
        self.driver.find_elements(By.CSS_SELECTOR, "input")[1].send_keys(TWITTER_PASSWORD, Keys.ENTER)
        time.sleep(5)
        # Texto a ser twittado.
        self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block").send_keys(
            f"Pago por {PROMISED_DOWN}down/{PROMISED_UP}up de internet mas recebo apenas {self.down}down/{self.up}up.")
        time.sleep(3)
        self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/'
                                           'div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]'
                                           '/div/div/div[2]/div[3]').click()
        time.sleep(5)
        self.driver.quit()


twitter_bot = InternetSpeedTwitterBot()
twitter_bot.get_internet_speed()
