import os
import time

from selenium.common import NoSuchElementException, WebDriverException, TimeoutException

from Photo import PhotoDetails
from auth import WP_USERNAME, WP_PASSWORD
from selenium_driver import get_browser
from uploader import Uploader


def read_photos():
    all_photos = []
    all_directories = os.listdir('./assets')
    for directory in all_directories:
        all_files = os.listdir('./assets/' + directory)
        for file in all_files:
            file_name = file.split('.')[0]
            # photo_name = file_name
            photo_name = file_name.split(',')[0]
            photo_category = 'drawings-' + directory.replace(' ', '-').lower()
            # photo_category = 'digital-art-' + directory.replace(' ', '-').lower()
            photo_path = os.path.abspath('./assets/' + directory + '/' + file)
            photo = PhotoDetails(photo_name, photo_category, file_name, photo_path)
            all_photos.append(photo)

    return all_photos


def main():
    all_photos = read_photos()
    uploader = Uploader(WP_USERNAME, WP_PASSWORD, get_browser())
    uploader.login_to_wordpress()
    try:
        for idx in range(0, len(all_photos)):
            current_photo = all_photos[idx]
            print("[UPLOADER] Uploading photo [" + str(idx + 1) + "/" + str(len(all_photos)) + "]: " + current_photo.title)
            uploader.upload_photo(current_photo)
    except (NoSuchElementException, WebDriverException, TimeoutException) as error:
        print('[UPLOADER] Error: ' + str(error))
        time.sleep(1000)



if __name__ == "__main__":
    main()
