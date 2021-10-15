import re
from typing import Tuple
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver import FirefoxOptions


def set_firfox_options()-> Tuple[FirefoxProfile, FirefoxOptions]:
    fp = FirefoxProfile()
    fp.set_preference("http.response.timeout", 5)
    fp.set_preference("dom.max_script_run_time", 5)

    options = FirefoxOptions()
    options.add_argument('-headless')
    
    return fp, options