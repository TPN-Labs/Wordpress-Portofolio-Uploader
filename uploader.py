import time
import os

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from auth import WP_DOMAIN, WP_PORTFOLIO_DOMAIN
from modal import select_photo_from_options


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

    def replace_post_content(self, title):
        tries = 0
        while (tries < 5):
            try:
                container_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[4]/div[2]/div[2]/div/div/div/div/div[2]/div[3]"
                container = self.driver.find_element(By.XPATH, container_xpath)
                self.actions.move_to_element(container).context_click().perform()
                break
            except:
                time.sleep(3)
                tries += 1
                print("[UPLOADER] Could not find post container, retrying..")

        container_title_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[8]/ul/li[1]"
        container_title = self.driver.find_element(By.XPATH, container_title_xpath)
        container_title.click()
        time.sleep(1)

        iframe = self.driver.find_element(By.ID, 'element_content_ifr')
        self.driver.switch_to.frame(iframe)

        textarea_xpath = "/html/body/p"
        textarea = self.driver.find_element(By.XPATH, textarea_xpath)
        textarea.send_keys(Keys.COMMAND + "A")
        time.sleep(1)
        textarea.send_keys(title)

        self.driver.switch_to.default_content()

    def save_post_changes(self):
        text_block_save_xpath = "/html/body/div[15]/div/div/div[2]/a[1]"
        text_block_save_button = self.driver.find_element(By.XPATH, text_block_save_xpath)
        text_block_save_button.click()

    def replace_post_photo(self, name):
        container_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[4]/div[3]/div[2]/div/div/div/div/div[2]/div[3]"
        container = self.driver.find_element(By.XPATH, container_xpath)
        self.actions.move_to_element(container).context_click().perform()
        time.sleep(1)

        container_edit_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[3]/div[1]/div[1]/div[2]/div/div[8]/ul/li[1]"
        container_edit = self.driver.find_element(By.XPATH, container_edit_xpath)
        container_edit.click()
        time.sleep(1)

        edit_photo_xpath = "/html/body/div[17]/div/div/div[3]/div/div[1]/ul/li[1]/div[2]/div/input[2]"
        edit_photo = self.driver.find_element(By.XPATH, edit_photo_xpath)
        edit_photo.click()
        time.sleep(1)

        search_asset_xpath = "/html/body/div[18]/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/input"
        search_asset = self.driver.find_element(By.XPATH, search_asset_xpath)
        search_asset.send_keys(name)
        time.sleep(3)

        search_tries = 0
        photo_is_found = False
        while search_tries < 5 and not photo_is_found:
            try:
                photo_results_xpath = "/html/body/div[18]/div[1]/div/div/div[3]/div[2]/div/div[3]/ul"
                photo_results = self.driver.find_element(By.XPATH, photo_results_xpath).find_elements(By.TAG_NAME, 'li')

                photo_is_found, photo_index = select_photo_from_options(photo_results, name)

                if photo_is_found:
                    photo_option_xpath = "/html/body/div[18]/div[1]/div/div/div[3]/div[2]/div/div[3]/ul/li[" + str(photo_index) + "]/div/div"
                    photo_option = self.driver.find_element(By.XPATH, photo_option_xpath)
                    photo_option.click()

                search_tries += 1
            except Exception as error:
                time.sleep(3)
                search_tries += 1
                print("[UPLOADER] Could not find result, retrying..")
                print(error)

        insert_button_xpath = "/html/body/div[18]/div[1]/div/div/div[4]/div/div[2]/button"
        insert_button = self.driver.find_element(By.XPATH, insert_button_xpath)
        insert_button.click()
        time.sleep(3)

        save_button_xpath = "/html/body/div[17]/div/div/div[2]/a[1]"
        save_button = self.driver.find_element(By.XPATH, save_button_xpath)
        save_button.click()
        time.sleep(3)

    def publish_post(self):
        publish_button_xpath = "/html/body/div[1]/div[4]/a[3]"
        publish_button = self.driver.find_element(By.XPATH, publish_button_xpath)
        publish_button.click()
        time.sleep(1)

    def delete_file(self, photo_path):
        os.remove(photo_path)

    def select_post_category(self, category):
        if category == 'paintings-transitions':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[13]"
        elif category == 'paintings-junkyard-symphony':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[10]"
        elif category == 'paintings-personal-mythologies':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]/ul/li[8]"
        elif category == 'paintings-memories-of-the-future':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]/ul/li[4]"
        elif category == 'paintings-playing-war':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]/ul/li[5]"
        elif category == 'paintings-the-ordinary-and-the-divine':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]/ul/li[7]"
        elif category == 'paintings-synthetic-future':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]/ul/li[6]"
        elif category == 'paintings-hybrid-playground':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]/ul/li[2]"
        elif category == 'paintings-heaven-and-earth':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]/ul/li[1]"
        elif category == 'digital-art-cosmic-junk':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[1]"
        elif category == 'drawings-junkyard':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[5]"
        elif category == 'drawings-meet-me':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[6]"
        elif category == 'drawings-playground':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[7]"
        elif category == 'drawings-synthetic':
            category_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[4]/div[2]/div/div[2]/ul/li[8]"

        category_option = self.driver.find_element(By.XPATH, category_xpath)
        category_option.click()

    def replace_thumbnail(self, name):
        set_thumbnail_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div/div[2]/div/div[9]/div[2]/p/a"
        set_thumbnail_button = self.driver.find_element(By.XPATH, set_thumbnail_xpath)
        set_thumbnail_button.click()
        time.sleep(1)

        search_asset_xpath = "/html/body/div[15]/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/input"
        search_asset = self.driver.find_element(By.XPATH, search_asset_xpath)
        search_asset.send_keys(name)
        time.sleep(3)

        search_tries = 0
        photo_is_found = False
        while search_tries < 5 and not photo_is_found:
            try:
                photo_results_xpath = "/html/body/div[15]/div[1]/div/div/div[3]/div[2]/div/div[3]/ul"
                photo_results = self.driver.find_element(By.XPATH, photo_results_xpath).find_elements(By.TAG_NAME, 'li')

                photo_is_found, photo_index = select_photo_from_options(photo_results, name)

                if photo_is_found:
                    photo_option_xpath = "/html/body/div[15]/div[1]/div/div/div[3]/div[2]/div/div[3]/ul/li[" + str(photo_index) + "]/div/div"
                    photo_option = self.driver.find_element(By.XPATH, photo_option_xpath)
                    photo_option.click()

                search_tries += 1
            except Exception as error:
                time.sleep(3)
                search_tries += 1
                print("[UPLOADER] Could not find result, retrying..")
                print(error)

        set_image_button_xpath = "/html/body/div[15]/div[1]/div/div/div[4]/div/div[2]/button"
        set_image_button = self.driver.find_element(By.XPATH, set_image_button_xpath)
        set_image_button.click()
        time.sleep(3)

    def upload_photo(self, photo):
        self.driver.get(WP_PORTFOLIO_DOMAIN)
        self.create_new_post()
        self.replace_post_title(photo.title)
        time.sleep(2)

        self.replace_post_content(photo.title)
        self.save_post_changes()
        self.select_post_category(photo.category)
        self.replace_thumbnail(photo.file_name)

        self.replace_post_photo(photo.file_name)
        self.publish_post()
        print("[UPLOADER] Photo uploaded successfully, deleting..")
        self.delete_file(photo.path)
        time.sleep(1)
