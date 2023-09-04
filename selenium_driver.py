from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = './chromedriver'
options = Options()


def set_options(options):
    # options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')


def get_browser():
    return webdriver.Chrome(options=options)
