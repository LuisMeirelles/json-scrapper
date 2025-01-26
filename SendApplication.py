import json
import re
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from AutomationInstance import AutomationInstance


class SendApplication(AutomationInstance, ABC):
    details_element: WebElement | None = None
    address_element: WebElement | None = None
    extra_info_element: WebElement | None = None

    new_data = {}

    @classmethod
    def given(cls):
        driver = cls.driver

        driver.get('https://pt.fakenamegenerator.com/index.php')

        details_element = driver.find_element(By.CSS_SELECTOR, '#details .content .info .content')

        SendApplication.details_element = details_element

        SendApplication.address_element = details_element.find_element(By.CLASS_NAME, 'address')
        SendApplication.extra_info_element = details_element.find_element(By.CLASS_NAME, 'extra')

    @classmethod
    def when(cls):
        SendApplication.set_name()
        SendApplication.set_ssn()
        SendApplication.set_email()
        SendApplication.set_address()
        SendApplication.set_phone()

    @classmethod
    def then(cls):
        SendApplication.merge_file_and_generated_data()

    @staticmethod
    def set_name():
        name = SendApplication.address_element.find_element(By.TAG_NAME, 'h3').text

        [first_name, *_, last_name] = name.split(' ')

        SendApplication.new_data['mainFirstName'] = first_name
        SendApplication.new_data['mainLastName'] = last_name

    @staticmethod
    def set_ssn():
        ssn = SendApplication.extra_info_element.find_element(
            By.XPATH,
            '//*[contains(text(), "SSN")]/following-sibling::dd[1]'
        ).text.replace('-', '').split()[0]

        SendApplication.new_data['mainSSN'] = ssn

    @staticmethod
    def set_email():
        email = SendApplication.extra_info_element.find_element(
            By.XPATH, '//*[contains(text(), "Endereço de e-mail")]/following-sibling::dd[1]'
        ).text.split()[0]

        SendApplication.new_data['emailAddress'] = email

    @staticmethod
    def set_address():
        full_address = SendApplication.address_element.find_element(by=By.CLASS_NAME, value='adr').text
        [main_address_1, city, state, zip_code] = re.match(r'(\d+\s.+)\n(.+), ([A-Z]{2}) (\d+)', full_address).groups()

        SendApplication.new_data['mainAddress1'] = main_address_1
        SendApplication.new_data['mainCity'] = city
        SendApplication.new_data['mainStateOrProvince'] = state
        SendApplication.new_data['mainPostalCode'] = zip_code

    @staticmethod
    def set_phone():
        cell_phone = SendApplication.extra_info_element.find_element(
            By.XPATH, '//dt[contains(text(), "Telefone")]/following-sibling::dd[1]'
        ).text.replace('-', '')

        SendApplication.new_data['mainCellPhone'] = cell_phone

    @staticmethod
    def merge_file_and_generated_data():
        with open('./stubs/sendApplication.json', 'r') as file:
            stub = json.load(file)

            stub.update(SendApplication.new_data)
        with open('./output/sendApplication.json', 'w') as file:
            file.write(json.dumps(stub, indent=4))
