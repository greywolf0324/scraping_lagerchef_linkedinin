import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

if __name__ == '__main__':
    URL = "https://www.linkedin.com"
    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(URL)

    login_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//div/a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]'))
    )
    login_btn.click()
    driver.implicitly_wait(15)

    try:
        mem_btn = driver.find_element(By.XPATH, '//div[@class="artdeco-list__item signin-other-account list-box"]')
        mem_btn.click()
    except:
        pass

    driver.implicitly_wait(15)
    input_username = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@id="username"]'))
    )
    driver.implicitly_wait(5)
    input_username.send_keys('plz write username here!!!')

    input_password = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@id="password"]'))
    )
    driver.implicitly_wait(5)
    input_password.send_keys('plz write password here!!!')

    login_button = driver.find_element(By.XPATH, '//button[@class="btn__primary--large from__button--floating"]')
    login_button.click()

    search_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//div [@class="search-global-typeahead__collapsed-search-button-text t-black--light t-12 t-normal"]'))
    )
    search_btn.click()
    search_btn.send_keys('lagerchef')
    search_btn.send_keys(Keys.RETURN)

    people_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "People")]'))
    )
    people_btn.click()

    usable_data = []

    driver.implicitly_wait(5)
    next_btn = driver.find_element(By.XPATH, '//button [@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')

    while next_btn.isEnabled():
        eles = driver.find_elements(By.XPATH, '//div/div/div/p/strong')
        for ele in eles:
            names = driver.find_element(By.XPATH, '//div[@class="entity-result__secondary-subtitle t-14 t-normal"]')
            pos = driver.find_element(By.XPATH, '//div/div/div/p')
            usable_data.append([{"position": pos.text},{"name" : names.text}])
        next_btn.click()
        next_btn = driver.find_element(By.XPATH, '//button [@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')

    eles = driver.find_elements(By.XPATH, '//div/div/div/p/strong')
    for ele in eles:
        names = driver.find_element(By.XPATH, '//div[@class="entity-result__secondary-subtitle t-14 t-normal"]')
        pos = driver.find_element(By.XPATH, '//div/div/div/p')
        usable_data.append([{"position": pos.text},{"name" : names.text}])
    df = pd.DataFrame(usable_data)
    df.to_excel("research.xlsx")