from abc import abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class AutomationInstance:
    driver: WebDriver | None = None

    @classmethod
    @abstractmethod
    def set_driver(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')

        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    @abstractmethod
    def setup(cls):
        cls.set_driver()

    @classmethod
    @abstractmethod
    def given(cls):
        pass

    @classmethod
    @abstractmethod
    def when(cls):
        pass

    @classmethod
    @abstractmethod
    def then(cls):
        pass

    @classmethod
    @abstractmethod
    def tear_down(cls):
        cls.driver.quit()

    @classmethod
    def run(cls):
        cls.setup()
        cls.given()
        cls.when()
        cls.then()
        cls.tear_down()
