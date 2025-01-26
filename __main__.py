import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

new_data = {}

if __name__ == '__main__':
    driver = webdriver.Chrome()

    driver.get('https://pt.fakenamegenerator.com/index.php')

    details_element = driver.find_element(By.CSS_SELECTOR, '#details .content .info .content')

    address_element = details_element.find_element(By.CLASS_NAME, 'address')
    extra_info_element = details_element.find_element(By.CLASS_NAME, 'extra')

    name = address_element.find_element(By.TAG_NAME, 'h3').text

    [first_name, *middle_names, last_name] = name.split(' ')

    new_data['mainFirstName'] = first_name
    new_data['mainLastName'] = last_name

    ssn = extra_info_element.find_element(
        By.XPATH,
        '//*[contains(text(), "SSN")]/following-sibling::dd[1]'
    ).text.replace('-', '').split()[0]

    new_data['mainSSN'] = ssn

    email = extra_info_element.find_element(
        By.XPATH, '//*[contains(text(), "Endereço de e-mail")]/following-sibling::dd[1]'
    ).text.split()[0]

    new_data['emailAddress'] = email

    full_address = address_element.find_element(by=By.CLASS_NAME, value='adr').text

    [main_address_1, city, state, zip_code] = re.match(r'(\d+\s.+)\n(.+), ([A-Z]{2}) (\d+)', full_address).groups()

    new_data['mainAddress1'] = main_address_1
    new_data['mainCity'] = city
    new_data['mainStateOrProvince'] = state
    new_data['mainPostalCode'] = zip_code

    cell_phone = extra_info_element.find_element(
        By.XPATH, '//dt[contains(text(), "Telefone")]/following-sibling::dd[1]'
    ).text.replace('-', '')

    new_data['mainCellPhone'] = cell_phone

    with open('./stubs/sendApplication.json', 'r') as file:
        stub = json.load(file)

        stub.update(new_data)

    with open('./output/sendApplication.json', 'w') as file:
        file.write(json.dumps(stub,indent=4))

    driver.quit()
