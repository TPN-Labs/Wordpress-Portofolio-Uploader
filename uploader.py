import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from auth import WP_DOMAIN, WP_PORTFOLIO_DOMAIN


class Uploader:
    def __init__(self, username, password, driver):
        self.actions = ActionChains(driver)
        self.username = username
        self.password = password
        self.driver = driver

    def login_to_wordpress(self):
        self.driver.get(WP_DOMAIN + '/wp-admin')
        time.sleep(3)
        username_box = self.driver.find_element(By.ID, 'user_login')
        password_box = self.driver.find_element(By.ID, 'user_pass')
        username_box.send_keys(self.username)
        password_box.send_keys(self.password)
        password_box.submit()
        print('[UPLOADER] Logged in to WordPress')
        time.sleep(3)

    def create_new_post(self):
        self.click_backend_builder()
        self.click_import_button()
        self.click_replace_template_button()

    def click_backend_builder(self):
        button_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[1]/div[2]/a[1]"
        backend_button = self.driver.find_element(By.XPATH, button_xpath)
        backend_button.click()

    def click_import_button(self):
        import_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[1]/a[3]"
        import_button = self.driver.find_element(By.XPATH, import_xpath)
        import_button.click()

    def click_replace_template_button(self):
        load_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[5]/div/div[2]/div[6]/ul/li/span/a[1]"
        load_button = self.driver.find_element(By.XPATH, load_xpath)
        self.actions.move_to_element(load_button).context_click().perform()
        time.sleep(1)

        replace_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[5]/div/div[2]/div[6]/ul/li/span/a[1]/div/div/div/span[1]"
        replace_button = self.driver.find_element(By.XPATH, replace_xpath)
        replace_button.click()
        time.sleep(1)

    def replace_post_title(self, title):
        title_box = self.driver.find_element(By.ID, 'title')
        title_box.send_keys(title)

    def replace_post_content(self):
        container_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[4]/div[2]/div[2]/div/div/div/div/div[2]/div[3]"
        container = self.driver.find_element(By.XPATH, container_xpath)
        self.actions.move_to_element(container).context_click().perform()
        time.sleep(1)

        container_title_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[8]/ul/li[1]"
        container_title = self.driver.find_element(By.XPATH, container_title_xpath)
        container_title.click()
        time.sleep(1)

        self.driver.switch_to.frame(0)

        textarea_xpath = "/html/body/p"
        textarea = self.driver.find_element(By.XPATH, textarea_xpath)
        textarea.send_keys("Hello world!")

        self.driver.switch_to.default_content()

    def upload_photo(self, photo):
        self.driver.get(WP_PORTFOLIO_DOMAIN)
        self.create_new_post()
        self.replace_post_title(photo.title)
        time.sleep(2)

        self.replace_post_content()
        time.sleep(10)
